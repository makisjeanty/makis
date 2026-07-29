from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return [
            'home', 'solicitar_orcamento', 'produto_digital', 'portfolio:lista', 'portfolio:cases', 'blog:lista', 'blog:categorias', 'blog:gerenciador_ia', 'accounts:sobre',



            'utilidades:lista', 'utilidades:gerador_senha', 'utilidades:validador_documento',
            'utilidades:formatador_json', 'utilidades:conversor_base64', 'utilidades:gerador_hash',
            'utilidades:gerador_uuid', 'utilidades:contador_texto', 'utilidades:conversor_timestamp',
            'utilidades:minificador_codigo', 'utilidades:calculadora_tokens', 'utilidades:gerador_prompts',
            'utilidades:json_para_markdown', 'utilidades:extrator_codigo_ia', 'utilidades:gerador_readme',
            'utilidades:seguranca_owasp', 'utilidades:agente_orientador', 'utilidades:seo_especialista',
            'utilidades:achador_oportunidades', 'utilidades:mini_curso', 'comunidade:lista', 'chat:sala',








        ]

    def location(self, item):
        return reverse(item)
