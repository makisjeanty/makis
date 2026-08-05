from django.db.models import Count, Sum, Prefetch
from django.shortcuts import render, get_object_or_404
from .models import Curso, Modulo, Licao


def lista_cursos(request):
    cursos = Curso.objects.filter(ativo=True).prefetch_related('modulos__licoes').order_by('ordem')
    
    # Anexa estatísticas calculadas para cada curso
    cursos_com_stats = []
    for curso in cursos:
        total_licoes = 0
        duracao_total = 0
        for modulo in curso.modulos.all():
            licoes = modulo.licoes.all()
            total_licoes += len(licoes)
            duracao_total += sum(l.duracao_minutos for l in licoes)
        
        curso.total_licoes = total_licoes
        curso.duracao_total = duracao_total
        cursos_com_stats.append(curso)

    return render(request, 'cursos/lista.html', {
        'cursos': cursos_com_stats,
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
