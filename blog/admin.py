from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Categoria, Post, Comentario


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ('nome', 'email', 'conteudo', 'aprovado', 'data_criacao')
    readonly_fields = ('data_criacao',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'total_posts')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)

    def total_posts(self, obj):
        return obj.posts.count()
    total_posts.short_description = "Total de Posts"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'status_badge', 'total_comentarios', 'ver_no_site', 'data_criacao')
    list_filter = ('publicado', 'categoria', 'data_criacao', 'autor')
    search_fields = ('titulo', 'conteudo', 'resumo')
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ()
    date_hierarchy = 'data_criacao'
    filter_horizontal = ('tags',)
    inlines = [ComentarioInline]
    actions = ['publicar_posts', 'despublicar_posts']

    def status_badge(self, obj):
        if obj.publicado:
            return format_html('<span style="background: #10B981; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">PUBLICADO</span>')
        return format_html('<span style="background: #EF4444; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">RASCUNHO</span>')
    status_badge.short_description = "Status"

    def total_comentarios(self, obj):
        count = obj.comentarios.count()
        pendentes = obj.comentarios.filter(aprovado=False).count()
        if pendentes > 0:
            return format_html('<b>{}</b> (<span style="color: #F59E0B; font-weight: bold;">{} pendentes</span>)', count, pendentes)
        return count
    total_comentarios.short_description = "Comentários"

    def ver_no_site(self, obj):
        if obj.publicado and obj.slug:
            url = reverse('blog:detalhe', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank" style="color: #3B82F6; font-weight: bold;">🔗 Ver no site</a>', url)
        return "-"
    ver_no_site.short_description = "Preview"

    @admin.action(description='Publicar posts selecionados')
    def publicar_posts(self, request, queryset):
        queryset.update(publicado=True)

    @admin.action(description='Despublicar posts selecionados')
    def despublicar_posts(self, request, queryset):
        queryset.update(publicado=False)

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
    list_display = ('nome', 'post', 'status_badge', 'data_criacao')
    list_filter = ('aprovado', 'data_criacao', 'post')
    search_fields = ('nome', 'conteudo', 'email')
    actions = ['aprovar_comentarios', 'reprovar_comentarios']

    def status_badge(self, obj):
        if obj.aprovado:
            return format_html('<span style="background: #10B981; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">APROVADO</span>')
        return format_html('<span style="background: #F59E0B; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">PENDENTE</span>')
    status_badge.short_description = "Status"

    def aprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=True)
    aprovar_comentarios.short_description = "Aprovar comentários selecionados"

    def reprovar_comentarios(self, request, queryset):
        queryset.update(aprovado=False)
    reprovar_comentarios.short_description = "Reprovar comentários selecionados"