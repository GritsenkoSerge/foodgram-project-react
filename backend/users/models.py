from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        "Имя пользователя",
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        help_text=(
            "Введите уникальное имя пользователя. Максимум 150 символов. "
            "Используйте только английские буквы, цифры и символы @/./+/-/_"
        ),
        validators=[ASCIIUsernameValidator()],
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        help_text="Введите адрес электронной почты",
        validators=[ASCIIUsernameValidator()],
        error_messages={
            "unique": "Пользователь с такой почтой уже существует",
        },
    )
    first_name = models.CharField(
        "Имя", max_length=settings.FIRST_NAME_MAX_LENGTH, help_text="Введите имя"
    )
    last_name = models.CharField(
        "Фамилия", max_length=settings.LAST_NAME_MAX_LENGTH, help_text="Введите фамилию"
    )

    def get_name(self):
        return self.get_full_name() or self.get_username()

    class Meta:
        db_table = "auth_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserRelated(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
        related_name="+",
    )

    class Meta:
        abstract = True


class AuthorRelated(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите автора",
        related_name="+",
    )

    class Meta:
        abstract = True


class Subscription(AuthorRelated, UserRelated):
    class Meta(AuthorRelated.Meta, UserRelated.Meta):
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
