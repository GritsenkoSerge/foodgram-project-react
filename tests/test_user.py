from django.contrib.auth import get_user_model
from django.db.models import fields

from .utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель `User` в приложении `users`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestUser:
    MODEL = User
    FIELDS = {
        'email': (fields.CharField, None),
        'username': (fields.CharField, None),
        'first_name': (fields.CharField, None),
        'last_name': (fields.CharField, None),
    }

    def test_user_model(self):
        assert User == get_user_model(), (
            'Модели `User` должна возвращаться get_user_model()'
        )

        check_model_field_names(self.MODEL, self.FIELDS)
