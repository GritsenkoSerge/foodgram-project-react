from django.conf import settings
from django.contrib import admin

from .models import (
    Recipe,
    IngredientInRecipe,
    FavoriteRecipe,
    TagRecipe,
    ShoppingCartRecipe,
)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 0
    min_num = 1


class FavoriteRecipeInline(admin.TabularInline):
    model = FavoriteRecipe
    extra = 0


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 0
    min_num = 1


class ShoppingCartRecipeInline(admin.TabularInline):
    model = ShoppingCartRecipe
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    @admin.display(description="Число добавлений в избранное")
    def favorite_amount(self):
        """Число добавлений рецепта в избранное для вывода в админке."""
        return FavoriteRecipe.objects.filter(recipe=self.id).count()

    @admin.display(description="Игредиенты")
    def ingredients_in_recipe(self):
        """Ингредиенты рецепта для вывода в админке."""
        return ", ".join(map(str, self.ingredientinrecipe_set.all()))

    list_display = (
        "pk",
        "name",
        "author",
        ingredients_in_recipe,
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
    inlines = (
        IngredientInRecipeInline,
        FavoriteRecipeInline,
        TagRecipeInline,
        ShoppingCartRecipeInline,
    )
    readonly_fields = (favorite_amount,)
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "ingredient",
        "amount",
    )
    list_editable = ("amount",)
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
    list_filter = (
        "recipe",
        "tag",
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE
