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
        on_delete=models.RESTRICT,
        verbose_name="Автор",
        help_text="Выберите из списка автора",
    )
    name = models.CharField(
        "Название", max_length=settings.NAME_MAX_LENGTH, help_text="Введите название"
    )
    image = models.ImageField(
        "Картинка",
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
    tags = models.ManyToManyField(
        Tag, through="TagRecipe", verbose_name="Теги", help_text="Выберите теги"
    )
    favorites = models.ManyToManyField(
        User,
        through="FavoriteRecipe",
        verbose_name="Избранное",
        related_name="favorite_recipes",
        blank=True,
        help_text="Выберите пользователей, для добавления в избранное",
    )
    shopping_carts = models.ManyToManyField(
        User,
        through="ShoppingCartRecipe",
        verbose_name="Корзины",
        related_name="shopping_cart_recipes",
        blank=True,
        help_text="Выберите пользователей, для добавления в их корзины",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        default_related_name = "%(class)ss"
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.id=} {self.author=} {self.name=}"

    @admin.display(description="Число добавлений в избранное")
    def favorite_amount(self):
        """Число добавлений рецепта в избранное для вывода в админке."""
        return self.favorites.count()


class TagRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.RESTRICT,
        verbose_name="Тег",
        help_text="Выберите из списка тег",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_recipe_tag",
                fields=["recipe", "tag"],
            ),
        ]


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите из списка автора",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_favorite",
                fields=["recipe", "user"],
            ),
        ]


class ShoppingCartRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите из списка автора",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_shopping_cart",
                fields=["recipe", "user"],
            ),
        ]


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
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

    def __str__(self) -> str:
        return f"{self.ingredient} — {self.amount}"
