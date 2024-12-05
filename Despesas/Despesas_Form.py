from django import forms
from Despesas.models import Categoria, Despesas

class DespesasForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = ("categoria", "descricao", "quantia", "data",)

class CategoriaForm (forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nome", "descricao")