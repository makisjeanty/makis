from django.test import Client, TestCase
from django.urls import reverse


class UtilidadesViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_lista_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/lista.html')

    def test_gerador_senha_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:gerador_senha'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/gerador_senha.html')

    def test_validador_documento_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:validador_documento'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/validador_documento.html')

    def test_formatador_json_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:formatador_json'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/formatador_json.html')

    def test_conversor_base64_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:conversor_base64'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/conversor_base64.html')
