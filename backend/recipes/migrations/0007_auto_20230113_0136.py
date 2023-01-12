# Generated by Django 3.2 on 2023-01-12 19:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_auto_20230113_0053"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientinrecipe",
            name="amount",
            field=models.PositiveSmallIntegerField(
                help_text="Введите количество ингридиента",
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="Укажите количество больше либо равное 1"
                    )
                ],
                verbose_name="Количество ингридиента",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveSmallIntegerField(
                help_text="Введите время приготовления в минутах",
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="Укажите время больше либо равное 1"
                    )
                ],
                verbose_name="Время приготовления в минутах",
            ),
        ),
    ]
