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
    
    filosofia = models.TextField(blank=True, max_length=600, verbose_name='Minha filosofia', help_text='O que você busca, como trabalha. Ex: "Quero resolver problemas de negócio usando tecnologia..."')
    disponivel_para_trabalho = models.BooleanField(default=True, verbose_name='Disponível para novos projetos')
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.cargo}"


class Habilidade(models.Model):
    CATEGORIAS = [
        ('linguagem', 'Linguagem'),
        ('framework', 'Framework'),
        ('banco', 'Banco de Dados'),
        ('cloud', 'Cloud/DevOps'),
        ('ferramenta', 'Ferramenta'),
    ]
    NIVEIS = [
        (1, 'Já explorei'),
        (2, 'Estudando'),
        (3, 'Domino bem'),
    ]

    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='skills')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='linguagem')
    nivel = models.PositiveSmallIntegerField(choices=NIVEIS, default=2, verbose_name='Nível de confiança')

    class Meta:
        ordering = ['categoria', '-nivel', 'nome']
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return f'{self.nome} ({self.get_nivel_display()})'