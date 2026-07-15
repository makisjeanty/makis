import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from .models import Mensagem

SALA_PADRAO = 'geral'


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
