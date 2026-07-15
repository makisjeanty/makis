from django.contrib import admin
from .models import Categoria, Post, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'publicado', 'data_criacao')
    list_filter = ('publicado', 'categoria', 'data_criacao', 'autor')
    search_fields = ('titulo', 'conteudo', 'resumo')
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ('publicado',)
    date_hierarchy = 'data_criacao'

    fieldsets = (
        ('Informações do Post', {
            'fields': ('titulo', 'slug', 'autor', 'categoria', 'resumo', 'conteudo')
        }),
        ('Mídia', {
            'fields': ('imagem_capa',)
        }),
        ('SEO e Tags', {
            'fields': ('tags',)
        }),
        ('Publicação', {
            'fields': ('publicado',)
        }),
    )

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'post', 'aprovado', 'data_criacao')
    list_filter = ('aprovado', 'data_criacao', 'post')
    search_fields = ('nome', 'conteudo', 'email')
    list_editable = ('aprovado',)
    actions = ['aprovar_comentarios']
    
    def aprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=True)
    aprovar_comentarios.short_description = "Aprovar comentários selecionados"