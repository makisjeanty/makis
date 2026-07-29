import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.utils import timezone

from .models import Mensagem

SALA_PADRAO = 'geral'

# Throttle simples por IP: no máximo RATE_LIMIT_MAX mensagens a cada
# RATE_LIMIT_JANELA segundos. Usa o mesmo cache configurado em CACHES
# (Redis em produção, in-memory local — igual ao resto do projeto), então
# um único contador vale por todos os workers em produção.
RATE_LIMIT_JANELA = 10
RATE_LIMIT_MAX = 8


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.grupo = f'chat_{SALA_PADRAO}'
        await self.channel_layer.group_add(self.grupo, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.grupo, self.channel_name)

    async def receive(self, text_data):
        try:
            dados = json.loads(text_data)
        except json.JSONDecodeError:
            return

        nome = str(dados.get('nome', '')).strip()[:50]
        texto = str(dados.get('texto', '')).strip()[:500]

        if not nome or not texto:
            return

        if not await self._dentro_do_limite():
            await self.send(text_data=json.dumps({
                'erro': 'Muitas mensagens em pouco tempo. Aguarde um instante.',
            }))
            return

        mensagem = await self.salvar_mensagem(nome, texto)

        await self.channel_layer.group_send(self.grupo, {
            'type': 'chat.mensagem',
            'nome': mensagem.nome,
            'texto': mensagem.texto,
            'criado_em': timezone.localtime(mensagem.criado_em).strftime('%H:%M'),
        })

    async def chat_mensagem(self, event):
        await self.send(text_data=json.dumps({
            'nome': event['nome'],
            'texto': event['texto'],
            'criado_em': event['criado_em'],
        }))

    @database_sync_to_async
    def salvar_mensagem(self, nome, texto):
        return Mensagem.objects.create(sala=SALA_PADRAO, nome=nome, texto=texto)

    def _client_ip(self):
        # Atrás do nginx (docker-compose.yml), a conexão TCP chega de dentro
        # da rede docker — o IP real do visitante vem no X-Forwarded-For que
        # o nginx anexa (proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for).
        # Pegamos o ÚLTIMO valor da lista (o mais próximo do nosso proxy
        # confiável), não o primeiro: um cliente malicioso pode mandar seu
        # próprio X-Forwarded-For, mas o nginx sempre acrescenta o IP real
        # observado no final da lista.
        for nome_header, valor in self.scope.get('headers', []):
            if nome_header == b'x-forwarded-for':
                partes = valor.decode('latin1').split(',')
                return partes[-1].strip()
        cliente = self.scope.get('client')
        return cliente[0] if cliente else 'desconhecido'

    async def _dentro_do_limite(self):
        chave = f'chat_ratelimit:{self._client_ip()}'

        # add() só grava se a chave ainda não existir — é atômico no backend
        # de cache (Redis/locmem), então duas mensagens concorrentes não
        # conseguem as duas passar pelo "contagem is None" ao mesmo tempo.
        await sync_to_async(cache.add)(chave, 0, timeout=RATE_LIMIT_JANELA)
        contagem = await sync_to_async(cache.incr)(chave)
        return contagem <= RATE_LIMIT_MAX
