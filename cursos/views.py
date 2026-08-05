from django.http import JsonResponse
from .models import Curso, Modulo, Licao, ProgressoLicao


def lista_cursos(request):
    cursos = Curso.objects.filter(ativo=True).prefetch_related('modulos__licoes').order_by('ordem')
    
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
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Obtém IDs das lições concluídas nesta sessão
    licoes_concluidas_ids = set(
        ProgressoLicao.objects.filter(session_key=session_key, concluida=True)
        .values_list('licao_id', flat=True)
    )

    modulos = curso.modulos.prefetch_related('licoes').all()
    
    # Processa desbloqueio sequencial:
    # A primeira lição da trilha é sempre liberada.
    # As subsequentes só são liberadas se a lição anterior tiver sido concluída.
    anterior_concluida = True  # Primeira lição sempre liberada
    
    for modulo in modulos:
        for licao in modulo.licoes.all():
            licao.concluidade = licao.id in licoes_concluidas_ids
            licao.liberada = anterior_concluida
            
            # Próxima lição só é liberada se ESTA lição estiver concluída
            anterior_concluida = licao.concluidade

    return render(request, 'cursos/trilha.html', {
        'curso': curso,
        'modulos': modulos,
        'licoes_concluidas_ids': licoes_concluidas_ids,
    })


def executar_licao(request, licao_id):
    licao = get_object_or_404(Licao, id=licao_id)
    etapas = licao.etapas.all()
    return render(request, 'cursos/licao.html', {
        'licao': licao,
        'etapas': etapas,
    })


def concluir_licao(request, licao_id):
    licao = get_object_or_404(Licao, id=licao_id)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    ProgressoLicao.objects.get_or_create(session_key=session_key, licao=licao, defaults={'concluida': True})
    return JsonResponse({'status': 'ok', 'licao_id': licao.id})

