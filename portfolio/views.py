from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Projeto

POR_PAGINA = 9


def lista_projetos(request):
    projetos = Projeto.objects.filter(publico=True)

    categoria_ativa = request.GET.get('categoria')
    if categoria_ativa:
        projetos = projetos.filter(categoria=categoria_ativa)

    page_obj = Paginator(projetos, POR_PAGINA).get_page(request.GET.get('page'))

    return render(request, 'portfolio/lista.html', {
        'page_obj': page_obj,
        'projetos': page_obj,
        'categorias': Projeto.CATEGORIAS,
        'categoria_ativa': categoria_ativa,
    })


def cases(request):
    projetos = Projeto.objects.filter(publico=True, destaque=True)
    return render(request, 'portfolio/cases.html', {'projetos': projetos})


def detalhe_projeto(request, slug):
    projeto = get_object_or_404(Projeto, slug=slug, publico=True)
    outros_projetos = Projeto.objects.filter(publico=True).exclude(pk=projeto.pk)[:3]
    return render(request, 'portfolio/detalhe.html', {
        'projeto': projeto,
        'outros_projetos': outros_projetos,
        'og_image_url': projeto.imagem_principal.url if projeto.imagem_principal else None,
    })
