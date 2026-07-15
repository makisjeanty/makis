from django.contrib.sitemaps import Sitemap

from .models import Projeto


class ProjetoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Projeto.objects.filter(publico=True)

    def lastmod(self, obj):
        return obj.data_atualizacao

    def location(self, obj):
        return f'/portfolio/{obj.slug}/'
