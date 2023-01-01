import pytest
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import status

from .utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, "Не найдена модель `User` в приложении `users`"


class TestUser:
    MODEL = User
    MODEL_FIELDS = {
        "email": (models.EmailField, None),
        "username": (models.CharField, None),
        "first_name": (models.CharField, None),
        "last_name": (models.CharField, None),
    }
    URL_USERS = r"/api/users/"
    URL_USERS_ME = r"/api/users/me/"
    URL_USERS_SET_PASSWORD = r"/api/users/set_password/"

    def test_user_model(self):
        assert (
            User == get_user_model()
        ), "Модели `User` должна возвращаться get_user_model()"

        check_model_field_names(self.MODEL, self.MODEL_FIELDS)

    @pytest.mark.django_db(transaction=True)
    def test_user_get(self, api_client):
        url = self.URL_USERS
        response = api_client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}` возвращается код {code_expected}."

    @pytest.mark.django_db(transaction=True)
    def test_user_post(self, client, user):
        password = "1234qwre!@#$QWER"
        url = self.URL_USERS
        data = {
            "email": "new" + user.email,
            "password": password,
            "first_name": user.first_name,
            "username": "new" + user.username,
            "last_name": user.last_name,
        }
        response = client.post(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с некорректными параметрами "
            f"возвращается код {code_expected}."
        )
        response = client.post(url, data=data)
        code_expected = status.HTTP_201_CREATED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"и корректными данными возвращается код {code_expected}."
        )
        assert response.json().get("email") == "new" + user.email, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"и корректными данными возвращается зарегистрированный пользователь."
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_id_get(self, client, api_client, user):
        url = f"{self.URL_USERS}0/"
        response = client.get(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без аутентификации "
            f"возвращается код {code_expected}."
        )
        response = api_client.get(url)
        code_expected = status.HTTP_404_NOT_FOUND
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` не существующего id "
            f"возвращается код {code_expected}."
        )
        url = f"{self.URL_USERS}{user.id}/"
        response = api_client.get(url)
        code_expected = status.HTTP_200_OK
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"возвращается код {code_expected}."
        )
        assert response.json().get("email") == user.email, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"и корректными данными возвращаются данные пользователя."
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_me_get(self, client, api_client, user):
        url = self.URL_USERS_ME
        response = client.get(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без аутентификации "
            f"возвращается код {code_expected}."
        )
        response = api_client.get(url)
        code_expected = status.HTTP_200_OK
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"возвращается код {code_expected}."
        )
        assert response.json().get("email") == user.email, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"возвращает данные пользователя."
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_set_password(self, client, api_client, user_password):
        url = self.URL_USERS_SET_PASSWORD
        response = client.post(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без аутентификации "
            f"возвращается код {code_expected}."
        )
        data = {}
        response = api_client.post(url, data=data)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с аутентификацией "
            f"и невалидными данными возвращается код {code_expected}."
        )
        required_fields = (
            "new_password",
            "current_password",
        )
        json = response.json()
        for field in required_fields:
            assert field in json, (
                f"Убедитесь, что при запросе `{url}` с невалидными данными "
                f"возвращается ошибка с указанием поля {field}."
            )
        data = {"new_password": "1234qwer!@#$QWER", "current_password": user_password}
        response = api_client.post(url, data=data)
        code_expected = status.HTTP_204_NO_CONTENT
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с валидными данными "
            f"возвращается код {code_expected}."
        )
