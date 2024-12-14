from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class PlanejamentoAnual(models.Model):
    """
    Modelo que representa um planejamento anual.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="planejamentos_anuais"
    )
    ano = models.PositiveIntegerField(verbose_name="Ano do Planejamento")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Planejamento Anual"
        verbose_name_plural = "Planejamentos Anuais"
        unique_together = ('usuario', 'ano')
        ordering = ['-ano']

    def __str__(self):
        return f"Planejamento Anual {self.ano} ({self.usuario.username})"

    def total_planejado(self):
        """
        Calcula o total planejado para todas as categorias.
        """
        return sum(categoria.orcamento_planejado for categoria in self.categorias.all())

    def total_gasto(self):
        """
        Calcula o total gasto em todas as categorias.
        """
        return sum(categoria.gasto_real for categoria in self.categorias.all())


class CategoriaPlanejamento(models.Model):
    """
    Modelo que representa uma categoria dentro do planejamento anual.
    """
    planejamento = models.ForeignKey(
        PlanejamentoAnual,
        on_delete=models.CASCADE,
        verbose_name="Planejamento Anual",
        related_name="categorias"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    orcamento_planejado = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Orçamento Planejado"
    )
    gasto_real = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Gasto Real"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Categoria de Planejamento"
        verbose_name_plural = "Categorias de Planejamento"
        unique_together = ('planejamento', 'nome')
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.planejamento.ano})"

    def saldo(self):
        """
        Calcula o saldo restante para a categoria.
        """
        return self.orcamento_planejado - self.gasto_real

    def clean(self):
        """
        Regras de validação:
        - O orçamento planejado deve ser maior que zero.
        - O gasto real não pode ser maior que o orçamento planejado.
        """
        if self.orcamento_planejado <= 0:
            raise ValidationError(_("O orçamento planejado deve ser maior que zero."))

        if self.gasto_real > self.orcamento_planejado:
            raise ValidationError(_("O gasto real não pode exceder o orçamento planejado."))

