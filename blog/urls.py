from django.urls import path

from . import views
from .feeds import PostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.lista_posts, name='lista'),
    path('rss/', PostsFeed(), name='rss'),
    path('categories/', views.lista_categorias, name='categorias'),
    path('categoria/<slug:slug>/', views.posts_por_categoria, name='categoria'),
    path('<slug:slug>/', views.detalhe_post, name='detalhe'),
]
