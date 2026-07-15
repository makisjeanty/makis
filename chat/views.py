from django.shortcuts import render

from .consumers import SALA_PADRAO
from .models import Mensagem


def sala(request):
    mensagens = list(Mensagem.objects.filter(sala=SALA_PADRAO).order_by('-criado_em')[:50])
    mensagens.reverse()
    return render(request, 'chat/sala.html', {'mensagens': mensagens})
