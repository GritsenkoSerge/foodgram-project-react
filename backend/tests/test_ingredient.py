from django.db import models

from tests.utils import check_model_field_names

try:
    from ingredients.models import Ingredient
except ImportError:
    assert False, "Не найдена модель `Ingredient` в приложении `ingredients`"


class TestIngredient:
    MODEL = Ingredient
    MODEL_FIELDS = {
        "name": (models.CharField, None),
        "measurement_unit": (models.CharField, None),
    }

    def test_ingredient_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
