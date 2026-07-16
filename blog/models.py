from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from core.image_utils import otimizar_imagem

User = get_user_model()

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

class Post(models.Model):
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    resumo = models.TextField(max_length=400, help_text='Resumo que aparece na listagem')
    conteudo = models.TextField(verbose_name='Conteúdo completo (use Markdown)')
    imagem_capa = models.ImageField(upload_to='blog/capas/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)
    data_publicacao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-data_publicacao']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._imagem_capa_original = self.imagem_capa.name if self.pk else None

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        if self.imagem_capa and self.imagem_capa.name != self._imagem_capa_original:
            otimizado = otimizar_imagem(self.imagem_capa, max_dimensao=1920)
            self.imagem_capa.save(otimizado.name, otimizado, save=False)
            self._imagem_capa_original = self.imagem_capa.name
        super().save(*args, **kwargs)

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    conteudo = models.TextField(max_length=1000)
    data_criacao = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
    
    def __str__(self):
        return f'Comentário de {self.nome} em "{self.post.titulo}"'