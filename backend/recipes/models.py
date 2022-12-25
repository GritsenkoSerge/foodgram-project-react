from django.contrib.auth import get_user_model
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import AuthorRelated, UserRelated

User = get_user_model()


class Recipe(AuthorRelated):
    name = models.CharField("Название", max_length=200, help_text="Введите название")
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/",
        help_text="Выберите картинку",
    )
    text = models.CharField(
        "Текстовое описание", max_length=200, help_text="Введите текстовое описание"
    )
    cooking_time = models.PositiveIntegerField(
        "Время приготовления в минутах",
        help_text="Введите время приготовления в минутах",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeRelated(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
    )


class Favorite(RecipeRelated, UserRelated):
    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранный рецепты"


class RecipeIngredient(RecipeRelated):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.RESTRICT,
        verbose_name="Ингредиент рецепта",
        help_text="Выберите ингредиент рецепта",
    )
    amount = models.PositiveIntegerField(
        "Количество ингридиента", help_text="Введите количество ингридиента"
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"


class RecipeTag(RecipeRelated):
    tag = models.ForeignKey(
        Tag, on_delete=models.RESTRICT, verbose_name="Тег", help_text="Выберите тег"
    )

    class Meta:
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецептов"


class ShoppingCart(RecipeRelated, UserRelated):
    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
