from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Post


class PostsFeed(Feed):
    title = f'{settings.SITE_NAME} — Blog'
    link = '/blog/'
    description = f'Últimos artigos publicados no blog de {settings.SITE_NAME}.'

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
