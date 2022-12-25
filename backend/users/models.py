from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(
        max_length=254,
        verbose_name='Почта',
        help_text='Введите адрес электронной почты',
    )

    def get_name(self):
        return self.get_full_name() or self.get_username()

    class Meta:
        db_table = 'auth_user'
