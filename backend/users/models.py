from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        help_text='Введите адрес электронной почты',
        validators=[ASCIIUsernameValidator()],
        error_messages={
            "unique": 'Пользователь с такой почтой уже существует',
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Введите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Введите фамилию'
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        help_text=(
            'Введите имя пользователя. Максимум 150 символов. '
            'Используйте только английские буквы, цифры и символы @/./+/-/_'
        ),
        validators=[ASCIIUsernameValidator()],
        error_messages={
            "unique": 'Пользователь с таким именем уже существует',
        },
    )

    def get_name(self):
        return self.get_full_name() or self.get_username()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserRelated(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )


class AuthorRelated(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Выберите автора'
    )


class Subscription(AuthorRelated, UserRelated):

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
