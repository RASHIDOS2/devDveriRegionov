from django.db import models
from catalogs.models import Products, Characteristics


# Create your models here.


class Prices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT, verbose_name='Номенклатура',
                                related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', blank=True, default=0)
    characteristic = models.ForeignKey(Characteristics, on_delete=models.PROTECT, verbose_name='Характеристика',
                                       default=None, blank=True, null=True, related_name='characteristic_prices')

    def __str__(self):
        return f'{self.product} - {self.characteristic} - {self.price}'

    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайс'
