from django.test import Client, TestCase
from django.urls import reverse

from .consumers import SALA_PADRAO
from .models import Mensagem


class ChatViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sala_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('chat:sala'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/sala.html')

    def test_sala_sem_mensagens_contexto_vazio(self):
        response = self.client.get(reverse('chat:sala'))
        self.assertEqual(list(response.context['mensagens']), [])

    def test_sala_mostra_mensagens_da_sala_padrao_em_ordem_cronologica(self):
        m1 = Mensagem.objects.create(sala=SALA_PADRAO, nome='Ana', texto='primeira')
        m2 = Mensagem.objects.create(sala=SALA_PADRAO, nome='Bia', texto='segunda')
        response = self.client.get(reverse('chat:sala'))
        self.assertEqual(list(response.context['mensagens']), [m1, m2])

    def test_sala_ignora_mensagens_de_outras_salas(self):
        Mensagem.objects.create(sala='outra-sala', nome='Ana', texto='não deve aparecer')
        response = self.client.get(reverse('chat:sala'))
        self.assertEqual(list(response.context['mensagens']), [])

    def test_sala_limita_as_ultimas_50_mensagens(self):
        for i in range(55):
            Mensagem.objects.create(sala=SALA_PADRAO, nome='Ana', texto=f'mensagem {i}')
        response = self.client.get(reverse('chat:sala'))
        mensagens = list(response.context['mensagens'])
        self.assertEqual(len(mensagens), 50)
        # deve manter as 50 mais recentes, em ordem cronológica
        self.assertEqual(mensagens[0].texto, 'mensagem 5')
        self.assertEqual(mensagens[-1].texto, 'mensagem 54')
