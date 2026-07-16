"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from decouple import config
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render

from blog.sitemaps import PostSitemap
from comunidade.sitemaps import TopicoSitemap
from core.sitemaps import StaticViewSitemap
from portfolio.sitemaps import ProjetoSitemap

# URL secreta do admin (vinda do .env) - não expõe o caminho padrão /admin/
ADMIN_URL = config('ADMIN_URL', default='gestao-dmh8g6skcx')

SITEMAPS = {
    'static': StaticViewSitemap,
    'projetos': ProjetoSitemap,
    'posts': PostSitemap,
    'topicos': TopicoSitemap,
}

# Disfarça a identidade do Django no painel
admin.site.site_header = 'Painel Makis'
admin.site.site_title = 'Painel Makis'
admin.site.index_title = 'Gerenciamento'

# View da página inicial
def home(request):
    return render(request, 'home.html', {
        'site_name': 'Makis Digital'
    })


# robots.txt: libera indexação geral, esconde o painel admin (mesmo já tendo URL
# ofuscada) e aponta para o sitemap
def robots_txt(request):
    linhas = [
        'User-agent: *',
        f'Disallow: /{ADMIN_URL}/',
        '',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(linhas), content_type='text/plain')


# Tratamento de erros sem expor detalhes técnicos (modo produção)
def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)

urlpatterns = [
    path('', home, name='home'),
    path(f'{ADMIN_URL}/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    # Páginas públicas das apps
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    path('sobre/', include('accounts.urls')),
    path('utilidades/', include('utilidades.urls')),
    path('comunidade/', include('comunidade.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Não expor stack trace nem caminhos internos em produção
handler404 = page_not_found
handler500 = server_error