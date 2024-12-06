
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class Category(models.Model):
    """
    Categoria das transações, como 'Aluguel', 'Salário', 'Investimentos', etc.
    """
    TYPE_CHOICES = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Tipo")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """
    Representa uma transação, seja uma receita ou despesa.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="transactions",
        verbose_name="Categoria"
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="Valor"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    date = models.DateField(verbose_name="Data da Transação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    TRANSACTION_TYPE = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    ]
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPE, 
        verbose_name="Tipo de Transação"
    )

    class Meta:
        ordering = ['-date']
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.get_transaction_type_display()} - R$ {self.amount} em {self.date}"

    def clean(self):
        """
        Validações personalizadas antes de salvar a transação.
        """
        # Verificar se o tipo da categoria corresponde ao tipo da transação
        if self.category and self.category.type != self.transaction_type:
            raise ValidationError(
                _("O tipo da transação ('%(transaction_type)s') não corresponde ao tipo da categoria ('%(category_type)s')."),
                params={
                    'transaction_type': self.get_transaction_type_display(),
                    'category_type': self.category.get_type_display(),
                },
            )

        # Verificar valores negativos para despesas
        if self.transaction_type == 'expense' and self.amount <= 0:
            raise ValidationError(_("Despesas devem ter um valor positivo."))

        # Verificar valores negativos para receitas
        if self.transaction_type == 'income' and self.amount <= 0:
            raise ValidationError(_("Receitas devem ter um valor positivo."))

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para aplicar as validações.
        """
        self.clean()
        super().save(*args, **kwargs)
