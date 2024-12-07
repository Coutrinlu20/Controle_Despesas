from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Meta(models.Model):
    """
    Modelo que representa uma meta financeira.
    """
    STATUS_CHOICES = [
        ('em_progresso', 'Em Progresso'),
        ('alcançada', 'Alcançada'),
        ('não_alcançada', 'Não Alcançada'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="metas"
    )
    titulo = models.CharField(max_length=255, verbose_name="Título da Meta")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    valor_alvo = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Valor Alvo"
    )
    progresso = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Progresso Atual"
    )
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Término")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='em_progresso',
        verbose_name="Status"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Metas"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"Meta: {self.titulo} ({self.usuario.username})"

    def clean(self):
        """
        Regras de validação:
        - O valor-alvo deve ser maior que zero.
        - O progresso não pode ser maior que o valor-alvo.
        - A data de início deve ser anterior à data de término.
        """
        if self.valor_alvo <= 0:
            raise ValidationError(_("O valor alvo deve ser maior que zero."))

        if self.progresso > self.valor_alvo:
            raise ValidationError(_("O progresso não pode ser maior que o valor alvo."))

        if self.data_inicio > self.data_fim:
            raise ValidationError(_("A data de início deve ser anterior à data de término."))

    def save(self, *args, **kwargs):
        """
        Atualiza automaticamente o status com base no progresso.
        """
        if self.progresso >= self.valor_alvo:
            self.status = 'alcançada'
        elif self.data_fim < models.DateField.today() and self.progresso < self.valor_alvo:
            self.status = 'não_alcançada'
        else:
            self.status = 'em_progresso'

        self.clean()
        super().save(*args, **kwargs)


class RegistroMeta(models.Model):
    """
    Modelo para registrar contribuições ou alterações no progresso de uma meta.
    """
    meta = models.ForeignKey(
        Meta,
        on_delete=models.CASCADE,
        verbose_name="Meta",
        related_name="registros"
    )
    descricao = models.TextField(verbose_name="Descrição da Contribuição")
    valor = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Valor Contribuído"
    )
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")

    class Meta:
        verbose_name = "Registro de Meta"
        verbose_name_plural = "Registros de Metas"
        ordering = ['-data']

    def __str__(self):
        return f"Registro de {self.valor} para a meta: {self.meta.titulo}"

    def clean(self):
        """
        Regras de validação:
        - O valor contribuído deve ser maior que zero.
        - A contribuição não pode exceder o valor restante para atingir a meta.
        """
        if self.valor <= 0:
            raise ValidationError(_("O valor contribuído deve ser maior que zero."))

        valor_restante = self.meta.valor_alvo - self.meta.progresso
        if self.valor > valor_restante:
            raise ValidationError(
                _("O valor contribuído excede o valor restante para atingir a meta.")
            )

    def save(self, *args, **kwargs):
        """
        Atualiza automaticamente o progresso da meta associada.
        """
        self.clean()
        super().save(*args, **kwargs)
        # Atualizar o progresso da meta
        self.meta.progresso += self.valor
        self.meta.save()
