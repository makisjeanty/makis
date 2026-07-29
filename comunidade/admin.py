from django.contrib import admin
from django.utils.html import format_html
from .models import Resposta, Topico


class RespostaInline(admin.TabularInline):
    model = Resposta
    extra = 0
    fields = ('autor_nome', 'autor_email', 'conteudo', 'aprovado', 'data_criacao')
    readonly_fields = ('data_criacao',)


@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor_nome', 'status_badge', 'status_fixado', 'total_respostas', 'data_criacao')
    list_filter = ('aprovado', 'fixado', 'data_criacao')
    search_fields = ('titulo', 'autor_nome', 'autor_email', 'conteudo')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [RespostaInline]
    actions = ['aprovar_topicos', 'reprovar_topicos', 'fixar_topicos', 'desafixar_topicos']

    def status_badge(self, obj):
        if obj.aprovado:
            return format_html('<span style="background: #10B981; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">APROVADO</span>')
        return format_html('<span style="background: #F59E0B; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">PENDENTE</span>')
    status_badge.short_description = "Status"

    def status_fixado(self, obj):
        if obj.fixado:
            return format_html('<span style="background: #8B5CF6; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">📌 FIXADO</span>')
        return "-"
    status_fixado.short_description = "Fixado"

    def total_respostas(self, obj):
        return obj.respostas.count()
    total_respostas.short_description = "Respostas"

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
    list_display = ('autor_nome', 'topico', 'status_badge', 'data_criacao')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('autor_nome', 'autor_email', 'conteudo')
    actions = ['aprovar_respostas', 'reprovar_respostas']

    def status_badge(self, obj):
        if obj.aprovado:
            return format_html('<span style="background: #10B981; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">APROVADO</span>')
        return format_html('<span style="background: #F59E0B; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">PENDENTE</span>')
    status_badge.short_description = "Status"

    @admin.action(description='Aprovar respostas selecionadas')
    def aprovar_respostas(self, request, queryset):
        queryset.update(aprovado=True)

    @admin.action(description='Reprovar respostas selecionadas')
    def reprovar_respostas(self, request, queryset):
        queryset.update(aprovado=False)

