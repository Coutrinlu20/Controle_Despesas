from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class DashboardSummary(models.Model):
    """
    Modelo que armazena dados resumidos para o painel, como total de receitas, despesas e balanço.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Usuário", 
        related_name="dashboard_summaries"
    )
    total_income = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Total de Receitas"
    )
    total_expense = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Total de Despesas"
    )
    balance = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Balanço"
    )
    period_start = models.DateField(verbose_name="Início do Período")
    period_end = models.DateField(verbose_name="Fim do Período")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Resumo do Dashboard"
        verbose_name_plural = "Resumos do Dashboard"
        ordering = ['-period_start']

    def __str__(self):
        return f"Resumo de {self.period_start} a {self.period_end} para {self.user.username}"

    def clean(self):
        """
        Regras de validação:
        - O período de início deve ser anterior ao período de fim.
        - O balanço deve ser igual à receita menos a despesa.
        """
        if self.period_start > self.period_end:
            raise ValidationError(_("O início do período não pode ser posterior ao fim do período."))

        calculated_balance = self.total_income - self.total_expense
        if self.balance != calculated_balance:
            raise ValidationError(
                _("O balanço não corresponde ao total de receitas menos despesas. "
                  "Esperado: %(expected_balance)s, encontrado: %(actual_balance)s."),
                params={
                    'expected_balance': calculated_balance,
                    'actual_balance': self.balance,
                }
            )

    def save(self, *args, **kwargs):
        """
        Atualiza o balanço automaticamente antes de salvar.
        """
        self.balance = self.total_income - self.total_expense
        self.clean()
        super().save(*args, **kwargs)


class DashboardChart(models.Model):
    """
    Modelo que armazena configurações e dados de gráficos exibidos no painel.
    """
    CHART_TYPE_CHOICES = [
        ('line', 'Linha'),
        ('bar', 'Barra'),
        ('pie', 'Pizza'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Usuário", 
        related_name="dashboard_charts"
    )
    chart_type = models.CharField(
        max_length=10, 
        choices=CHART_TYPE_CHOICES, 
        default='line', 
        verbose_name="Tipo de Gráfico"
    )
    title = models.CharField(max_length=100, verbose_name="Título do Gráfico")
    data = models.JSONField(verbose_name="Dados do Gráfico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Gráfico do Dashboard"
        verbose_name_plural = "Gráficos do Dashboard"
        ordering = ['-created_at']

    def __str__(self):
        return f"Gráfico {self.title} para {self.user.username}"

    def clean(self):
        """
        Regras de validação:
        - Os dados do gráfico devem estar no formato JSON.
        """
        if not isinstance(self.data, dict):
            raise ValidationError(_("Os dados do gráfico devem estar no formato JSON válido."))


class DashboardNotification(models.Model):
    """
    Modelo que armazena notificações e alertas para exibição no dashboard.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Usuário", 
        related_name="dashboard_notifications"
    )
    message = models.TextField(verbose_name="Mensagem")
    is_read = models.BooleanField(default=False, verbose_name="Lida")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Notificação do Dashboard"
        verbose_name_plural = "Notificações do Dashboard"
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificação para {self.user.username}: {self.message[:30]}{'...' if len(self.message) > 30 else ''}"
