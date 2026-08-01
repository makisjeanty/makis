from django.shortcuts import render, get_object_or_404
from .models import Curso, Modulo, Licao


def lista_cursos(request):
    cursos = Curso.objects.filter(ativo=True)
    return render(request, 'cursos/lista.html', {
        'cursos': cursos,
    })


def trilha_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug, ativo=True)
    modulos = curso.modulos.prefetch_related('licoes').all()
    return render(request, 'cursos/trilha.html', {
        'curso': curso,
        'modulos': modulos,
    })


def executar_licao(request, licao_id):
    licao = get_object_or_404(Licao, id=licao_id)
    etapas = licao.etapas.all()
    return render(request, 'cursos/licao.html', {
        'licao': licao,
        'etapas': etapas,
    })
