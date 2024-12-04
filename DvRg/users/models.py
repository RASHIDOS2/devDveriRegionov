import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    COMPANY = 'COMP'
    PRIVATE_PERSON = 'PRIV'
    COMPANY_PRIVATE = [
        (COMPANY, 'Компания'),
        (PRIVATE_PERSON, 'Частное лицо')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=250,
                                 blank=True,
                                 unique=True,
                                 null=True)
    status = models.CharField(verbose_name='Юр/Физлицо', max_length=50, choices=COMPANY_PRIVATE, default=COMPANY)
    