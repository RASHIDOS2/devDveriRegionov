import uuid
from django.db import models
from django.contrib.auth import get_user_model
from catalogs.models import Counterparty, Organization, Agreement, Contract, Products, Characteristics
from datetime import datetime


class SiteOrderStatus(models.TextChoices):
    CREATE = 'CR', 'Создан'
    WRITE = 'WR', 'Записан'
    PROCESS = 'PR', 'Обработан'
    CLOSE = 'CL', 'Закрыт'


class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    number = models.CharField(verbose_name="Номер", max_length=128, default='', blank=True, null=True)
    partner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Партнер', default=None,
                                related_name='partner_order', blank=True, null=True)
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, verbose_name='Контрагент', default=None,
                                     related_name='counterparty_order', blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Организация', default=None,
                                     related_name='organization_order', blank=True, null=True)
    agreement = models.ForeignKey(Agreement, on_delete=models.PROTECT, verbose_name='Соглашение', default=None,
                                  related_name='agreement_order', blank=True, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, verbose_name='Договор', default=None,
                                 related_name='contract_order', blank=True, null=True)
    site_status = models.CharField(verbose_name="Статус заказа на сайте",
                                   max_length=10, choices=SiteOrderStatus.choices,
                                   default=SiteOrderStatus.CREATE)

    def fix_exchange(self):
        exchange = ExchangeNode.objects.filter(order=self)
        if exchange:
            exchange_obj = exchange.get()
        else:
            exchange_obj = ExchangeNode()
        exchange_obj.order = self
        exchange_obj.updated_at = datetime.today()
        exchange_obj.save()

    def __str__(self):
        return 'Заказ клиента №{} от {} - {}'.format(self.number, self.date, self.partner)

    class Meta:
        verbose_name = 'Заказ клиента'
        verbose_name_plural = 'Заказы клиента'


class OrdersDetail(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ клиента', default=None,
                              related_name='order_orders_detail')
    product = models.ForeignKey(Products, on_delete=models.PROTECT, verbose_name='Номенклатура', default=None,
                                related_name='product_orders_detail')
    characteristic = models.ForeignKey(Characteristics, on_delete=models.PROTECT, verbose_name='Характеристика',
                                       default=None, blank=True, null=True,
                                       related_name='characteristic_orders_detail')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')

    def __str__(self):
        return 'Заказ клиента №{} от {} - {}'.format(self.order.number, self.order.date, self.product)

    class Meta:
        verbose_name = 'Заказ клиента (товары)'
        verbose_name_plural = 'Заказы клиента (товары)'


class ExchangeNode(models.Model):
    updated_at = models.DateTimeField(verbose_name="Дата и время изменения")
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ клиента', default=None,
                              related_name='order_exchange_node')

    def __str__(self):
        return 'Заказ клиента №{} от {} - {}'.format(self.order.number, self.order.date, self.updated_at)

    class Meta:
        verbose_name = 'Измененный заказ'
        verbose_name_plural = 'Измененные заказы'
