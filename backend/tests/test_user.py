from django.contrib.auth import get_user_model
from django.db import models

from .utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель `User` в приложении `users`'


class TestUser:
    MODEL = User
    MODEL_FIELDS = {
        'email': (models.EmailField, None),
        'username': (models.CharField, None),
        'first_name': (models.CharField, None),
        'last_name': (models.CharField, None),
    }

    def test_user_model(self):
        assert User == get_user_model(), (
            'Модели `User` должна возвращаться get_user_model()'
        )

        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
