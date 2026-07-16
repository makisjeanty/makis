from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Habilidade, PerfilUsuario


class PerfilUsuarioModelTests(TestCase):
    def test_criar_perfil_usuario_basico(self):
        perfil = PerfilUsuario.objects.create_user(username='makis', password='senha123')
        self.assertEqual(PerfilUsuario.objects.count(), 1)
        self.assertEqual(perfil.cargo, 'Analista de Sistemas')  # default aplicado

    def test_str_representation(self):
        perfil = PerfilUsuario.objects.create_user(
            username='makis', password='senha123',
            first_name='Makis', last_name='Digital', cargo='Dev',
        )
        self.assertEqual(str(perfil), 'Makis Digital - Dev')

    def test_username_em_branco_falha_validacao(self):
        perfil = PerfilUsuario(username='', cargo='Dev')
        with self.assertRaises(ValidationError):
            perfil.full_clean()

    def test_username_duplicado_viola_constraint_unica(self):
        PerfilUsuario.objects.create_user(username='makis', password='senha123')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PerfilUsuario.objects.create_user(username='makis', password='outrasenha')

    def test_disponivel_para_trabalho_default_true(self):
        perfil = PerfilUsuario.objects.create_user(username='makis', password='senha123')
        self.assertTrue(perfil.disponivel_para_trabalho)

    def test_filosofia_e_opcional(self):
        perfil = PerfilUsuario(username='makis', cargo='Dev')
        perfil.set_password('senha123')
        perfil.full_clean()  # não deve levantar, filosofia tem blank=True


class HabilidadeModelTests(TestCase):
    def setUp(self):
        self.perfil = PerfilUsuario.objects.create_user(username='makis', password='senha123')

    def test_criar_habilidade_vinculada_ao_usuario(self):
        habilidade = Habilidade.objects.create(usuario=self.perfil, nome='Python')
        self.assertEqual(habilidade.usuario, self.perfil)
        self.assertIn(habilidade, self.perfil.skills.all())  # related_name='skills'

    def test_categoria_e_nivel_tem_defaults(self):
        habilidade = Habilidade.objects.create(usuario=self.perfil, nome='Python')
        self.assertEqual(habilidade.categoria, 'linguagem')
        self.assertEqual(habilidade.nivel, 2)

    def test_nome_em_branco_falha_validacao(self):
        habilidade = Habilidade(usuario=self.perfil, nome='')
        with self.assertRaises(ValidationError):
            habilidade.full_clean()

    def test_usuario_obrigatorio(self):
        habilidade = Habilidade(nome='Python')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                habilidade.save()

    def test_deletar_usuario_apaga_habilidades_em_cascata(self):
        Habilidade.objects.create(usuario=self.perfil, nome='Python')
        Habilidade.objects.create(usuario=self.perfil, nome='Django')
        self.assertEqual(Habilidade.objects.count(), 2)
        self.perfil.delete()
        self.assertEqual(Habilidade.objects.count(), 0)

    def test_ordering_por_categoria_nivel_desc_nome(self):
        Habilidade.objects.create(usuario=self.perfil, nome='MySQL', categoria='banco', nivel=1)
        Habilidade.objects.create(usuario=self.perfil, nome='AWS', categoria='cloud', nivel=3)
        Habilidade.objects.create(usuario=self.perfil, nome='Python', categoria='linguagem', nivel=3)
        Habilidade.objects.create(usuario=self.perfil, nome='Django', categoria='linguagem', nivel=2)
        nomes = list(Habilidade.objects.values_list('nome', flat=True))
        self.assertEqual(nomes, ['MySQL', 'AWS', 'Python', 'Django'])

    def test_str_representation(self):
        habilidade = Habilidade.objects.create(usuario=self.perfil, nome='Python', nivel=3)
        self.assertEqual(str(habilidade), 'Python (Domino bem)')
