from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'Имя',
        unique=True,
        max_length=200,
        help_text='Введите имя'
    )
    # TODO сделать валидатор на цвет
    color = models.CharField(
        'Цвет',
        max_length=7,
        help_text='Введите цвет в HEX (#rrggbb)'
    )
    slug = models.SlugField(
        'Slug',
        max_length=200,
        help_text='Введите slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
