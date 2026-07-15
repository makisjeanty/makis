from django.db import models
from django.utils.text import slugify


class Topico(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, blank=True, max_length=220)
    autor_nome = models.CharField(max_length=100, verbose_name='Nome')
    autor_email = models.EmailField(verbose_name='E-mail')
    conteudo = models.TextField(max_length=3000, verbose_name='Mensagem')
    data_criacao = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=True, verbose_name='Visível publicamente')
    fixado = models.BooleanField(default=False, verbose_name='Fixado no topo')

    class Meta:
        ordering = ['-fixado', '-data_criacao']
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200]
            slug = base
            contador = 1
            while Topico.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                contador += 1
                slug = f'{base}-{contador}'
            self.slug = slug
        super().save(*args, **kwargs)


class Resposta(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='respostas')
    autor_nome = models.CharField(max_length=100, verbose_name='Nome')
    autor_email = models.EmailField(verbose_name='E-mail')
    conteudo = models.TextField(max_length=2000, verbose_name='Resposta')
    data_criacao = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=True, verbose_name='Visível publicamente')

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    def __str__(self):
        return f'Resposta de {self.autor_nome} em "{self.topico.titulo}"'
