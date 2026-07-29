"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Precisa ser instanciado antes de importar qualquer coisa que toque em models/apps
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import AllowedHostsOriginValidator  # noqa: E402

import chat.routing  # noqa: E402

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    # Rejeita handshakes de WebSocket cujo header Origin não bata com
    # ALLOWED_HOSTS — sem isso, qualquer site de terceiros pode abrir uma
    # conexão cross-site ao chat (CSWSH) no contexto do navegador da vítima.
    'websocket': AllowedHostsOriginValidator(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})
