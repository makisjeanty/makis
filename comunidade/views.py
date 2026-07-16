from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django_ratelimit.decorators import ratelimit

from core.antispam import formulario_parece_bot, gerar_timestamp_assinado

from .forms import RespostaForm, TopicoForm
from .models import Topico

POR_PAGINA = 10

MENSAGEM_LIMITE = 'Muitas publicações em pouco tempo. Aguarde alguns minutos e tente novamente.'
MENSAGEM_ANTISPAM = 'Não foi possível processar seu envio. Tente novamente.'


@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def lista(request):
    form = TopicoForm(request.POST or None)
    if request.method == 'POST':
        if getattr(request, 'limited', False):
            messages.error(request, MENSAGEM_LIMITE)
        elif formulario_parece_bot(request):
            messages.error(request, MENSAGEM_ANTISPAM)
        elif form.is_valid():
            topico = form.save()
            messages.success(request, 'Tópico publicado!')
            return redirect('comunidade:detalhe', slug=topico.slug)

    topicos = Topico.objects.filter(aprovado=True)
    page_obj = Paginator(topicos, POR_PAGINA).get_page(request.GET.get('page'))

    return render(request, 'comunidade/lista.html', {
        'page_obj': page_obj,
        'topicos': page_obj,
        'form': form,
        'antispam_ts': gerar_timestamp_assinado(),
    })


@ratelimit(key='ip', rate='10/m', method='POST', block=False)
def detalhe(request, slug):
    topico = get_object_or_404(Topico, slug=slug, aprovado=True)

    form = RespostaForm(request.POST or None)
    if request.method == 'POST':
        if getattr(request, 'limited', False):
            messages.error(request, MENSAGEM_LIMITE)
        elif formulario_parece_bot(request):
            messages.error(request, MENSAGEM_ANTISPAM)
        elif form.is_valid():
            resposta = form.save(commit=False)
            resposta.topico = topico
            resposta.save()
            messages.success(request, 'Resposta publicada!')
            return redirect('comunidade:detalhe', slug=topico.slug)

    respostas = topico.respostas.filter(aprovado=True)

    return render(request, 'comunidade/detalhe.html', {
        'topico': topico,
        'respostas': respostas,
        'form': form,
        'antispam_ts': gerar_timestamp_assinado(),
    })
