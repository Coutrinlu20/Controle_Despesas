from django.contrib import admin
from annual_planning.models import PlanejamentoAnual, CategoriaPlanejamento

@admin.register(PlanejamentoAnual)
class PlanejamentoAnualAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ano', 'criado_em', 'atualizado_em')
    list_filter = ('ano', 'usuario')
    search_fields = ('usuario__username',)


@admin.register(CategoriaPlanejamento)
class CategoriaPlanejamentoAdmin(admin.ModelAdmin):
    list_display = ('planejamento', 'nome', 'orcamento_planejado', 'gasto_real', 'saldo')
    list_filter = ('planejamento__ano', 'nome')
    search_fields = ('nome', 'descricao', 'planejamento__usuario__username')

