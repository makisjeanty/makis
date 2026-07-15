from django.contrib import admin

from .models import Resposta, Topico


class RespostaInline(admin.TabularInline):
    model = Resposta
    extra = 0


@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor_nome', 'aprovado', 'fixado', 'data_criacao')
    list_filter = ('aprovado', 'fixado', 'data_criacao')
    search_fields = ('titulo', 'autor_nome', 'autor_email', 'conteudo')
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ('aprovado', 'fixado')
    inlines = [RespostaInline]


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('autor_nome', 'topico', 'aprovado', 'data_criacao')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('autor_nome', 'autor_email', 'conteudo')
    list_editable = ('aprovado',)
