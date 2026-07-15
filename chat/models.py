from django.db import models


class Mensagem(models.Model):
    sala = models.CharField(max_length=50, default='geral', db_index=True)
    nome = models.CharField(max_length=50, verbose_name='Nome')
    texto = models.CharField(max_length=500, verbose_name='Mensagem')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'

    def __str__(self):
        return f'{self.nome}: {self.texto[:40]}'
