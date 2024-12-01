from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)


class Despesas(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    descricao = models.CharField(max_length=100)
    quantia = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()


def __str__(self):
    return f"{self.descricao} - {self.quantia}"