from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class TopicoSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        from .models import Topico
        return Topico.objects.filter(aprovado=True)

    def lastmod(self, obj):
        return obj.data_criacao

    def location(self, obj):
        return reverse('comunidade:detalhe', args=[obj.slug])
