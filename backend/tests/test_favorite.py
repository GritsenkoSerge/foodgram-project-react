from django.db import models

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
    from recipes.models import Favorite
except ImportError:
    assert False, 'Не найдена модель `Favorite` в приложении `recipes`'


class TestFavorite:
    MODEL = Favorite
    MODEL_FIELDS = {
        'recipe': (models.ForeignKey, Recipe),
        'user': (models.ForeignKey, User),
    }

    def test_favorite_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
