from django.db.models import fields

from tests.utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, 'Не найдена модель `User` в приложении `users`'
try:
    from users.models import Subscription
except ImportError:
    assert False, 'Не найдена модель `Subscription` в приложении `users`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestSubscription:
    MODEL = Subscription
    FIELDS = {
        'user': (fields.ForeignKey, User),
        'author': (fields.ForeignKey, User),
    }

    def test_subscription_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
