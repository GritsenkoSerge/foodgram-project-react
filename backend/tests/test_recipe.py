from django.db import models

from tests.utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, "Не найдена модель `User` в приложении `users`"
try:
    from recipes.models import Recipe
except ImportError:
    assert False, "Не найдена модель `Recipe` в приложении `recipes`"


class TestRecipe:
    MODEL = Recipe
    MODEL_FIELDS = {
        "author": (models.ForeignKey, User),
        "name": (models.CharField, None),
        "image": (models.ImageField, None),
        "text": (models.CharField, None),
        "cooking_time": (models.PositiveIntegerField, None),
    }

    def test_recipe_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
