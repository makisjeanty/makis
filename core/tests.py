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
