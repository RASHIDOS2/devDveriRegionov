# Generated by Django 5.1.3 on 2025-01-09 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0003_alter_products_use_characteristics'),
        ('price', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='characteristic',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='characteristic_prices', to='catalogs.characteristics', verbose_name='Характеристика'),
        ),
    ]
