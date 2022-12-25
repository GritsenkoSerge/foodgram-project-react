from django.db.models import fields

from tests.utils import check_model_field_names

try:
    from ingredients.models import Ingredient
except ImportError:
    assert False, 'Не найдена модель `Ingredient` в приложении `ingredients`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestIngredient:
    MODEL = Ingredient
    FIELDS = {
        'name': (fields.CharField, None),
        'measurement_unit': (fields.CharField, None),
    }

    def test_ingredient_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
