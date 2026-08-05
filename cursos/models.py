from django.db import models
from django.utils.text import slugify

class Curso(models.Model):
    NIVEIS = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título do Curso')
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField(verbose_name='Descrição')
    icone = models.CharField(max_length=50, default='🐍', help_text='Emoji ou classe de ícone: 🐍, ⚡, 🤖')
    nivel = models.CharField(max_length=20, choices=NIVEIS, default='iniciante')
    ordem = models.PositiveIntegerField(default=1)
    ativo = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return f"{self.icone} {self.titulo}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200, verbose_name='Título do Módulo')
    descricao = models.TextField(blank=True, verbose_name='Descrição do Módulo')
    icone = models.CharField(max_length=50, default='📌', help_text='Emoji ou símbolo do capítulo: 🐍, 🧱, ⚡, 🤖, 💾')
    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return f"{self.icone} {self.curso.titulo} - {self.titulo}"


class Licao(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='licoes')
    titulo = models.CharField(max_length=200, verbose_name='Título da Lição')
    descricao = models.TextField(blank=True, verbose_name='Descrição da Lição')
    icone = models.CharField(max_length=50, default='🎯', help_text='Emoji ou símbolo do tópico: 🐍, ⚡, 🎯, 🧠, ⚙️')
    ordem = models.PositiveIntegerField(default=1)
    duracao_minutos = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Lição'
        verbose_name_plural = 'Lições'

    def __str__(self):
        return f"{self.icone} {self.modulo.titulo} -> {self.titulo}"



class Etapa(models.Model):
    TIPOS = [
        ('slide', 'Slide Explicativo (Teoria)'),
        ('quiz', 'Múltipla Escolha (Quiz)'),
        ('code', 'Completar Código'),
    ]

    licao = models.ForeignKey(Licao, on_delete=models.CASCADE, related_name='etapas')
    ordem = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='slide')
    
    # Conteúdo geral / Slide
    titulo = models.CharField(max_length=250, blank=True)
    conteudo = models.TextField(blank=True, help_text='Texto explicativo ou instruções')
    imagem_url = models.URLField(blank=True, null=True)

    # Quiz & Exercício
    pergunta = models.CharField(max_length=300, blank=True)
    opcoes_json = models.JSONField(default=list, blank=True, help_text='Lista de strings para as opções')
    resposta_correta = models.CharField(max_length=250, blank=True)
    
    # Bloco de código
    nome_arquivo = models.CharField(max_length=50, default='script.py', blank=True)
    dica = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Etapa da Lição'
        verbose_name_plural = 'Etapas da Lição'

    def __str__(self):
        return f"Lição {self.licao.id} - Etapa {self.ordem} ({self.get_tipo_display()})"


class ProgressoLicao(models.Model):
    session_key = models.CharField(max_length=100, db_index=True)
    licao = models.ForeignKey(Licao, on_delete=models.CASCADE, related_name='progressos')
    concluida = models.BooleanField(default=True)
    data_conclusao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'licao')
        verbose_name = 'Progresso de Lição'
        verbose_name_plural = 'Progressos de Lições'

    def __str__(self):
        return f"Sessão {self.session_key[:8]}... - Lição {self.licao.titulo}"

