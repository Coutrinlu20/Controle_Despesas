from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Divida(models.Model):
    """
    Modelo que representa uma dívida financeira.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('parcial', 'Parcialmente Paga'),
        ('liquidada', 'Liquidada'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="dividas"
    )
    credor = models.CharField(max_length=255, verbose_name="Credor")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    valor_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Valor Total"
    )
    valor_pago = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor Pago"
    )
    taxa_juros = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Taxa de Juros (%)"
    )
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Dívida"
        verbose_name_plural = "Dívidas"
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"Dívida com {self.credor} ({self.usuario.username})"

    def calcular_juros(self):
        """
        Calcula os juros acumulados com base na taxa de juros.
        """
        dias_atraso = (models.DateField.today() - self.data_vencimento).days
        if dias_atraso > 0 and self.taxa_juros > 0:
            return self.valor_total * (self.taxa_juros / 100) * dias_atraso / 365
        return Decimal('0.00')

    def clean(self):
        """
        Regras de validação:
        - O valor total deve ser maior que zero.
        - O valor pago não pode ser maior que o valor total.
        - A data de início deve ser anterior à data de vencimento.
        """
        if self.valor_total <= 0:
            raise ValidationError(_("O valor total deve ser maior que zero."))

        if self.valor_pago > self.valor_total:
            raise ValidationError(_("O valor pago não pode ser maior que o valor total."))

        if self.data_inicio > self.data_vencimento:
            raise ValidationError(_("A data de início deve ser anterior à data de vencimento."))

    def save(self, *args, **kwargs):
        """
        Atualiza automaticamente o status com base no valor pago.
        """
        if self.valor_pago >= self.valor_total:
            self.status = 'liquidada'
        elif self.valor_pago > 0:
            self.status = 'parcial'
        else:
            self.status = 'pendente'

        self.clean()
        super().save(*args, **kwargs)


class PagamentoDivida(models.Model):
    """
    Modelo para registrar pagamentos realizados em uma dívida.
    """
    divida = models.ForeignKey(
        Divida,
        on_delete=models.CASCADE,
        verbose_name="Dívida",
        related_name="pagamentos"
    )
    descricao = models.TextField(verbose_name="Descrição do Pagamento", blank=True, null=True)
    valor = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Valor Pago"
    )
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pagamento")

    class Meta:
        verbose_name = "Pagamento de Dívida"
        verbose_name_plural = "Pagamentos de Dívidas"
        ordering = ['-data']

    def __str__(self):
        return f"Pagamento de {self.valor} para a dívida: {self.divida.credor}"

    def clean(self):
        """
        Regras de validação:
        - O valor pago deve ser maior que zero.
        - O valor não pode exceder o saldo restante da dívida.
        """
        if self.valor <= 0:
            raise ValidationError(_("O valor pago deve ser maior que zero."))

        saldo_restante = self.divida.valor_total - self.divida.valor_pago
        if self.valor > saldo_restante:
            raise ValidationError(
                _("O valor pago excede o saldo restante da dívida.")
            )

    def save(self, *args, **kwargs):
        """
        Atualiza automaticamente o valor pago da dívida associada.
        """
        self.clean()
        super().save(*args, **kwargs)
        # Atualizar o valor pago na dívida
        self.divida.valor_pago += self.valor
        self.divida.save()

