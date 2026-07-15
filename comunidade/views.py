from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RespostaForm, TopicoForm
from .models import Topico

POR_PAGINA = 10


def lista(request):
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save()
            messages.success(request, 'Tópico publicado!')
            return redirect('comunidade:detalhe', slug=topico.slug)
    else:
        form = TopicoForm()

    topicos = Topico.objects.filter(aprovado=True)
    page_obj = Paginator(topicos, POR_PAGINA).get_page(request.GET.get('page'))

    return render(request, 'comunidade/lista.html', {
        'page_obj': page_obj,
        'topicos': page_obj,
        'form': form,
    })


def detalhe(request, slug):
    topico = get_object_or_404(Topico, slug=slug, aprovado=True)

    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.topico = topico
            resposta.save()
            messages.success(request, 'Resposta publicada!')
            return redirect('comunidade:detalhe', slug=topico.slug)
    else:
        form = RespostaForm()

    respostas = topico.respostas.filter(aprovado=True)

    return render(request, 'comunidade/detalhe.html', {
        'topico': topico,
        'respostas': respostas,
        'form': form,
    })
