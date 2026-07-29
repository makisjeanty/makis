import time

from django.core import signing

from core.antispam import SALT


def antispam_ok():
    """Campos que fazem um POST parecer preenchido por um humano: honeypot
    vazio + timestamp assinado de alguns segundos atrás. Usar em testes que
    precisam passar pelo core.antispam.formulario_parece_bot()."""
    return {'website': '', 'ts_form': signing.dumps(time.time() - 5, salt=SALT)}
