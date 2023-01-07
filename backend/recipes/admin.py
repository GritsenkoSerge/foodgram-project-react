from django.conf import settings
from django.contrib import admin

from .models import Recipe, IngredientInRecipe


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
        "author",
        "name",
        "favorites",
    )
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
