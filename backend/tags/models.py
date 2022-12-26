from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        "Название",
        unique=True,
        max_length=settings.NAME_MAX_LENGTH,
        help_text="Введите название",
    )
    # TODO сделать валидатор на цвет
    color = models.CharField(
        "Цвет",
        max_length=settings.COLOR_MAX_LENGTH,
        help_text="Введите цвет в HEX (#rrggbb)",
    )
    slug = models.SlugField(
        "Slug", max_length=settings.SLUG_MAX_LENGTH, help_text="Введите slug"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
