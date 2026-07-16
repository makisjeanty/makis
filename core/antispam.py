import time

from django.core import signing

SALT = 'antispam-honeypot'
CAMPO_HONEYPOT = 'website'
CAMPO_TIMESTAMP = 'ts_form'
TEMPO_MINIMO_SEGUNDOS = 3


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
