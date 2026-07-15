from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'cargo', 'disponivel_para_trabalho', 'date_joined')
    list_filter = ('disponivel_para_trabalho', 'cargo')
    search_fields = ('username', 'email', 'cargo')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Profissionais', {
            'fields': ('cargo', 'bio', 'avatar', 'localizacao', 'linkedin', 'github', 'site_pessoal', 'whatsapp', 'habilidades', 'disponivel_para_trabalho')
        }),
    )