from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import uuid


class Relatorio(models.Model):
    """
    Modelo que representa um relatório no sistema.
    """
    TIPO_RELATORIO_CHOICES = [
        ('transacoes', 'Transações'),
        ('usuarios', 'Usuários'),
        ('contas', 'Contas'),
        ('customizado', 'Customizado'),
    ]

    STATUS_RELATORIO_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_processamento', 'Em Processamento'),
        ('concluido', 'Concluído'),
        ('falha', 'Falha'),
    ]

    id_relatorio = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID do Relatório"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário Solicitante",
        related_name="relatorios"
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_RELATORIO_CHOICES,
        verbose_name="Tipo de Relatório"
    )
    parametros = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Parâmetros Personalizados"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_RELATORIO_CHOICES,
        default='pendente',
        verbose_name="Status do Relatório"
    )
    caminho_arquivo = models.FileField(
        upload_to='relatorios/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Caminho do Arquivo"
    )
    data_solicitacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Solicitação"
    )
    data_conclusao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de Conclusão"
    )

    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"Relatório {self.tipo} - {self.usuario.username} ({self.get_status_display()})"

    def marcar_concluido(self, caminho_arquivo):
        """
        Marca o relatório como concluído e define o caminho do arquivo.
        """
        self.status = 'concluido'
        self.caminho_arquivo = caminho_arquivo
        self.data_conclusao = now()
        self.save()

    def marcar_falha(self, mensagem_erro):
        """
        Marca o relatório como falho e registra o erro nos parâmetros.
        """
        self.status = 'falha'
        self.parametros = {'erro': mensagem_erro}
        self.save()

    def clean(self):
        """
        Regras de validação:
        - Os parâmetros devem estar no formato JSON, se fornecidos.
        """
        if self.parametros and not isinstance(self.parametros, dict):
            raise ValidationError(_("Os parâmetros personalizados devem ser um objeto JSON válido."))


class LogRelatorio(models.Model):
    """
    Modelo para registrar logs de execução de relatórios.
    """
    relatorio = models.ForeignKey(
        Relatorio,
        on_delete=models.CASCADE,
        verbose_name="Relatório",
        related_name="logs"
    )
    mensagem = models.TextField(verbose_name="Mensagem")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data do Log")

    class Meta:
        verbose_name = "Log de Relatório"
        verbose_name_plural = "Logs de Relatórios"
        ordering = ['-data']

    def __str__(self):
        return f"Log {self.relatorio.id_relatorio} - {self.data}"

