from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    created = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        help_text="Автоматически устанавливается текущая дата и время",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите из списка автора",
    )
    name = models.CharField(
        "Название", max_length=settings.NAME_MAX_LENGTH, help_text="Введите название"
    )
    image = models.ImageField(
        "Recipe image",
        upload_to="recipes/",
        help_text="Выберите картинку",
    )
    text = models.TextField(
        "Текстовое описание", help_text="Введите текстовое описание"
    )
    cooking_time = models.PositiveIntegerField(
        "Время приготовления в минутах",
        help_text="Введите время приготовления в минутах",
        validators=[
            MinValueValidator(1, message="Укажите время больше либо равное 1"),
        ],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Ингредиенты",
        help_text="Выберите ингредиенты",
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги", help_text="Выберите теги")
    favorites = models.ManyToManyField(
        User,
        verbose_name="Избранное",
        related_name="favorite_recipes",
        blank=True,
        help_text="Выберите пользователей, для добавления в избранное",
    )
    carts = models.ManyToManyField(
        User,
        verbose_name="Корзины",
        related_name="cart_recipes",
        blank=True,
        help_text="Выберите пользователей, для добавления в их корзины",
    )

    @admin.display(description="Число добавлений в избранное")
    def favorite_amount(self):
        return self.favorites.count()

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        default_related_name = "%(class)ss"
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.id=} {self.author=} {self.name=}"


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.RESTRICT,
        verbose_name="Ингредиент рецепта",
        help_text="Выберите ингредиент рецепта",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.RESTRICT,
        verbose_name="Ингредиент рецепта",
        help_text="Выберите ингредиент рецепта",
    )
    amount = models.PositiveIntegerField(
        "Количество ингридиента",
        help_text="Введите количество ингридиента",
        validators=[
            MinValueValidator(1, message="Укажите количество больше либо равное 1"),
        ],
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"
