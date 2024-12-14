# Generated by Django 5.1.2 on 2024-12-14 18:00

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
            name='Divida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credor', models.CharField(max_length=255, verbose_name='Credor')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor Total')),
                ('valor_pago', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, verbose_name='Valor Pago')),
                ('taxa_juros', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5, verbose_name='Taxa de Juros (%)')),
                ('data_inicio', models.DateField(verbose_name='Data de Início')),
                ('data_vencimento', models.DateField(verbose_name='Data de Vencimento')),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('parcial', 'Parcialmente Paga'), ('liquidada', 'Liquidada')], default='pendente', max_length=15, verbose_name='Status')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dividas', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Dívida',
                'verbose_name_plural': 'Dívidas',
                'ordering': ['-data_vencimento'],
            },
        ),
        migrations.CreateModel(
            name='PagamentoDivida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição do Pagamento')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor Pago')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Pagamento')),
                ('divida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamentos', to='debts.divida', verbose_name='Dívida')),
            ],
            options={
                'verbose_name': 'Pagamento de Dívida',
                'verbose_name_plural': 'Pagamentos de Dívidas',
                'ordering': ['-data'],
            },
        ),
    ]
