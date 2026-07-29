from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Projeto, ImagemProjeto


class ImagemProjetoInline(admin.TabularInline):
    model = ImagemProjeto
    extra = 1


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tipo', 'status_destaque', 'status_publico', 'ver_no_site', 'data_criacao')
    list_filter = ('categoria', 'tipo', 'destaque', 'publico', 'data_criacao')
    search_fields = ('titulo', 'descricao_curta', 'tecnologias')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ImagemProjetoInline]
    actions = ['marcar_destaque', 'remover_destaque', 'publicar_projetos', 'despublicar_projetos']

    def status_destaque(self, obj):
        if obj.destaque:
            return format_html('<span style="background: #F59E0B; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">⭐ DESTAQUE</span>')
        return "-"
    status_destaque.short_description = "Destaque"

    def status_publico(self, obj):
        if obj.publico:
            return format_html('<span style="background: #10B981; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">VISÍVEL</span>')
        return format_html('<span style="background: #EF4444; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">OCULTO</span>')
    status_publico.short_description = "Status"

    def ver_no_site(self, obj):
        if obj.publico and obj.slug:
            url = reverse('portfolio:detalhe', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank" style="color: #3B82F6; font-weight: bold;">🔗 Ver Projeto</a>', url)
        return "-"
    ver_no_site.short_description = "Preview"

    @admin.action(description='Marcar como destaque')
    def marcar_destaque(self, request, queryset):
        queryset.update(destaque=True)

    @admin.action(description='Remover destaque')
    def remover_destaque(self, request, queryset):
        queryset.update(destaque=False)

    @admin.action(description='Publicar projetos selecionados')
    def publicar_projetos(self, request, queryset):
        queryset.update(publico=True)

    @admin.action(description='Despublicar projetos selecionados')
    def despublicar_projetos(self, request, queryset):
        queryset.update(publico=False)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'slug', 'categoria', 'tipo', 'descricao_curta', 'descricao_completa')
        }),
        ('Mídia', {
            'fields': ('imagem_principal',)
        }),
        ('Links', {
            'fields': ('link_demo', 'link_github')
        }),
        ('Tecnologias', {
            'fields': ('tecnologias',)
        }),
        ('Publicação', {
            'fields': ('destaque', 'publico')
        }),
    )


@admin.register(ImagemProjeto)
class ImagemProjetoAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'legenda')
    list_filter = ('projeto',)
    search_fields = ('legenda',)