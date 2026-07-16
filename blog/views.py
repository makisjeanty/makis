from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django_ratelimit.decorators import ratelimit

from core.antispam import formulario_parece_bot, gerar_timestamp_assinado

from .forms import ComentarioForm
from .models import Categoria, Post

POR_PAGINA = 9


def lista_posts(request):
    posts = Post.objects.filter(publicado=True).select_related('categoria', 'autor')

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        posts = posts.filter(categoria__slug=categoria_slug)

    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    page_obj = Paginator(posts, POR_PAGINA).get_page(request.GET.get('page'))

    return render(request, 'blog/lista.html', {
        'page_obj': page_obj,
        'posts': page_obj,
        'categorias': Categoria.objects.all(),
        'categoria_ativa': categoria_slug,
    })


@ratelimit(key='ip', rate='10/m', method='POST', block=False)
def detalhe_post(request, slug):
    post = get_object_or_404(Post, slug=slug, publicado=True)

    form = ComentarioForm(request.POST or None)
    if request.method == 'POST':
        if getattr(request, 'limited', False):
            messages.error(request, 'Muitos comentários em pouco tempo. Aguarde alguns minutos e tente novamente.')
        elif formulario_parece_bot(request):
            messages.error(request, 'Não foi possível processar seu envio. Tente novamente.')
        elif form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.save()
            messages.success(request, 'Comentário enviado! Ele aparecerá aqui após ser aprovado.')
            return redirect('blog:detalhe', slug=post.slug)

    comentarios = post.comentarios.filter(aprovado=True)
    posts_relacionados = Post.objects.filter(
        publicado=True, categoria=post.categoria
    ).exclude(pk=post.pk)[:3]
    return render(request, 'blog/detalhe.html', {
        'post': post,
        'comentarios': comentarios,
        'posts_relacionados': posts_relacionados,
        'form': form,
        'antispam_ts': gerar_timestamp_assinado(),
        'og_image_url': post.imagem_capa.url if post.imagem_capa else None,
    })


def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'blog/categorias.html', {'categorias': categorias})


def posts_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    posts = Post.objects.filter(publicado=True, categoria=categoria)
    page_obj = Paginator(posts, POR_PAGINA).get_page(request.GET.get('page'))
    return render(request, 'blog/lista.html', {
        'page_obj': page_obj,
        'posts': page_obj,
        'categorias': Categoria.objects.all(),
        'categoria_ativa': slug,
        'categoria_obj': categoria,
    })
