from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        from .models import Post
        return Post.objects.filter(publicado=True)

    def lastmod(self, obj):
        return obj.data_atualizacao

    def location(self, obj):
        return reverse('blog:detalhe', args=[obj.slug])
