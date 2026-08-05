"""
views.py — Views do app core (Makis Digital)

Seções:
  1. Views públicas  — home, produto_digital, solicitar_orcamento, robots_txt
  2. Utilitários     — health_check, tratamento de erros (404/500)
  3. Monitoria       — painel superuser, API JSON, moderação, webhook Kiwify
"""

import hmac
import json
import logging
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.core.cache import cache, caches
from django.db import connection
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from decouple import config
from django_ratelimit.decorators import ratelimit

from blog.models import Comentario, Post
from chat.models import Mensagem
from comunidade.models import Topico
from core.antispam import bloquear_submissao_suspeita, gerar_timestamp_assinado
from core.models import Compra, LeadOrcamento
from portfolio.models import Projeto

logger = logging.getLogger('django.request')

# URL secreta do admin (vinda do .env)
ADMIN_URL = config('ADMIN_URL', default='gestao-dmh8g6skcx')


# ─────────────────────────────────────────────────────────────
#  1. Views públicas
# ─────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'home.html', {
        'site_name': 'Makis Digital'
    })


def produto_digital(request):
    return render(request, 'core/produto_digital.html')


@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def solicitar_orcamento(request):
    enviado = False

    if request.method == 'POST' and not bloquear_submissao_suspeita(request):
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        whatsapp = request.POST.get('whatsapp', '').strip()
        tipos_projeto = ', '.join(request.POST.getlist('tipo_projeto'))
        prazo = request.POST.get('prazo', '').strip()
        suporte = request.POST.get('suporte', '').strip()
        descricao = request.POST.get('descricao', '').strip()

        if nome and email and descricao:
            LeadOrcamento.objects.create(
                nome=nome,
                email=email,
                whatsapp=whatsapp,
                tipos_projeto=tipos_projeto,
                prazo=prazo,
                suporte=suporte,
                descricao=descricao
            )
            enviado = True

    return render(request, 'core/solicitar_orcamento.html', {
        'antispam_ts': gerar_timestamp_assinado(),
        'enviado': enviado,
    })


def robots_txt(request):
    """robots.txt: libera indexação geral, esconde o painel admin e aponta para o sitemap."""
    linhas = [
        'User-agent: *',
        f'Disallow: /{ADMIN_URL}/',
        '',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(linhas), content_type='text/plain')


# ─────────────────────────────────────────────────────────────
#  2. Utilitários — health check e tratamento de erros
# ─────────────────────────────────────────────────────────────

def health_check(request):
    """Endpoint de checagem de saúde com validação de dependências (sem expor segredos)."""
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


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)


# ─────────────────────────────────────────────────────────────
#  3. Monitoria — painel de administração interno
#
#  Três frentes:
#    a. Vendas      — modelo Compra + webhook Kiwify
#    b. Servidor    — saúde do banco, Redis, contadores
#    c. Moderação   — comentários pendentes, tópicos, chat
#
#  Acesso restrito a superusers via decorador customizado.
# ─────────────────────────────────────────────────────────────

def superuser_required(view_func):
    """Redireciona para login se não autenticado; retorna 403 se não é superuser."""
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden('Acesso negado.')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ── Helpers de saúde do servidor ──

def _checar_banco():
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return True
    except Exception:
        return False


def _checar_redis():
    try:
        c = caches['default']
        c.set('_monitoria_ping', '1', timeout=5)
        return c.get('_monitoria_ping') == '1'
    except Exception:
        return False


def _contadores():
    agora = timezone.now()
    hoje = agora.date()
    semana_atras = agora - timedelta(days=7)
    mes_atras = agora - timedelta(days=30)

    # Vendas
    compras_total = Compra.objects.filter(status='aprovada').count()
    compras_hoje = Compra.objects.filter(status='aprovada', criado_em__date=hoje).count()
    compras_semana = Compra.objects.filter(status='aprovada', criado_em__gte=semana_atras).count()
    compras_mes = Compra.objects.filter(status='aprovada', criado_em__gte=mes_atras).count()

    receita_total = Compra.objects.filter(status='aprovada').values_list('valor', flat=True)
    receita_total = sum(v for v in receita_total if v) or Decimal('0')

    receita_mes = Compra.objects.filter(status='aprovada', criado_em__gte=mes_atras).values_list('valor', flat=True)
    receita_mes = sum(v for v in receita_mes if v) or Decimal('0')

    # Conteúdo
    comentarios_pendentes = Comentario.objects.filter(aprovado=False).count()
    total_posts = Post.objects.filter(publicado=True).count()
    total_projetos = Projeto.objects.count()
    total_topicos = Topico.objects.count()
    mensagens_24h = Mensagem.objects.filter(criado_em__gte=agora - timedelta(hours=24)).count()

    return {
        'compras_total': compras_total,
        'compras_hoje': compras_hoje,
        'compras_semana': compras_semana,
        'compras_mes': compras_mes,
        'receita_total': float(receita_total),
        'receita_mes': float(receita_mes),
        'comentarios_pendentes': comentarios_pendentes,
        'total_posts': total_posts,
        'total_projetos': total_projetos,
        'total_topicos': total_topicos,
        'mensagens_24h': mensagens_24h,
    }


# ── Views do painel ──

@superuser_required
def painel_monitoria(request):
    agora = timezone.now()
    mes_atras = agora - timedelta(days=30)

    # ── Aba 1: Vendas ──
    ultimas_compras = Compra.objects.order_by('-criado_em')[:15]

    # Dados para gráfico de barras (últimos 7 dias)
    grafico_labels = []
    grafico_valores = []
    for i in range(6, -1, -1):
        dia = (agora - timedelta(days=i)).date()
        qtd = Compra.objects.filter(status='aprovada', criado_em__date=dia).count()
        grafico_labels.append(dia.strftime('%d/%m'))
        grafico_valores.append(qtd)

    # ── Aba 2: Servidor ──
    banco_ok = _checar_banco()
    redis_ok = _checar_redis()

    # ── Aba 3: Moderação ──
    comentarios_pendentes = (
        Comentario.objects
        .filter(aprovado=False)
        .select_related('post')
        .order_by('-data_criacao')[:20]
    )
    topicos_ocultos = (
        Topico.objects
        .filter(aprovado=False)
        .order_by('-data_criacao')[:10]
    )
    mensagens_recentes = (
        Mensagem.objects
        .filter(criado_em__gte=agora - timedelta(hours=24))
        .order_by('-criado_em')[:30]
    )

    contadores = _contadores()

    context = {
        'ultimas_compras': ultimas_compras,
        'grafico_labels': json.dumps(grafico_labels),
        'grafico_valores': json.dumps(grafico_valores),
        'banco_ok': banco_ok,
        'redis_ok': redis_ok,
        'comentarios_pendentes': comentarios_pendentes,
        'topicos_ocultos': topicos_ocultos,
        'mensagens_recentes': mensagens_recentes,
        **contadores,
    }
    return render(request, 'core/monitoria.html', context)


@superuser_required
@require_GET
def api_monitoria(request):
    """API JSON — dados em tempo real para o painel (fetch AJAX)."""
    dados = _contadores()
    dados['banco_ok'] = _checar_banco()
    dados['redis_ok'] = _checar_redis()
    dados['timestamp'] = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')
    return JsonResponse(dados)


@superuser_required
@require_POST
def moderar_comentario(request, comentario_id):
    """AJAX inline — aprovar/rejeitar comentário sem sair do painel."""
    acao = request.POST.get('acao')  # 'aprovar' ou 'rejeitar'
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    if acao == 'aprovar':
        comentario.aprovado = True
        comentario.save()
        return JsonResponse({'ok': True, 'mensagem': 'Comentário aprovado.'})
    elif acao == 'rejeitar':
        comentario.delete()
        return JsonResponse({'ok': True, 'mensagem': 'Comentário removido.'})

    return JsonResponse({'ok': False, 'mensagem': 'Ação inválida.'}, status=400)


# ── Webhook Kiwify ──

KIWIFY_TOKEN = config('KIWIFY_TOKEN', default='')


@csrf_exempt
@require_POST
def webhook_kiwify(request):
    """
    Kiwify envia um POST com token de verificação no header ou query param.
    Formato do payload JSON:
      {
        "order_id": "abc123",
        "order_status": "paid",  # paid | refunded | chargedback
        "Customer": {"full_name": "...", "email": "..."},
        "Product": {"name": "..."},
        "order_value": 9700,   # em centavos
        ...
      }
    Documentação: https://docs.kiwify.com.br/webhooks
    """
    # Falha fechado: sem token configurado, nenhum payload é aceito (em vez de
    # aceitar qualquer POST sem verificação).
    if not KIWIFY_TOKEN:
        logger.error('Webhook Kiwify chamado sem KIWIFY_TOKEN configurado — requisição rejeitada.')
        return JsonResponse({'erro': 'Webhook não configurado.'}, status=503)

    # Valida token de segurança (query param ou header) em tempo constante
    token_recebido = (
        request.GET.get('token', '')
        or request.headers.get('X-Kiwify-Token', '')
    )
    if not hmac.compare_digest(token_recebido, KIWIFY_TOKEN):
        logger.warning('Webhook Kiwify com token inválido recebido.')
        return JsonResponse({'erro': 'Token inválido.'}, status=403)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Payload inválido.'}, status=400)

    order_status = payload.get('order_status', '')
    status_map = {
        'paid': 'aprovada',
        'refunded': 'reembolsada',
        'chargedback': 'cancelada',
    }
    status = status_map.get(order_status, 'pendente')

    customer = payload.get('Customer') or {}
    product = payload.get('Product') or {}
    order_id = payload.get('order_id') or None

    # Valor em centavos → reais
    valor_centavos = payload.get('order_value')
    try:
        valor = Decimal(valor_centavos) / 100 if valor_centavos is not None else None
    except (InvalidOperation, TypeError, ValueError):
        return JsonResponse({'erro': 'order_value inválido.'}, status=400)

    defaults = {
        'produto': str(product.get('name', 'Kit Dev Pro'))[:200],
        'comprador_nome': str(customer.get('full_name', '—'))[:200],
        'comprador_email': str(customer.get('email', ''))[:254],
        'valor': valor,
        'status': status,
        'plataforma': 'kiwify',
    }

    if order_id:
        # get_or_create trata a corrida de webhooks concorrentes/retries: o
        # unique= em referencia_externa faz o segundo INSERT falhar e o
        # Django recupera a linha já criada pelo primeiro, em vez de duplicar.
        compra, criada = Compra.objects.get_or_create(referencia_externa=order_id, defaults=defaults)
        if not criada:
            logger.info(f'Webhook Kiwify: order_id {order_id} já registrado.')
            return JsonResponse({'ok': True, 'mensagem': 'Já registrado.'})
    else:
        Compra.objects.create(referencia_externa=None, **defaults)

    logger.info(f'Compra registrada via Kiwify: {order_id} — {status}')
    return JsonResponse({'ok': True})
