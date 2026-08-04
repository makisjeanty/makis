"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

from core.views import (
    home,
    health_check,
    solicitar_orcamento,
    produto_digital,
    robots_txt,
    page_not_found,
    server_error,
    painel_monitoria,
    api_monitoria,
    moderar_comentario,
    webhook_kiwify,
)

from blog.sitemaps import PostSitemap
from comunidade.sitemaps import TopicoSitemap
from core.sitemaps import StaticViewSitemap
from portfolio.sitemaps import ProjetoSitemap

# URL secreta do admin (vinda do .env) - não expõe o caminho padrão /admin/
ADMIN_URL = config('ADMIN_URL', default='gestao-dmh8g6skcx')

# URL do painel de monitoria (pode ser ofuscada via env)
MONITORIA_URL = config('MONITORIA_URL', default='monitoria')

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

urlpatterns = [
    path('', home, name='home'),
    path('health/', health_check, name='health_check'),
    path('solicitar-orcamento/', solicitar_orcamento, name='solicitar_orcamento'),
    # Monitoria
    path(f'{MONITORIA_URL}/', painel_monitoria, name='painel_monitoria'),
    path(f'{MONITORIA_URL}/api/', api_monitoria, name='api_monitoria'),
    path(f'{MONITORIA_URL}/moderar/<int:comentario_id>/', moderar_comentario, name='moderar_comentario'),
    # Webhook de pagamento (Kiwify)
    path('api/webhook/kiwify/', webhook_kiwify, name='webhook_kiwify'),
    path('produtos/kit-dev-pro/', produto_digital, name='produto_digital'),
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
    path('cursos/', include('cursos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Não expor stack trace nem caminhos internos em produção
handler404 = page_not_found
handler500 = server_error