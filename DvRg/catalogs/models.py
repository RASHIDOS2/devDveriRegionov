from django.db import models
import uuid
from django.contrib.auth import get_user_model

# Create your models here.


class ProductsGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name="Наименование", max_length=250)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родитель',
                               related_name='products_group')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа номенклатуры'
        verbose_name_plural = 'Группы номенклатуры'


class UseCharacteristic(models.TextChoices):
    NOT_USE = 'NU', 'Не используются'
    GENERAL = 'GEN', 'Общие для вида номенклатуры'
    OTHER = 'OTH', 'Общие с другим видом номенклатуры'
    INDIVIDUAL = 'IND', 'Индивидуальные для номенклатуры'


class TypesOfProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид номенклатуры'
        verbose_name_plural = 'Виды номенклатуры'


class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(verbose_name="Наименование полное", max_length=250)
    group = models.ForeignKey(ProductsGroup, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Группа',
                              related_name='group_products')
    use_characteristics = models.CharField(verbose_name="Варианты использования характеристик номенклатуры",
                                           max_length=20, choices=UseCharacteristic.choices,
                                           default=UseCharacteristic.NOT_USE)
    type_of_product = models.ForeignKey(TypesOfProducts, on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Вид номенклатуры',
                                        related_name='type_of_product_products')
    description = models.TextField(verbose_name='Описание', max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'


def image_directory_path(instance, filename):
    return 'products_images/{}/{}'.format(instance.product.id, filename)


class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Номенклатура',
                                related_name='product_images')

    image = models.ImageField(verbose_name='Картинка', upload_to=image_directory_path, default=None)

    def __str__(self):
        return '{} - {}'.format(self.product, self.image)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинка'


class Characteristics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=150)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Номенклатура',
                                related_name='product_characteristics')
    type_of_product = models.ForeignKey(TypesOfProducts, on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Вид номенклатуры',
                                        related_name='type_of_product_characteristics')

    def __str__(self):
        return '{} ({}/{})'.format(self.name, self.product, self.type_of_product)

    class Meta:
        verbose_name = 'Характеристика номенклатуры'
        verbose_name_plural = 'Характеристики номенклатуры'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Counterparty(models.Model):
    COMPANY = 'COMP'
    PRIVATE_PERSON = 'PRIV'
    COMPANY_PRIVATE = [
        (COMPANY, 'Компания'),
        (PRIVATE_PERSON, 'Частное лицо')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Партнер', default=None,
                                related_name='partner_counterparty')
    name = models.CharField(verbose_name="Наименование", max_length=100, unique=True)
    full_name = models.CharField(verbose_name="Сокращенное юр. наименование", max_length=250, unique=True, null=True,
                                 blank=True)
    status = models.CharField(verbose_name="Юр/Физлицо", max_length=50, choices=COMPANY_PRIVATE, default=COMPANY)
    inn = models.CharField(verbose_name="ИНН", max_length=12)
    kpp = models.CharField(verbose_name="КПП", max_length=9, null=True, blank=True)

    def __str__(self):
        return '{} - {} {}/{}'.format(self.partner, self.name, self.inn, self.kpp)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class Agreement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=100)
    number = models.CharField(verbose_name="Номер", max_length=30)
    date = models.DateField(verbose_name="Дата")
    partner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Партнер', default=None,
                                related_name='partner_agreement', null=True, blank=True)
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, verbose_name='Контрагент', default=None,
                                     related_name='counterparty_agreement', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Организация', default=None,
                                     related_name='organization_agreement', null=True, blank=True)

    def __str__(self):
        return '{} №{} от {} - {}'.format(self.name, self.number, self.date, self.counterparty)

    class Meta:
        verbose_name = 'Соглашение об условиях продаж'
        verbose_name_plural = 'Соглашения об условиях продаж'


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=150)
    number = models.CharField(verbose_name="Номер", max_length=128)
    date = models.DateField(verbose_name="Дата")
    partner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Партнер', default=None,
                                related_name='partner_contract')
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, verbose_name='Контрагент', default=None,
                                     related_name='counterparty_contract')
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Организация', default=None,
                                     related_name='organization_contract')
    default = models.BooleanField(verbose_name='Использовать по умолчанию', default=False)

    def __str__(self):
        return '{} №{} от {}'.format(self.name, self.number, self.date)

    class Meta:
        verbose_name = 'Договор с контрагентом'
        verbose_name_plural = 'Договоры с контрагентами'
