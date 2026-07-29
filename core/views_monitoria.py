"""
views_monitoria.py — Painel de Monitoria do Makis Digital

Três frentes:
  1. Vendas — modelo Compra + webhook Kiwify
  2. Servidor — saúde do banco, Redis, contadores
  3. Moderação — comentários pendentes, tópicos, chat

Acesso restrito a superusers via decorador customizado.
"""

import hmac
import json
import logging
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.core.cache import caches
from django.db import connection
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from decouple import config

from blog.models import Comentario, Post
from chat.models import Mensagem
from comunidade.models import Topico, Resposta
from core.models import Compra
from portfolio.models import Projeto

logger = logging.getLogger('django.request')


# ─────────────────────────────────────────────────────────────
#  Decorador: só superuser passa
# ─────────────────────────────────────────────────────────────

def superuser_required(view_func):
    """Redireciona para login se não autenticado; retorna 403 se não é superuser."""
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden('Acesso negado.')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ─────────────────────────────────────────────────────────────
#  Helpers de saúde do servidor
# ─────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────
#  View principal: Painel de Monitoria
# ─────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────
#  API JSON — dados em tempo real para o painel (fetch AJAX)
# ─────────────────────────────────────────────────────────────

@superuser_required
@require_GET
def api_monitoria(request):
    dados = _contadores()
    dados['banco_ok'] = _checar_banco()
    dados['redis_ok'] = _checar_redis()
    dados['timestamp'] = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')
    return JsonResponse(dados)


# ─────────────────────────────────────────────────────────────
#  AJAX inline — aprovar/rejeitar comentário sem sair do painel
# ─────────────────────────────────────────────────────────────

@superuser_required
@require_POST
def moderar_comentario(request, comentario_id):
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


# ─────────────────────────────────────────────────────────────
#  Webhook Kiwify — recebe POST com confirmação de compra
# ─────────────────────────────────────────────────────────────

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
