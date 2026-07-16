import time

from django.core import signing
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from core.antispam import SALT

from .models import Resposta, Topico


def antispam_ok():
    """Campos que fazem o formulário parecer preenchido por um humano:
    honeypot vazio + timestamp assinado de alguns segundos atrás."""
    return {'website': '', 'ts_form': signing.dumps(time.time() - 5, salt=SALT)}


class ComunidadeViewsTests(TestCase):
    def setUp(self):
        cache.clear()  # isola o contador de rate-limit entre testes
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
            **antispam_ok(),
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


class ComunidadeRateLimitTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.topico = Topico.objects.create(
            titulo='Tópico para respostas', autor_nome='V', autor_email='v@example.com',
            conteudo='c', aprovado=True,
        )

    def _payload_topico(self, i):
        return {
            'titulo': f'Tópico {i}', 'autor_nome': 'V', 'autor_email': f'v{i}@example.com',
            'conteudo': 'conteúdo',
            **antispam_ok(),
        }

    def test_criacao_de_topico_e_bloqueada_apos_5_por_minuto(self):
        url = reverse('comunidade:lista')
        for i in range(5):
            response = self.client.post(url, self._payload_topico(i))
            self.assertEqual(response.status_code, 302, f'requisição {i} deveria ter passado')

        response = self.client.post(url, self._payload_topico(5))
        self.assertEqual(response.status_code, 200)  # form re-renderizado, sem redirect
        self.assertFalse(Topico.objects.filter(titulo='Tópico 5').exists())
        mensagens = [str(m) for m in response.context['messages']]
        self.assertTrue(any('Muitas publicações' in m for m in mensagens))

    def test_criacao_de_resposta_e_bloqueada_apos_10_por_minuto(self):
        url = reverse('comunidade:detalhe', args=[self.topico.slug])
        for i in range(10):
            response = self.client.post(url, {
                'autor_nome': 'V', 'autor_email': f'v{i}@example.com', 'conteudo': 'c',
                **antispam_ok(),
            })
            self.assertEqual(response.status_code, 302, f'requisição {i} deveria ter passado')

        response = self.client.post(url, {
            'autor_nome': 'V', 'autor_email': 'v10@example.com', 'conteudo': 'c',
            **antispam_ok(),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Resposta.objects.filter(autor_email='v10@example.com').count(), 0)


class ComunidadeAntiSpamTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_honeypot_preenchido_bloqueia_criacao_de_topico(self):
        response = self.client.post(reverse('comunidade:lista'), {
            'titulo': 'Tópico de bot', 'autor_nome': 'Bot', 'autor_email': 'bot@example.com',
            'conteudo': 'spam', 'website': 'http://spam.example.com',
            'ts_form': signing.dumps(time.time() - 5, salt=SALT),
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topico.objects.filter(titulo='Tópico de bot').exists())

    def test_envio_rapido_demais_bloqueia_criacao_de_topico(self):
        response = self.client.post(reverse('comunidade:lista'), {
            'titulo': 'Tópico rápido', 'autor_nome': 'Bot', 'autor_email': 'bot2@example.com',
            'conteudo': 'spam', 'website': '',
            'ts_form': signing.dumps(time.time(), salt=SALT),  # "agora", sem tempo de preencher
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topico.objects.filter(titulo='Tópico rápido').exists())

    def test_timestamp_ausente_ou_adulterado_bloqueia(self):
        response = self.client.post(reverse('comunidade:lista'), {
            'titulo': 'Tópico sem timestamp', 'autor_nome': 'Bot', 'autor_email': 'bot3@example.com',
            'conteudo': 'spam', 'website': '', 'ts_form': 'valor-forjado-invalido',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topico.objects.filter(titulo='Tópico sem timestamp').exists())

    def test_envio_normal_com_antispam_ok_e_aceito(self):
        response = self.client.post(reverse('comunidade:lista'), {
            'titulo': 'Tópico legítimo', 'autor_nome': 'Visitante', 'autor_email': 'v@example.com',
            'conteudo': 'conteúdo real', **antispam_ok(),
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topico.objects.filter(titulo='Tópico legítimo').exists())
