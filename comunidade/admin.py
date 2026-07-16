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
    actions = ['aprovar_topicos', 'reprovar_topicos', 'fixar_topicos', 'desafixar_topicos']

    @admin.action(description='Aprovar tópicos selecionados')
    def aprovar_topicos(self, request, queryset):
        queryset.update(aprovado=True)

    @admin.action(description='Reprovar tópicos selecionados')
    def reprovar_topicos(self, request, queryset):
        queryset.update(aprovado=False)

    @admin.action(description='Fixar tópicos selecionados')
    def fixar_topicos(self, request, queryset):
        queryset.update(fixado=True)

    @admin.action(description='Desafixar tópicos selecionados')
    def desafixar_topicos(self, request, queryset):
        queryset.update(fixado=False)


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('autor_nome', 'topico', 'aprovado', 'data_criacao')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('autor_nome', 'autor_email', 'conteudo')
    list_editable = ('aprovado',)
    actions = ['aprovar_respostas', 'reprovar_respostas']

    @admin.action(description='Aprovar respostas selecionadas')
    def aprovar_respostas(self, request, queryset):
        queryset.update(aprovado=True)

    @admin.action(description='Reprovar respostas selecionadas')
    def reprovar_respostas(self, request, queryset):
        queryset.update(aprovado=False)
