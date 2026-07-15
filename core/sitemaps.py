from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return [
            'home', 'portfolio:lista', 'portfolio:cases', 'blog:lista', 'blog:categorias', 'accounts:sobre',
            'utilidades:lista', 'utilidades:gerador_senha', 'utilidades:validador_documento',
            'utilidades:formatador_json', 'utilidades:conversor_base64', 'comunidade:lista', 'chat:sala',
        ]

    def location(self, item):
        return reverse(item)
