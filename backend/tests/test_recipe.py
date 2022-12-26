from django.db import models

from recipes.models import RecipeIngredient
from tags.models import Tag
from tests.utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, "Не найдена модель `User` в приложении `users`"
try:
    from tags.models import Tag
except ImportError:
    assert False, "Не найдена модель `Tag` в приложении `tags`"
try:
    from recipes.models import RecipeIngredient
except ImportError:
    assert False, "Не найдена модель `RecipeIngredient` в приложении `recipes`"
try:
    from recipes.models import Recipe
except ImportError:
    assert False, "Не найдена модель `Recipe` в приложении `recipes`"


class TestRecipe:
    MODEL = Recipe
    MODEL_FIELDS = {
        "created": (models.DateTimeField, None),
        "author": (models.ForeignKey, User),
        "name": (models.CharField, None),
        "image": (models.ImageField, None),
        "text": (models.TextField, None),
        "cooking_time": (models.PositiveIntegerField, None),
        "ingredients": (models.ManyToManyField, RecipeIngredient),
        "tags": (models.ManyToManyField, Tag),
        "favorites": (models.ManyToManyField, User),
        "carts": (models.ManyToManyField, User),
    }

    def test_recipe_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
