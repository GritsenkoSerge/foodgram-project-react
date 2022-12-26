from django.db import models

from tests.utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, "Не найдена модель `User` в приложении `users`"
try:
    from users.models import Subscription
except ImportError:
    assert False, "Не найдена модель `Subscription` в приложении `users`"


class TestSubscription:
    MODEL = Subscription
    MODEL_FIELDS = {
        "user": (models.ForeignKey, User),
        "author": (models.ForeignKey, User),
    }

    def test_subscription_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
