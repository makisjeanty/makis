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
