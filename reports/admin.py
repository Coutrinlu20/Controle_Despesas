from django.contrib import admin
from reports.models import Relatorio, LogRelatorio

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('id_relatorio', 'usuario', 'tipo', 'status', 'data_solicitacao', 'data_conclusao')
    list_filter = ('tipo', 'status', 'data_solicitacao')
    search_fields = ('usuario__username', 'tipo')
    readonly_fields = ('id_relatorio', 'data_solicitacao', 'data_conclusao')


@admin.register(LogRelatorio)
class LogRelatorioAdmin(admin.ModelAdmin):
    list_display = ('relatorio', 'mensagem', 'data')
    list_filter = ('data',)
    search_fields = ('relatorio__id_relatorio', 'mensagem')

