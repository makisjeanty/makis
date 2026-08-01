from django.test import Client, TestCase
from django.urls import reverse

from .models import Curso, Etapa, Licao, Modulo


class CursoModelTests(TestCase):
    def _criar_curso(self, **kwargs):
        defaults = dict(
            titulo='Python para Iniciantes',
            descricao='Aprenda o básico de Python.',
        )
        defaults.update(kwargs)
        return Curso.objects.create(**defaults)

    def test_criar_curso_basico(self):
        curso = self._criar_curso()
        self.assertEqual(Curso.objects.count(), 1)
        self.assertEqual(curso.icone, '🐍')  # default
        self.assertEqual(curso.nivel, 'iniciante')  # default
        self.assertTrue(curso.ativo)  # default

    def test_slug_autogerado_a_partir_do_titulo(self):
        curso = self._criar_curso(titulo='Django Avançado')
        self.assertEqual(curso.slug, 'django-avancado')

    def test_slug_explicito_nao_e_sobrescrito(self):
        curso = self._criar_curso(titulo='Curso X', slug='slug-customizado')
        self.assertEqual(curso.slug, 'slug-customizado')

    def test_str_inclui_icone_e_titulo(self):
        curso = self._criar_curso(titulo='Engenharia de IA', icone='🤖')
        self.assertEqual(str(curso), '🤖 Engenharia de IA')

    def test_ordering_por_ordem(self):
        c2 = self._criar_curso(titulo='Segundo', slug='segundo', ordem=2)
        c1 = self._criar_curso(titulo='Primeiro', slug='primeiro', ordem=1)
        self.assertEqual(list(Curso.objects.all()), [c1, c2])


class ModuloModelTests(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(titulo='Python para Iniciantes', descricao='desc')

    def test_str_inclui_curso_e_titulo(self):
        modulo = Modulo.objects.create(curso=self.curso, titulo='Variáveis')
        self.assertEqual(str(modulo), 'Python para Iniciantes - Variáveis')

    def test_modulo_relacionado_ao_curso(self):
        modulo = Modulo.objects.create(curso=self.curso, titulo='Variáveis')
        self.assertIn(modulo, self.curso.modulos.all())  # related_name='modulos'

    def test_deletar_curso_apaga_modulos_em_cascata(self):
        Modulo.objects.create(curso=self.curso, titulo='Módulo 1')
        Modulo.objects.create(curso=self.curso, titulo='Módulo 2')
        self.assertEqual(Modulo.objects.count(), 2)
        self.curso.delete()
        self.assertEqual(Modulo.objects.count(), 0)

    def test_ordering_por_ordem(self):
        m2 = Modulo.objects.create(curso=self.curso, titulo='Segundo', ordem=2)
        m1 = Modulo.objects.create(curso=self.curso, titulo='Primeiro', ordem=1)
        self.assertEqual(list(Modulo.objects.all()), [m1, m2])


class LicaoModelTests(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(titulo='Python para Iniciantes', descricao='desc')
        self.modulo = Modulo.objects.create(curso=self.curso, titulo='Variáveis')

    def test_str_inclui_modulo_e_titulo(self):
        licao = Licao.objects.create(modulo=self.modulo, titulo='O que é uma variável?')
        self.assertEqual(str(licao), 'Variáveis -> O que é uma variável?')

    def test_licao_relacionada_ao_modulo(self):
        licao = Licao.objects.create(modulo=self.modulo, titulo='Lição 1')
        self.assertIn(licao, self.modulo.licoes.all())  # related_name='licoes'

    def test_duracao_minutos_default(self):
        licao = Licao.objects.create(modulo=self.modulo, titulo='Lição 1')
        self.assertEqual(licao.duracao_minutos, 5)

    def test_deletar_modulo_apaga_licoes_em_cascata(self):
        Licao.objects.create(modulo=self.modulo, titulo='Lição 1')
        Licao.objects.create(modulo=self.modulo, titulo='Lição 2')
        self.assertEqual(Licao.objects.count(), 2)
        self.modulo.delete()
        self.assertEqual(Licao.objects.count(), 0)

    def test_ordering_por_ordem(self):
        l2 = Licao.objects.create(modulo=self.modulo, titulo='Segunda', ordem=2)
        l1 = Licao.objects.create(modulo=self.modulo, titulo='Primeira', ordem=1)
        self.assertEqual(list(Licao.objects.all()), [l1, l2])


class EtapaModelTests(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(titulo='Python para Iniciantes', descricao='desc')
        self.modulo = Modulo.objects.create(curso=self.curso, titulo='Variáveis')
        self.licao = Licao.objects.create(modulo=self.modulo, titulo='O que é uma variável?')

    def test_tipo_default_e_slide(self):
        etapa = Etapa.objects.create(licao=self.licao)
        self.assertEqual(etapa.tipo, 'slide')

    def test_opcoes_json_default_e_lista_vazia(self):
        etapa = Etapa.objects.create(licao=self.licao)
        self.assertEqual(etapa.opcoes_json, [])

    def test_opcoes_json_armazena_lista_de_strings(self):
        etapa = Etapa.objects.create(
            licao=self.licao, tipo='quiz',
            pergunta='Qual é o tipo correto?', opcoes_json=['int', 'str', 'float'],
            resposta_correta='str',
        )
        etapa.refresh_from_db()
        self.assertEqual(etapa.opcoes_json, ['int', 'str', 'float'])

    def test_str_inclui_licao_ordem_e_tipo_display(self):
        etapa = Etapa.objects.create(licao=self.licao, ordem=1, tipo='quiz')
        self.assertEqual(str(etapa), f"Lição {self.licao.id} - Etapa 1 (Múltipla Escolha (Quiz))")

    def test_etapa_relacionada_a_licao(self):
        etapa = Etapa.objects.create(licao=self.licao)
        self.assertIn(etapa, self.licao.etapas.all())  # related_name='etapas'

    def test_deletar_licao_apaga_etapas_em_cascata(self):
        Etapa.objects.create(licao=self.licao, ordem=1)
        Etapa.objects.create(licao=self.licao, ordem=2)
        self.assertEqual(Etapa.objects.count(), 2)
        self.licao.delete()
        self.assertEqual(Etapa.objects.count(), 0)

    def test_ordering_por_ordem(self):
        e2 = Etapa.objects.create(licao=self.licao, ordem=2)
        e1 = Etapa.objects.create(licao=self.licao, ordem=1)
        self.assertEqual(list(Etapa.objects.all()), [e1, e2])


class CursosViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso_ativo = Curso.objects.create(
            titulo='Python para Iniciantes', descricao='desc', slug='python-para-iniciantes', ativo=True,
        )
        self.curso_inativo = Curso.objects.create(
            titulo='Curso Rascunho', descricao='desc', slug='curso-rascunho', ativo=False,
        )
        self.modulo = Modulo.objects.create(curso=self.curso_ativo, titulo='Variáveis')
        self.licao = Licao.objects.create(modulo=self.modulo, titulo='O que é uma variável?')
        self.etapa = Etapa.objects.create(licao=self.licao, ordem=1, tipo='slide', titulo='Introdução')

    def test_lista_cursos_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('cursos:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/lista.html')

    def test_lista_cursos_mostra_apenas_ativos(self):
        response = self.client.get(reverse('cursos:lista'))
        cursos = list(response.context['cursos'])
        self.assertIn(self.curso_ativo, cursos)
        self.assertNotIn(self.curso_inativo, cursos)

    def test_trilha_curso_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('cursos:trilha', args=[self.curso_ativo.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/trilha.html')
        self.assertEqual(response.context['curso'], self.curso_ativo)
        self.assertIn(self.modulo, list(response.context['modulos']))

    def test_trilha_curso_inativo_retorna_404(self):
        response = self.client.get(reverse('cursos:trilha', args=[self.curso_inativo.slug]))
        self.assertEqual(response.status_code, 404)

    def test_trilha_curso_inexistente_retorna_404(self):
        response = self.client.get(reverse('cursos:trilha', args=['slug-que-nao-existe']))
        self.assertEqual(response.status_code, 404)

    def test_executar_licao_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('cursos:licao', args=[self.licao.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/licao.html')
        self.assertEqual(response.context['licao'], self.licao)
        self.assertIn(self.etapa, list(response.context['etapas']))

    def test_executar_licao_inexistente_retorna_404(self):
        response = self.client.get(reverse('cursos:licao', args=[999999]))
        self.assertEqual(response.status_code, 404)
