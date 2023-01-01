import pytest
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
    URL_USERS = "/api/users/"
    URL_SUBSCRIPTIONS = "/api/users/subscriptions/"

    def test_subscription_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)

    # get /api/users/subscriptions/ 200 401
    @pytest.mark.django_db(transaction=True)
    def test_subscription_get(self, client, user):
        ...

    # post /api/users/{id}/subscribe/ 201 400 401 404
    @pytest.mark.django_db(transaction=True)
    def test_subscription_post(self, client, user, another_user):
        ...

    # delete /api/users/{id}/subscribe/ 204 400 401 404
    @pytest.mark.django_db(transaction=True)
    def test_subscription_delete(self, client, user, another_user):
        ...
