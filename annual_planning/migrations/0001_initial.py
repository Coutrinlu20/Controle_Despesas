# Generated by Django 5.1.2 on 2024-12-14 18:11

import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanejamentoAnual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.PositiveIntegerField(verbose_name='Ano do Planejamento')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planejamentos_anuais', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Planejamento Anual',
                'verbose_name_plural': 'Planejamentos Anuais',
                'ordering': ['-ano'],
                'unique_together': {('usuario', 'ano')},
            },
        ),
        migrations.CreateModel(
            name='CategoriaPlanejamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome da Categoria')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('orcamento_planejado', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Orçamento Planejado')),
                ('gasto_real', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, verbose_name='Gasto Real')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('planejamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='annual_planning.planejamentoanual', verbose_name='Planejamento Anual')),
            ],
            options={
                'verbose_name': 'Categoria de Planejamento',
                'verbose_name_plural': 'Categorias de Planejamento',
                'ordering': ['nome'],
                'unique_together': {('planejamento', 'nome')},
            },
        ),
    ]