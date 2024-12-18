import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=250,
                                 blank=True,
                                 unique=True,
                                 null=True)

    def set_random_password(self):
        password = BaseUserManager.make_random_password(8)
        self.set_password(password)
        self.save()
        return password

    def send_wellcome(self, password):
        subject = 'Регистрация в личном кабинете'
        html_message = render_to_string('users/email_welcome.html', {
            'user': self,
            'domain': 'www.dvernoymarket.xyz',
            'password': password
        })
        from_email = 'admin <tex1s2015@yandex.ru>'
        to_email = self.email
        email = EmailMessage(subject, html_message, from_email, [to_email])
        email.content_subtype = 'html'
        email.send()

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user.send_wellcome(validated_data['password'])
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

    def __str__(self):
        return f'{self.full_name}'
