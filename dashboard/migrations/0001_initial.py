# Generated by Django 5.1.2 on 2024-12-06 00:04

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
            name='DashboardChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chart_type', models.CharField(choices=[('line', 'Linha'), ('bar', 'Barra'), ('pie', 'Pizza')], default='line', max_length=10, verbose_name='Tipo de Gráfico')),
                ('title', models.CharField(max_length=100, verbose_name='Título do Gráfico')),
                ('data', models.JSONField(verbose_name='Dados do Gráfico')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_charts', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Gráfico do Dashboard',
                'verbose_name_plural': 'Gráficos do Dashboard',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DashboardNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Mensagem')),
                ('is_read', models.BooleanField(default=False, verbose_name='Lida')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Notificação do Dashboard',
                'verbose_name_plural': 'Notificações do Dashboard',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DashboardSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_income', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, verbose_name='Total de Receitas')),
                ('total_expense', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, verbose_name='Total de Despesas')),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, verbose_name='Balanço')),
                ('period_start', models.DateField(verbose_name='Início do Período')),
                ('period_end', models.DateField(verbose_name='Fim do Período')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_summaries', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Resumo do Dashboard',
                'verbose_name_plural': 'Resumos do Dashboard',
                'ordering': ['-period_start'],
            },
        ),
    ]
