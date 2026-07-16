from django.contrib import admin
from .models import Projeto, ImagemProjeto

class ImagemProjetoInline(admin.TabularInline):
    model = ImagemProjeto
    extra = 1

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tipo', 'destaque', 'publico', 'data_criacao')
    list_filter = ('categoria', 'tipo', 'destaque', 'publico', 'data_criacao')
    search_fields = ('titulo', 'descricao_curta', 'tecnologias')
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ('destaque', 'publico')
    inlines = [ImagemProjetoInline]
    actions = ['marcar_destaque', 'remover_destaque', 'publicar_projetos', 'despublicar_projetos']

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