from django.contrib import admin
from debts.models import Divida, PagamentoDivida

@admin.register(Divida)
class DividaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'credor', 'valor_total', 'valor_pago', 'status', 'data_vencimento')
    list_filter = ('usuario', 'status', 'data_vencimento')
    search_fields = ('credor', 'descricao', 'usuario__username')

@admin.register(PagamentoDivida)
class PagamentoDividaAdmin(admin.ModelAdmin):
    list_display = ('divida', 'valor', 'data', 'descricao')
    list_filter = ('divida', 'data')
    search_fields = ('divida__credor', 'descricao')
