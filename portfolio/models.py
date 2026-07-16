from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

from core.image_utils import otimizar_imagem

class Projeto(models.Model):
    CATEGORIAS = [
        ('web', 'Web'),
        ('mobile', 'Mobile'),
        ('data', 'Análise de Dados'),
        ('automacao', 'Automação'),
        ('outro', 'Outro'),
    ]

    TIPOS = [
        ('pessoal', 'Projeto Pessoal'),
        ('academico', 'Projeto Acadêmico'),
        ('fork', 'Fork de Open Source'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, blank=True)
    descricao_curta = models.TextField(max_length=300, verbose_name='Descrição curta')
    descricao_completa = models.TextField(verbose_name='Descrição completa')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='web')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='pessoal', verbose_name='Tipo de projeto')
    imagem_principal = models.ImageField(
        upload_to='projetos/', 
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    link_demo = models.URLField(blank=True, null=True, verbose_name='Link demo')
    link_github = models.URLField(blank=True, null=True, verbose_name='Link GitHub')
    tecnologias = models.CharField(max_length=500, help_text='Separe por vírgulas: Python,Django,MySQL')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    destaque = models.BooleanField(default=False, verbose_name='Destaque na home')
    publico = models.BooleanField(default=True, verbose_name='Publicado')
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._imagem_principal_original = self.imagem_principal.name if self.pk else None

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        if self.imagem_principal and self.imagem_principal.name != self._imagem_principal_original:
            otimizado = otimizar_imagem(self.imagem_principal, max_dimensao=1920)
            self.imagem_principal.save(otimizado.name, otimizado, save=False)
            self._imagem_principal_original = self.imagem_principal.name
        super().save(*args, **kwargs)

    def get_tecnologias_list(self):
        return [tech.strip() for tech in self.tecnologias.split(',')]

class ImagemProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(
        upload_to='projetos/galeria/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    legenda = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Imagem do projeto'
        verbose_name_plural = 'Imagens dos projetos'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._imagem_original = self.imagem.name if self.pk else None

    def save(self, *args, **kwargs):
        if self.imagem and self.imagem.name != self._imagem_original:
            otimizado = otimizar_imagem(self.imagem, max_dimensao=1920)
            self.imagem.save(otimizado.name, otimizado, save=False)
            self._imagem_original = self.imagem.name
        super().save(*args, **kwargs)