from django.db import models
from django.utils import timezone


class Compra(models.Model):
    """
    Registra cada venda confirmada do produto digital (Kit Dev Pro).
    Pode ser alimentado via webhook (Kiwify/Hotmart) ou manualmente pelo admin.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('reembolsada', 'Reembolsada'),
        ('cancelada', 'Cancelada'),
    ]

    PLATAFORMA_CHOICES = [
        ('kiwify', 'Kiwify'),
        ('hotmart', 'Hotmart'),
        ('stripe', 'Stripe'),
        ('manual', 'Registro Manual'),
    ]

    produto = models.CharField(max_length=200, verbose_name='Produto', default='Kit Dev Pro')
    comprador_nome = models.CharField(max_length=200, verbose_name='Nome do comprador')
    comprador_email = models.EmailField(verbose_name='E-mail do comprador')
    valor = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Valor (R$)'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='aprovada', verbose_name='Status', db_index=True
    )
    plataforma = models.CharField(
        max_length=20, choices=PLATAFORMA_CHOICES,
        default='kiwify', verbose_name='Plataforma'
    )
    # ID externo da plataforma (Kiwify order ID, Hotmart purchase code, etc.)
    # null=True (não apenas blank=True) para que múltiplos registros manuais sem
    # referência externa não colidam com o unique= abaixo — MySQL permite vários
    # NULLs numa coluna única, mas trataria múltiplas strings vazias como duplicatas.
    referencia_externa = models.CharField(
        max_length=200, blank=True, null=True, unique=True,
        verbose_name='Referência externa',
        help_text='ID da transação na plataforma de pagamento'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Data da compra')
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f'{self.comprador_nome} — {self.produto} ({self.get_status_display()})'


class LeadOrcamento(models.Model):
    """
    Registra as solicitações de orçamento e consultoria recebidas via formulário público.
    """
    nome = models.CharField(max_length=200, verbose_name='Nome / Empresa')
    email = models.EmailField(verbose_name='E-mail')
    whatsapp = models.CharField(max_length=50, blank=True, verbose_name='WhatsApp')
    tipos_projeto = models.CharField(max_length=255, verbose_name='Tipos de Projeto')
    prazo = models.CharField(max_length=50, verbose_name='Prazo')
    suporte = models.CharField(max_length=50, verbose_name='Suporte')
    descricao = models.TextField(verbose_name='Descrição do Projeto')
    atendido = models.BooleanField(default=False, verbose_name='Atendido/Respondido')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio')

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Solicitação de Orçamento'
        verbose_name_plural = 'Solicitações de Orçamento'

    def __str__(self):
        return f'{self.nome} — {self.email} ({self.criado_em.strftime("%d/%m/%Y")})'

