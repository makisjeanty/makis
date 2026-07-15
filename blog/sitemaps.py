from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Post.objects.filter(publicado=True)

    def lastmod(self, obj):
        return obj.data_atualizacao

    def location(self, obj):
        return f'/blog/{obj.slug}/'
