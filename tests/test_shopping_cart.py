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
try:
    from recipes.models import ShoppingCart
except ImportError:
    assert False, 'Не найдена модель `ShoppingCart` в приложении `recipes`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestShoppingCart:
    MODEL = ShoppingCart
    FIELDS = {
        'recipe': (fields.ForeignKey, Recipe),
        'user': (fields.ForeignKey, User),
    }

    def test_shopping_cart_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
