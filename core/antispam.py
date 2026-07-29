import time

from django.contrib import messages
from django.core import signing

SALT = 'antispam-honeypot'
CAMPO_HONEYPOT = 'website'
CAMPO_TIMESTAMP = 'ts_form'
TEMPO_MINIMO_SEGUNDOS = 3

MENSAGEM_LIMITE_PADRAO = 'Muitas mensagens em pouco tempo. Aguarde alguns minutos e tente novamente.'
MENSAGEM_ANTISPAM_PADRAO = 'Não foi possível processar seu envio. Tente novamente.'


def gerar_timestamp_assinado():
    """Chamar no GET (antes de renderizar o form) e colocar no contexto
    como antispam_ts, pra ser reenviado como campo oculto no POST."""
    return signing.dumps(time.time(), salt=SALT)


def formulario_parece_bot(request):
    """True se o POST tem cara de bot: campo-honeypot preenchido (só um
    bot preencheria, é escondido via CSS) ou enviado rápido/sem a marca
    de tempo assinada (nenhum humano preenche um formulário em menos de
    TEMPO_MINIMO_SEGUNDOS)."""
    if request.POST.get(CAMPO_HONEYPOT):
        return True

    bruto = request.POST.get(CAMPO_TIMESTAMP, '')
    try:
        enviado_em = signing.loads(bruto, salt=SALT, max_age=3600)
    except signing.BadSignature:
        return True

    return (time.time() - enviado_em) < TEMPO_MINIMO_SEGUNDOS


def bloquear_submissao_suspeita(request, mensagem_limite=MENSAGEM_LIMITE_PADRAO, mensagem_antispam=MENSAGEM_ANTISPAM_PADRAO):
    """Checa rate-limit (django-ratelimit, via request.limited) e antispam
    (honeypot + timestamp) num POST. Já adiciona a messages.error
    correspondente quando bloqueia. Retorna True se a submissão deve ser
    rejeitada (view não deve seguir para form.is_valid())."""
    if getattr(request, 'limited', False):
        messages.error(request, mensagem_limite)
        return True
    if formulario_parece_bot(request):
        messages.error(request, mensagem_antispam)
        return True
    return False
