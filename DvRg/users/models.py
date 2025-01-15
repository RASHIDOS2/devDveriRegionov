import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(verbose_name="Наименование полное", max_length=250)

    def set_random_password(self):
        password = BaseUserManager.make_random_password(8)
        self.set_password(password)
        self.save()
        return password

    def send_wellcome(self, password):
        subject = 'Регистрация в личном кабинете www.nizamovschool.xyz'
        html_message = render_to_string('users/email_wellcome.html', {
            'user': self,
            'domain': 'www.nizamovschool.xyz',
            'password': password
        })
        from_email = 'admin <test1s2015@yandex.ru>'
        to_email = self.email
        email = EmailMessage(subject, html_message, from_email, [to_email])
        email.content_subtype = 'html'
        email.send()

    def __str__(self):
        return '{}'.format(self.full_name)
