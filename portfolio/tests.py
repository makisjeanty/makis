import io

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase
from PIL import Image

from .models import ImagemProjeto, Projeto


def _imagem_valida(nome='teste.png'):
    buf = io.BytesIO()
    Image.new('RGB', (10, 10), color='blue').save(buf, format='PNG')
    return SimpleUploadedFile(nome, buf.getvalue(), content_type='image/png')


class ProjetoModelTests(TestCase):
    def _criar_projeto(self, **kwargs):
        defaults = dict(
            titulo='Sistema de Gestão',
            descricao_curta='Um sistema de gestão simples.',
            descricao_completa='Descrição completa do projeto.',
            imagem_principal=_imagem_valida(),
            tecnologias='Python, Django, MySQL',
        )
        defaults.update(kwargs)
        return Projeto.objects.create(**defaults)

    def test_criar_projeto_basico(self):
        projeto = self._criar_projeto()
        self.assertEqual(Projeto.objects.count(), 1)
        self.assertEqual(projeto.categoria, 'web')  # default
        self.assertEqual(projeto.tipo, 'pessoal')  # default

    def test_slug_autogerado_a_partir_do_titulo(self):
        projeto = self._criar_projeto(titulo='Sistema de Gestão Financeira')
        self.assertEqual(projeto.slug, 'sistema-de-gestao-financeira')

    def test_slug_explicito_nao_e_sobrescrito(self):
        projeto = self._criar_projeto(titulo='Sistema X', slug='slug-customizado')
        self.assertEqual(projeto.slug, 'slug-customizado')

    def test_slug_deve_ser_unico(self):
        self._criar_projeto(titulo='Projeto A', slug='mesmo-slug')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self._criar_projeto(titulo='Projeto B', slug='mesmo-slug')

    def test_titulo_em_branco_falha_validacao(self):
        projeto = Projeto(
            titulo='',
            descricao_curta='desc',
            descricao_completa='desc completa',
            imagem_principal=_imagem_valida(),
            tecnologias='Python',
        )
        with self.assertRaises(ValidationError):
            projeto.full_clean()

    def test_imagem_principal_obrigatoria(self):
        projeto = Projeto(
            titulo='Sem imagem',
            descricao_curta='desc',
            descricao_completa='desc completa',
            tecnologias='Python',
        )
        with self.assertRaises(ValidationError):
            projeto.full_clean()

    def test_get_tecnologias_list(self):
        projeto = self._criar_projeto(tecnologias='Python, Django , MySQL')
        self.assertEqual(projeto.get_tecnologias_list(), ['Python', 'Django', 'MySQL'])

    def test_ordering_mais_recente_primeiro(self):
        p1 = self._criar_projeto(titulo='Primeiro', slug='primeiro')
        p2 = self._criar_projeto(titulo='Segundo', slug='segundo')
        self.assertEqual(list(Projeto.objects.all()), [p2, p1])


class ImagemProjetoModelTests(TestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(
            titulo='Projeto com Galeria',
            descricao_curta='desc',
            descricao_completa='desc completa',
            imagem_principal=_imagem_valida(),
            tecnologias='Python',
        )

    def test_imagem_relacionada_ao_projeto(self):
        imagem = ImagemProjeto.objects.create(projeto=self.projeto, imagem=_imagem_valida('galeria.png'))
        self.assertIn(imagem, self.projeto.imagens.all())  # related_name='imagens'

    def test_deletar_projeto_apaga_imagens_em_cascata(self):
        ImagemProjeto.objects.create(projeto=self.projeto, imagem=_imagem_valida('g1.png'))
        ImagemProjeto.objects.create(projeto=self.projeto, imagem=_imagem_valida('g2.png'))
        self.assertEqual(ImagemProjeto.objects.count(), 2)
        self.projeto.delete()
        self.assertEqual(ImagemProjeto.objects.count(), 0)
