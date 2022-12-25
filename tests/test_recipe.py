from django.db.models import fields

from tests.utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель `User` в приложении `users`'
try:
    from recipes.models import Recipe
except ImportError:
    assert False, 'Не найдена модель `Recipe` в приложении `recipes`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestRecipe:
    MODEL = Recipe
    FIELDS = {
        'author': (fields.ForeignKey, User),
        'name': (fields.CharField, None),
        'image': (fields.ImageField, None),
        'text': (fields.CharField, None),
        'cooking_time': (fields.PositiveIntegerField, None),
    }

    def test_recipe_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
