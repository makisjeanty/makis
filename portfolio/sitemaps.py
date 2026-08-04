from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ProjetoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        from .models import Projeto
        return Projeto.objects.filter(publico=True)

    def lastmod(self, obj):
        return obj.data_atualizacao

    def location(self, obj):
        return reverse('portfolio:detalhe', args=[obj.slug])
