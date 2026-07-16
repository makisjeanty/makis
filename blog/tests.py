from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import PerfilUsuario

from .models import Categoria, Comentario, Post, Tag


class PostModelTests(TestCase):
    def setUp(self):
        self.autor = PerfilUsuario.objects.create_user(username='makis', password='senha123')
        self.categoria = Categoria.objects.create(nome='Categoria de Teste')

    def _criar_post(self, **kwargs):
        defaults = dict(
            titulo='Como migrei um CSV para um modelo relacional',
            autor=self.autor,
            categoria=self.categoria,
            resumo='Resumo do post.',
            conteudo='Conteúdo completo do post.',
        )
        defaults.update(kwargs)
        return Post.objects.create(**defaults)

    def test_criar_post_basico(self):
        post = self._criar_post()
        self.assertEqual(Post.objects.count(), 1)
        self.assertFalse(post.publicado)  # default

    def test_slug_autogerado_a_partir_do_titulo(self):
        post = self._criar_post(titulo='Meu Primeiro Artigo Técnico')
        self.assertEqual(post.slug, 'meu-primeiro-artigo-tecnico')

    def test_autor_obrigatorio(self):
        post = Post(titulo='Sem autor', resumo='r', conteudo='c')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                post.save()

    def test_titulo_em_branco_falha_validacao(self):
        post = Post(titulo='', autor=self.autor, resumo='r', conteudo='c')
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_categoria_pode_ser_nula(self):
        post = self._criar_post(categoria=None)
        self.assertIsNone(post.categoria)

    def test_deletar_categoria_define_null_no_post(self):
        post = self._criar_post()
        self.categoria.delete()
        post.refresh_from_db()
        self.assertIsNone(post.categoria)

    def test_tags_relacionamento_muitos_para_muitos(self):
        post = self._criar_post()
        django_tag = Tag.objects.create(nome='Django')
        python_tag = Tag.objects.create(nome='Python')
        post.tags.add(django_tag, python_tag)
        self.assertEqual(post.tags.count(), 2)
        self.assertIn(post, django_tag.posts.all())  # related_name='posts'

    def test_ordering_mais_recente_primeiro(self):
        from django.utils import timezone
        p1 = self._criar_post(titulo='Post Antigo', slug='post-antigo', data_publicacao=timezone.now())
        p2 = self._criar_post(titulo='Post Novo', slug='post-novo', data_publicacao=timezone.now() + timezone.timedelta(days=1))
        self.assertEqual(list(Post.objects.all()), [p2, p1])


class ComentarioModelTests(TestCase):
    def setUp(self):
        self.autor = PerfilUsuario.objects.create_user(username='makis', password='senha123')
        self.post = Post.objects.create(
            titulo='Post com comentários',
            autor=self.autor,
            resumo='r',
            conteudo='c',
        )

    def test_criar_comentario_relacionado_ao_post(self):
        comentario = Comentario.objects.create(
            post=self.post, nome='Visitante', email='v@example.com', conteudo='Ótimo post!',
        )
        self.assertIn(comentario, self.post.comentarios.all())  # related_name='comentarios'
        self.assertFalse(comentario.aprovado)  # default

    def test_email_invalido_falha_validacao(self):
        comentario = Comentario(post=self.post, nome='Visitante', email='nao-e-email', conteudo='texto')
        with self.assertRaises(ValidationError):
            comentario.full_clean()

    def test_deletar_post_apaga_comentarios_em_cascata(self):
        Comentario.objects.create(post=self.post, nome='V1', email='v1@example.com', conteudo='c1')
        Comentario.objects.create(post=self.post, nome='V2', email='v2@example.com', conteudo='c2')
        self.assertEqual(Comentario.objects.count(), 2)
        self.post.delete()
        self.assertEqual(Comentario.objects.count(), 0)
