from django.db.models import fields

from tests.utils import check_model_field_names

try:
    from recipes.models import Recipe
except ImportError:
    assert False, 'Не найдена модель `Recipe` в приложении `recipes`'
try:
    from ingredients.models import Ingredient
except ImportError:
    assert False, 'Не найдена модель `Ingredient` в приложении `ingredients`'
try:
    from recipes.models import RecipeIngredient
except ImportError:
    assert False, 'Не найдена модель `RecipeIngredient` в приложении `recipes`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestRecipeIngredient:
    MODEL = RecipeIngredient
    FIELDS = {
        'recipe': (fields.ForeignKey, Recipe),
        'ingredient': (fields.ForeignKey, Ingredient),
        'amount': (fields.PositiveIntegerField, None),
    }

    def test_recipe_tag_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
