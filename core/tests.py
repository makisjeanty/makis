import json

from django.test import Client, TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_retorna_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_usa_template_correto(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_home_contexto_basico(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['site_name'], 'Makis Digital')


class RobotsTxtTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt_retorna_200_texto_plano(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')

    def test_robots_txt_referencia_sitemap(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertIn(b'Sitemap:', response.content)
        self.assertIn(b'/sitemap.xml', response.content)

    def test_robots_txt_bloqueia_admin(self):
        from decouple import config
        response = self.client.get(reverse('robots_txt'))
        admin_url = config('ADMIN_URL', default='gestao-dmh8g6skcx')
        self.assertIn(f'Disallow: /{admin_url}/'.encode(), response.content)


class SolicitarOrcamentoTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_solicitar_orcamento_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('solicitar_orcamento'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/solicitar_orcamento.html')


    def test_solicitar_orcamento_post_valido(self):
        from core.testing_helpers import antispam_ok

        data = {
            'nome': 'Empresa Teste',
            'email': 'contato@teste.com',
            'descricao': 'Necessito de um sistema Django.',
            **antispam_ok(),
        }
        response = self.client.post(reverse('solicitar_orcamento'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['enviado'])

    def test_produto_digital_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('produto_digital'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/produto_digital.html')


class MonitoriaTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin_test', password='senha_segura_123', email='admin@test.com'
        )
        self.user_comum = User.objects.create_user(
            username='user_comum', password='senha_segura_123'
        )

    def _login_superuser(self):
        self.client.login(username='admin_test', password='senha_segura_123')

    def test_painel_monitoria_requer_login(self):
        """Anônimo é redirecionado para o login."""
        resp = self.client.get(reverse('painel_monitoria'))
        self.assertIn(resp.status_code, [301, 302])

    def test_painel_monitoria_bloqueia_usuario_comum(self):
        """Usuário autenticado mas não-superuser recebe 403."""
        self.client.login(username='user_comum', password='senha_segura_123')
        resp = self.client.get(reverse('painel_monitoria'))
        self.assertEqual(resp.status_code, 403)

    def test_painel_monitoria_ok_para_superuser(self):
        """Superuser acessa o painel com sucesso."""
        self._login_superuser()
        resp = self.client.get(reverse('painel_monitoria'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/monitoria.html')

    def test_api_monitoria_retorna_json(self):
        """API JSON retorna estrutura válida para superuser."""
        self._login_superuser()
        resp = self.client.get(reverse('api_monitoria'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/json')
        data = resp.json()
        self.assertIn('compras_hoje', data)
        self.assertIn('banco_ok', data)
        self.assertIn('redis_ok', data)

    def test_webhook_kiwify_token_invalido_retorna_403(self):
        """Webhook com token errado é bloqueado."""
        from unittest.mock import patch
        with patch('core.views.KIWIFY_TOKEN', 'token-real-secreto'):
            resp = self.client.post(
                reverse('webhook_kiwify') + '?token=token_errado',
                data='{}',
                content_type='application/json',
            )
        self.assertEqual(resp.status_code, 403)

    def test_webhook_kiwify_salva_compra(self):
        """Webhook com token válido cria um registro de Compra."""
        from core.models import Compra
        from unittest.mock import patch
        from decimal import Decimal

        payload = {
            'order_id': 'kiwify-order-001',
            'order_status': 'paid',
            'Customer': {'full_name': 'João Teste', 'email': 'joao@teste.com'},
            'Product': {'name': 'Kit Dev Pro'},
            'order_value': 9700,
        }
        with patch('core.views.KIWIFY_TOKEN', 'dev-token-local-123'):
            resp = self.client.post(
                reverse('webhook_kiwify') + '?token=dev-token-local-123',
                data=json.dumps(payload),
                content_type='application/json',
            )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['ok'])
        compra = Compra.objects.get(referencia_externa='kiwify-order-001')
        self.assertEqual(compra.status, 'aprovada')
        self.assertEqual(compra.comprador_nome, 'João Teste')
        self.assertEqual(compra.valor, Decimal('97.00'))

    def test_webhook_kiwify_evita_duplicata(self):
        """Segundo webhook com mesmo order_id não cria duplicata."""
        from core.models import Compra
        from unittest.mock import patch

        Compra.objects.create(
            produto='Kit Dev Pro',
            comprador_nome='Já Existe',
            comprador_email='existe@teste.com',
            status='aprovada',
            plataforma='kiwify',
            referencia_externa='order-duplicado-001',
        )
        payload = {
            'order_id': 'order-duplicado-001',
            'order_status': 'paid',
            'Customer': {'full_name': 'Outro', 'email': 'outro@teste.com'},
            'Product': {'name': 'Kit Dev Pro'},
            'order_value': 9700,
        }
        with patch('core.views.KIWIFY_TOKEN', 'dev-token-local-123'):
            resp = self.client.post(
                reverse('webhook_kiwify') + '?token=dev-token-local-123',
                data=json.dumps(payload),
                content_type='application/json',
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Compra.objects.filter(referencia_externa='order-duplicado-001').count(), 1)

    def test_webhook_kiwify_sem_token_configurado_falha_fechado(self):
        """Sem KIWIFY_TOKEN configurado no servidor, o webhook rejeita tudo (503), em vez de aceitar qualquer requisição."""
        from unittest.mock import patch

        with patch('core.views.KIWIFY_TOKEN', ''):
            resp = self.client.post(
                reverse('webhook_kiwify'),
                data='{}',
                content_type='application/json',
            )
        self.assertEqual(resp.status_code, 503)
