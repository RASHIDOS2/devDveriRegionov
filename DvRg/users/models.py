import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=250,
                                 blank=True,
                                 unique=True,
                                 null=True)

    def __str__(self):
        return '{}'.format(self.full_name)


    