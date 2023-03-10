import pytest
from django.db import models
from rest_framework import status

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
    URL_USERS_SUBSCRIPTIONS = "/api/users/subscriptions/"
    URL_USERS_SUBSCRIBE = "/api/users/{}/subscribe/"

    def test_subscription_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)

    # get /api/users/subscriptions/ 401
    @pytest.mark.django_db(transaction=True)
    def test_subscription__unauthorized_get(self, client):
        url = self.URL_USERS_SUBSCRIPTIONS
        response = client.get(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без имеющейся авторизации, "
            f"возвращается код {code_expected}."
        )

    # get /api/users/subscriptions/ 200
    @pytest.mark.django_db(transaction=True)
    def test_subscription__authorized_get(
        self, api_client, subscription, denied_recipe, one_more_denied_recipe
    ):
        url = self.URL_USERS_SUBSCRIPTIONS
        response = api_client.get(url)
        code_expected = status.HTTP_200_OK
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся авторизацией, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert (
            json.get("count") == 1
        ), f"Убедитесь, что при запросе `{url}`, возвращается одна подписка."
        results = json.get("results")
        assert (
            isinstance(results, list) and len(results) == 1
        ), f"Убедитесь, что при запросе `{url}`, возвращается одна подписка."
        assert results[0].get("recipes_count") == 2, (
            f"Убедитесь, что при запросе `{url}`, возвращается одна подписка "
            " с двумя рецептами."
        )
        recipes = results[0].get("recipes")
        assert isinstance(recipes, list) and len(recipes) == 2, (
            f"Убедитесь, что при запросе `{url}`, возвращается одна подписка "
            " со списокм из двух рецептов."
        )
        url = self.URL_USERS_SUBSCRIPTIONS + "?recipes_limit=1"
        response = api_client.get(url)
        code_expected = status.HTTP_200_OK
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся авторизацией, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        results = json.get("results")
        assert (
            isinstance(results, list) and len(results) == 1
        ), f"Убедитесь, что при запросе `{url}`, возвращается одна подписка."
        recipes = results[0].get("recipes")
        assert isinstance(recipes, list) and len(recipes) == 1, (
            f"Убедитесь, что при запросе `{url}`, возвращается одна подписка "
            " со списокм из одного рецепта."
        )

    # post /api/users/{id}/subscribe/ 401
    @pytest.mark.django_db(transaction=True)
    def test_subscription__unauthorized_post(self, client, user):
        url = self.URL_USERS_SUBSCRIBE.format(user.id)
        response = client.post(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без имеющейся авторизации, "
            f"возвращается код {code_expected}."
        )

    # post /api/users/{id}/subscribe/ 400
    @pytest.mark.django_db(transaction=True)
    def test_subscription__authorized_invalid_post(
        self, api_client, user, subscription
    ):
        url = self.URL_USERS_SUBSCRIBE.format(user.id)
        response = api_client.post(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}`, "
            f"на подписку на самого себя, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert json.get(
            "errors"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."
        url = self.URL_USERS_SUBSCRIBE.format(subscription.author.id)
        response = api_client.post(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}`, "
            f"на уже имеющуюся подписку, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert json.get(
            "errors"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # post /api/users/{id}/subscribe/ 404
    @pytest.mark.django_db(transaction=True)
    def test_subscription__authorized_not_found_post(self, api_client):
        not_found_id = "404"
        url = self.URL_USERS_SUBSCRIBE.format(not_found_id)
        response = api_client.post(url)
        code_expected = status.HTTP_404_NOT_FOUND
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` "
            f"на подписку на несуществующего пользователя, "
            f"возвращается код {code_expected}."
        )

    # post /api/users/{id}/subscribe/ 201
    @pytest.mark.django_db(transaction=True)
    def test_subscription__authorized_valid_post(self, api_client, one_more_user):
        url = self.URL_USERS_SUBSCRIBE.format(one_more_user.id)
        response = api_client.post(url)
        code_expected = status.HTTP_201_CREATED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся авторизацией, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert json.get("is_subscribed"), (
            f"Убедитесь, что при запросе `{url}`, возвращается данные пользователя, "
            "на которого подписались, с is_subscribed=true."
        )

    # delete /api/users/{id}/subscribe/ 204
    @pytest.mark.django_db(transaction=True)
    def test_subscription__valid_delete(self, api_client, another_user, subscription):
        url = self.URL_USERS_SUBSCRIBE.format(another_user.id)
        response = api_client.delete(url)
        code_expected = status.HTTP_204_NO_CONTENT
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся авторизацией, "
            f"возвращается код {code_expected}."
        )
        assert (
            not response.content
        ), f"Убедитесь, что при запросе `{url}`, возвращается пустой content."

    # delete /api/users/{id}/subscribe/ 400
    @pytest.mark.django_db(transaction=True)
    def test_subscription__invalid_delete(self, api_client, one_more_user):
        url = self.URL_USERS_SUBSCRIBE.format(one_more_user.id)
        response = api_client.delete(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся авторизацией, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert json.get(
            "errors"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/users/{id}/subscribe/ 401
    @pytest.mark.django_db(transaction=True)
    def test_subscription__unauthorized_delete(
        self, client, another_user, subscription
    ):
        url = self.URL_USERS_SUBSCRIBE.format(another_user.id)
        response = client.delete(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без авторизации, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/users/{id}/subscribe/ 404
    @pytest.mark.django_db(transaction=True)
    def test_subscription__not_found_delete(self, api_client):
        not_found_id = "404"
        url = self.URL_USERS_SUBSCRIBE.format(not_found_id)
        response = api_client.delete(url)
        code_expected = status.HTTP_404_NOT_FOUND
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` "
            f"на отписку от несуществующего пользователя, "
            f"возвращается код {code_expected}."
        )
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."
