from django.test import Client, TestCase
from django.urls import reverse

from .models import Resposta, Topico


class ComunidadeViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.topico_aprovado = Topico.objects.create(
            titulo='Como estruturar um projeto Django?',
            autor_nome='Visitante',
            autor_email='v@example.com',
            conteudo='Conteúdo do tópico.',
            aprovado=True,
        )
        self.topico_nao_aprovado = Topico.objects.create(
            titulo='Tópico Escondido',
            autor_nome='Visitante',
            autor_email='v@example.com',
            conteudo='Conteúdo escondido.',
            aprovado=False,
        )

    def test_lista_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('comunidade:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comunidade/lista.html')

    def test_lista_mostra_apenas_topicos_aprovados(self):
        response = self.client.get(reverse('comunidade:lista'))
        topicos = list(response.context['topicos'])
        self.assertIn(self.topico_aprovado, topicos)
        self.assertNotIn(self.topico_nao_aprovado, topicos)

    def test_lista_contexto_inclui_form(self):
        response = self.client.get(reverse('comunidade:lista'))
        self.assertIn('form', response.context)

    def test_lista_post_cria_topico_e_redireciona(self):
        response = self.client.post(reverse('comunidade:lista'), {
            'titulo': 'Novo Tópico de Teste',
            'autor_nome': 'Visitante',
            'autor_email': 'novo@example.com',
            'conteudo': 'Conteúdo do novo tópico.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topico.objects.filter(titulo='Novo Tópico de Teste').exists())

    def test_detalhe_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('comunidade:detalhe', args=[self.topico_aprovado.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comunidade/detalhe.html')
        self.assertEqual(response.context['topico'], self.topico_aprovado)

    def test_detalhe_topico_nao_aprovado_retorna_404(self):
        response = self.client.get(reverse('comunidade:detalhe', args=[self.topico_nao_aprovado.slug]))
        self.assertEqual(response.status_code, 404)

    def test_detalhe_topico_inexistente_retorna_404(self):
        response = self.client.get(reverse('comunidade:detalhe', args=['slug-que-nao-existe']))
        self.assertEqual(response.status_code, 404)

    def test_detalhe_mostra_apenas_respostas_aprovadas(self):
        resposta_aprovada = Resposta.objects.create(
            topico=self.topico_aprovado, autor_nome='A', autor_email='a@example.com',
            conteudo='resposta aprovada', aprovado=True,
        )
        resposta_escondida = Resposta.objects.create(
            topico=self.topico_aprovado, autor_nome='B', autor_email='b@example.com',
            conteudo='resposta escondida', aprovado=False,
        )
        response = self.client.get(reverse('comunidade:detalhe', args=[self.topico_aprovado.slug]))
        respostas = list(response.context['respostas'])
        self.assertIn(resposta_aprovada, respostas)
        self.assertNotIn(resposta_escondida, respostas)
