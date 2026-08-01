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
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.core.cache import cache
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from core.antispam import bloquear_submissao_suspeita, gerar_timestamp_assinado
from core.views_monitoria import painel_monitoria, api_monitoria, moderar_comentario, webhook_kiwify

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


# Endpoint de checagem de saúde com validação de dependências (sem expor segredos)
def health_check(request):
    db_ok = True
    redis_ok = True
    storage_ok = True

    try:
        connection.ensure_connection()
    except Exception:
        db_ok = False

    try:
        cache.set('_health_check', '1', 5)
        redis_ok = (cache.get('_health_check') == '1')
    except Exception:
        redis_ok = False

    status_code = 200 if (db_ok and redis_ok and storage_ok) else 503
    return JsonResponse({
        'status': 'ok' if status_code == 200 else 'degraded',
        'database': 'ok' if db_ok else 'error',
        'redis': 'ok' if redis_ok else 'error',
        'storage': 'ok' if storage_ok else 'error',
    }, status=status_code)


# View de solicitação de orçamento & consultoria
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def solicitar_orcamento(request):
    enviado = False

    if request.method == 'POST' and not bloquear_submissao_suspeita(request):
        enviado = True

    return render(request, 'core/solicitar_orcamento.html', {
        'antispam_ts': gerar_timestamp_assinado(),
        'enviado': enviado,
    })


# View da página de vendas do produto digital
def produto_digital(request):
    return render(request, 'core/produto_digital.html')


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

# URL do painel de monitoria (pode ser ofuscada via env)
MONITORIA_URL = config('MONITORIA_URL', default='monitoria')

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