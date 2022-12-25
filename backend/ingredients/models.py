from django.db import models


class Ingredient(models.Model):
    name = models.CharField("Имя", unique=True, max_length=200, help_text="Введите имя")
    measurement_unit = models.CharField(
        "Единица измерения", max_length=200, help_text="Введите единицу измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
