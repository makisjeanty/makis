from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class PerfilUsuario(AbstractUser):
    # Extensões do perfil profissional
    cargo = models.CharField(max_length=200, verbose_name='Cargo atual', default='Analista de Sistemas')
    bio = models.TextField(max_length=1000, verbose_name='Biografia', blank=True)
    avatar = models.ImageField(upload_to='perfis/', null=True, blank=True)
    localizacao = models.CharField(max_length=200, blank=True, verbose_name='Localização')
    
    # Links profissionais
    linkedin = models.URLField(blank=True, null=True, verbose_name='LinkedIn')
    github = models.URLField(blank=True, null=True, verbose_name='GitHub')
    site_pessoal = models.URLField(blank=True, null=True, verbose_name='Site pessoal')
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name='WhatsApp (apenas números)')
    
    # Habilidades (separadas por vírgula)
    habilidades = models.TextField(blank=True, help_text='Ex: Python, Django, MySQL, AWS, Power BI')
    disponivel_para_trabalho = models.BooleanField(default=True, verbose_name='Disponível para novos projetos')
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.cargo}"
    
    def get_habilidades_list(self):
        return [h.strip() for h in self.habilidades.split(',')] if self.habilidades else []