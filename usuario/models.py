from django.db import models
from datetime import datetime

class Usuario(models.Model):
    nome_user = models.CharField(max_length=150, unique=True)
    email_user = models.EmailField(unique=True)
    senha_user =  models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)# esta_ativo
    created_at = models.DateTimeField(auto_now_add=True)# Criado_em


    def __str__(self):
        return f"Usuario [nome_user={self.nome_user}]"
