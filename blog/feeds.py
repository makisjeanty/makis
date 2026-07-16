from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Post


class PostsFeed(Feed):
    title = 'Makis Digital — Estudos'
    link = '/blog/'
    description = 'Últimos artigos publicados na trilha de estudos da Makis Digital.'

    def items(self):
        return Post.objects.filter(publicado=True).order_by('-data_publicacao')[:20]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return item.resumo

    def item_link(self, item):
        return reverse('blog:detalhe', args=[item.slug])

    def item_pubdate(self, item):
        return item.data_publicacao

    def item_author_name(self, item):
        return item.autor.get_full_name() or item.autor.username
