import re

from django.contrib.auth import get_user_model
from django.db.models import fields

try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель User'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """Поиск запуска"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


class TestUser:

    def test_user_model(self):
        assert User == get_user_model(), (
            'Модели `User` должна возвращаться get_user_model()'
        )

        model_fields = User._meta.fields

        email_field = search_field(model_fields, 'email')
        assert email_field is not None, 'Добавьте поле `email` модели `User`'
        assert type(email_field) == fields.CharField, (
            'Свойство `email` модели `User` '
            'должно быть текстовым `CharField`'
        )

        username_field = search_field(model_fields, 'username')
        assert username_field is not None, (
            'Добавьте поле `username` модели `User`'
        )
        assert type(username_field) == fields.CharField, (
            'Свойство `username` модели `User` '
            'должно быть текстовым `CharField`'
        )

        first_name_field = search_field(model_fields, 'first_name')
        assert first_name_field is not None, (
            'Добавьте поле `first_name` модели `User`'
        )
        assert type(first_name_field) == fields.CharField, (
            'Свойство `first_name` модели `User` '
            'должно быть текстовым `CharField`'
        )

        last_name_field = search_field(model_fields, 'last_name')
        assert last_name_field is not None, (
            'Добавьте поле `last_name` модели `User`'
        )
        assert type(last_name_field) == fields.CharField, (
            'Свойство `last_name` модели `User` '
            'должно быть текстовым `CharField`'
        )
