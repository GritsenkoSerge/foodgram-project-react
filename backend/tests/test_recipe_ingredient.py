from django.db import models

from tests.utils import check_model_field_names

try:
    from recipes.models import Recipe
except ImportError:
    assert False, "Не найдена модель `Recipe` в приложении `recipes`"
try:
    from ingredients.models import Ingredient
except ImportError:
    assert False, "Не найдена модель `Ingredient` в приложении `ingredients`"
try:
    from recipes.models import RecipeIngredient
except ImportError:
    assert False, "Не найдена модель `RecipeIngredient` в приложении `recipes`"


class TestRecipeIngredient:
    MODEL = RecipeIngredient
    MODEL_FIELDS = {
        "recipe": (models.ForeignKey, Recipe),
        "ingredient": (models.ForeignKey, Ingredient),
        "amount": (models.PositiveIntegerField, None),
    }

    def test_recipe_tag_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
