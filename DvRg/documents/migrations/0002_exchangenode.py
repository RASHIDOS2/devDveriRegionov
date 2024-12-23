# Generated by Django 5.1.3 on 2024-12-23 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(verbose_name='Дата и время изменения')),
                ('order', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='order_exchange_node', to='documents.orders', verbose_name='Заказ покупателя')),
            ],
            options={
                'verbose_name': 'Измененный заказ',
                'verbose_name_plural': 'Измененные заказы',
            },
        ),
    ]