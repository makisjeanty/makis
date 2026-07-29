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

    def test_gerador_hash_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:gerador_hash'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/gerador_hash.html')

    def test_gerador_uuid_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:gerador_uuid'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/gerador_uuid.html')

    def test_contador_texto_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:contador_texto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/contador_texto.html')

    def test_conversor_timestamp_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:conversor_timestamp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/conversor_timestamp.html')

    def test_minificador_codigo_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:minificador_codigo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/minificador_codigo.html')

    def test_calculadora_tokens_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:calculadora_tokens'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/calculadora_tokens.html')

    def test_gerador_prompts_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:gerador_prompts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/gerador_prompts.html')

    def test_json_para_markdown_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:json_para_markdown'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/json_para_markdown.html')

    def test_extrator_codigo_ia_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:extrator_codigo_ia'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/extrator_codigo_ia.html')

    def test_gerador_readme_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:gerador_readme'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/gerador_readme.html')

    def test_seguranca_owasp_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:seguranca_owasp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/seguranca_owasp.html')

    def test_agente_orientador_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:agente_orientador'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/agente_orientador.html')

    def test_seo_especialista_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:seo_especialista'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/seo_especialista.html')

    def test_achador_oportunidades_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:achador_oportunidades'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/achador_oportunidades.html')

    def test_mini_curso_retorna_200_e_template_correto(self):
        response = self.client.get(reverse('utilidades:mini_curso'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utilidades/mini_curso.html')




