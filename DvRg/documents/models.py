import uuid
from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from catalogs.models import CounterParty, Organizations, Agreement, Contract, Products, Characteristics


class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(verbose_name='Date')
    number = models.CharField(verbose_name='Номер', max_length=128)

    partner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Партнер', default=None,
                                related_name='partner_order')

    counterparty = models.ForeignKey(CounterParty, on_delete=models.PROTECT, verbose_name='Контрагент', default=None,
                                     related_name='counterparty_order')

    organization = models.ForeignKey(Organizations, on_delete=models.PROTECT, verbose_name='Организация', default=None,
                                     related_name='organization_order')

    agreement = models.ForeignKey(Agreement, on_delete=models.PROTECT, verbose_name='Соглашения', default=None,
                                  related_name='agreement_order', blank=True, null=True)

    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, verbose_name='Договор', default=None,
                                 related_name='contract_order', blank=True, null=True)

    def __str__(self):
        return f'Заказ клиента №{self.number} от {self.date} - {self.partner}'

    class Meta:
        verbose_name = 'Заказ клиента'
        verbose_name_plural = 'Заказы клиента'


class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT, verbose_name='Заказ клиента', default=None,
                              related_name='order_orders_detail')

    product = models.ForeignKey(Products, on_delete=models.PROTECT, verbose_name='Номенклатура', default=None,
                                related_name='product_orders_detail')

    characteristic = models.ForeignKey(Characteristics, on_delete=models.PROTECT, verbose_name='Характеристика',
                                       default=None, blank=True,
                                       related_name='characteristics_orders_detail')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    quntity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')

    def __str__(self):
        return f'Заказ клиента №{self.order.number} от {self.order.date} - {self.product}'

    class Meta:
        verbose_name = 'Заказ клиента (товары)'
        verbose_name_plural = 'Заказы клиента (товары)'
