from django.contrib import admin
from .models import Meta, RegistroMeta

@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'valor_alvo', 'progresso', 'status', 'data_inicio', 'data_fim')
    list_filter = ('usuario', 'status', 'data_inicio', 'data_fim')
    search_fields = ('titulo', 'descricao', 'usuario__username')

@admin.register(RegistroMeta)
class RegistroMetaAdmin(admin.ModelAdmin):
    list_display = ('meta', 'valor', 'data', 'descricao')
    list_filter = ('meta', 'data')
    search_fields = ('meta__titulo', 'descricao')
