from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Habilidade, PerfilUsuario


class HabilidadeInline(admin.TabularInline):
    model = Habilidade
    extra = 1


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'cargo', 'disponivel_para_trabalho', 'date_joined')
    list_filter = ('disponivel_para_trabalho', 'cargo')
    search_fields = ('username', 'email', 'cargo')
    inlines = [HabilidadeInline]
    actions = ['marcar_disponivel', 'marcar_indisponivel']

    @admin.action(description='Marcar como disponível para trabalho')
    def marcar_disponivel(self, request, queryset):
        queryset.update(disponivel_para_trabalho=True)

    @admin.action(description='Marcar como indisponível para trabalho')
    def marcar_indisponivel(self, request, queryset):
        queryset.update(disponivel_para_trabalho=False)

    fieldsets = UserAdmin.fieldsets + (
        ('Informações Profissionais', {
            'fields': ('cargo', 'bio', 'avatar', 'localizacao', 'linkedin', 'github', 'site_pessoal', 'whatsapp', 'filosofia', 'disponivel_para_trabalho')
        }),
    )


@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'categoria', 'nivel')
    list_filter = ('categoria', 'nivel')
    search_fields = ('nome',)
    list_editable = ('nivel',)
