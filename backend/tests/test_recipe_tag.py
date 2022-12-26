from django.db import models

from tests.utils import check_model_field_names

try:
    from recipes.models import Recipe
except ImportError:
    assert False, "Не найдена модель `Recipe` в приложении `recipes`"
try:
    from tags.models import Tag
except ImportError:
    assert False, "Не найдена модель `Tag` в приложении `tags`"
try:
    from recipes.models import RecipeTag
except ImportError:
    assert False, "Не найдена модель `RecipeTag` в приложении `recipes`"


class TestRecipeTag:
    MODEL = RecipeTag
    MODEL_FIELDS = {
        "recipe": (models.ForeignKey, Recipe),
        "tag": (models.ForeignKey, Tag),
    }

    def test_recipe_tag_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
