from django.contrib import admin
from .models import Curso, Modulo, Licao, Etapa


class EtapaInline(admin.TabularInline):
    model = Etapa
    extra = 1


@admin.register(Licao)
class LicaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'ordem', 'duracao_minutos')
    list_filter = ('modulo__curso', 'modulo')
    inlines = [EtapaInline]


class LicaoInline(admin.TabularInline):
    model = Licao
    extra = 1


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ordem')
    list_filter = ('curso',)
    inlines = [LicaoInline]


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('icone', 'titulo', 'nivel', 'ordem', 'ativo')
    list_editable = ('ordem', 'ativo')
    prepopulated_fields = {'slug': ('titulo',)}
