from django.contrib import admin
from django.utils.html import format_html
from .models import Compra, LeadOrcamento


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        'comprador_nome', 'comprador_email', 'produto',
        'valor_formatado', 'status_badge', 'plataforma', 'criado_em'
    )
    list_filter = ('status', 'plataforma', 'criado_em')
    search_fields = ('comprador_nome', 'comprador_email', 'referencia_externa', 'produto')
    readonly_fields = ('criado_em', 'atualizado_em')
    date_hierarchy = 'criado_em'
    actions = ['marcar_aprovada', 'marcar_reembolsada']

    def valor_formatado(self, obj):
        if obj.valor is not None:
            return 'R$ {:,.2f}'.format(obj.valor).replace(',', '.')
        return '—'
    valor_formatado.short_description = 'Valor'

    def status_badge(self, obj):
        cores = {
            'aprovada':    ('#10B981', 'APROVADA'),
            'pendente':    ('#F59E0B', 'PENDENTE'),
            'reembolsada': ('#EF4444', 'REEMBOLSADA'),
            'cancelada':   ('#6B7280', 'CANCELADA'),
        }
        cor, label = cores.get(obj.status, ('#6B7280', obj.status.upper()))
        return format_html(
            '<span style="background:{};color:white;padding:3px 8px;'
            'border-radius:6px;font-weight:bold;font-size:11px;">{}</span>',
            cor, label
        )
    status_badge.short_description = 'Status'

    @admin.action(description='Marcar como Aprovada')
    def marcar_aprovada(self, request, queryset):
        queryset.update(status='aprovada')

    @admin.action(description='Marcar como Reembolsada')
    def marcar_reembolsada(self, request, queryset):
        queryset.update(status='reembolsada')


@admin.register(LeadOrcamento)
class LeadOrcamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'whatsapp', 'tipos_projeto', 'prazo', 'atendido', 'criado_em')
    list_filter = ('atendido', 'prazo', 'criado_em')
    search_fields = ('nome', 'email', 'whatsapp', 'descricao')
    readonly_fields = ('criado_em',)
    date_hierarchy = 'criado_em'
    actions = ['marcar_atendido']

    @admin.action(description='Marcar como Atendido')
    def marcar_atendido(self, request, queryset):
        queryset.update(atendido=True)

