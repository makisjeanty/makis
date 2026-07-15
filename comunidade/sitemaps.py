from django.contrib.sitemaps import Sitemap

from .models import Topico


class TopicoSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return Topico.objects.filter(aprovado=True)

    def lastmod(self, obj):
        return obj.data_criacao

    def location(self, obj):
        return f'/comunidade/{obj.slug}/'
