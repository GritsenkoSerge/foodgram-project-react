from django.conf import settings
from django.contrib import admin

from .models import (
    Recipe,
    IngredientInRecipe,
    FavoriteRecipe,
    TagRecipe,
    ShoppingCartRecipe,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "author",
    )
    list_editable = (
        "name",
        "author",
    )
    search_fields = (
        "author",
        "name",
    )
    list_filter = (
        "name",
        "author",
        "tags",
    )
    readonly_fields = ("favorite_amount",)
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "ingredient",
        "amount",
    )
    list_editable = (
        "recipe",
        "ingredient",
        "amount",
    )
    list_filter = (
        "recipe",
        "ingredient",
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "user",
    )
    list_editable = (
        "recipe",
        "user",
    )
    list_filter = (
        "recipe",
        "user",
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(ShoppingCartRecipe)
class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "user",
    )
    list_editable = (
        "recipe",
        "user",
    )
    list_filter = (
        "recipe",
        "user",
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "tag",
    )
    list_editable = (
        "recipe",
        "tag",
    )
    list_filter = (
        "recipe",
        "tag",
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE
