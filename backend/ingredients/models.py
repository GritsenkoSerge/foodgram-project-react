from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        "Название",
        max_length=settings.NAME_MAX_LENGTH,
        help_text="Введите название",
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=settings.MEASUREMENT_UNIT_MAX_LENGTH,
        help_text="Введите единицу измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                name="unique_ingridient",
                fields=["name", "measurement_unit"],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.measurement_unit})"
