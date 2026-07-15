from django.contrib import admin

from .models import Mensagem


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'texto', 'sala', 'criado_em')
    list_filter = ('sala', 'criado_em')
    search_fields = ('nome', 'texto')
