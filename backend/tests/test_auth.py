import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TestAuth:
    url_login = "/api/auth/token/login/"
    url_logout = "/api/auth/token/logout/"
    url_users_me = "/api/users/me/"

    @pytest.mark.django_db(transaction=True)
    def test_auth_login__invalid_request_data(self, user_client):
        url = self.url_login
        response = user_client.post(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без параметров, "
            f"возвращается код {code_expected}"
        )

        password_invalid = "invalid pwd"
        email_invalid = "invalid_email_not_exists"
        data_invalid = {
            "password": password_invalid,
            "email": email_invalid,
        }
        response = user_client.post(url, data=data_invalid)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с некорректными параметрами, "
            f"возвращается код {code_expected}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_login__valid_request_data(self, user_client, user):
        url = self.url_login
        password = ("1234567",)
        valid_data = {"email": user.email, "password": password}
        response = user_client.post(url, data=valid_data)
        code_expected = status.HTTP_201_CREATED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с валидными данными, "
            f"возвращается код {code_expected}"
        )
        token_field = "auth_token"
        assert token_field in response.json(), (
            f"Убедитесь, что при запросе `{url}` с валидными данными, "
            f"данные с токеном {token_field}"
        )
        url = self.url_users_me
        token = response.json().get(token_field)
        code_expected = status.HTTP_200_OK
        headers = {
            "HTTP_AUTHORIZATION": f"Token {token}",
        }
        response = user_client.get(url, **headers)
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся аутентификацей, "
            f"возвращается код {code_expected}."
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_logout__auth_was_not_provided(self, user_client):
        url = self.url_logout
        headers = {"HTTP_WWW_AUTHENTICATE": "Token"}
        response = user_client.post(url, **headers)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без имеющейся аутентификации, "
            f"возвращается код {code_expected}."
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_logout__auth_was_provided(self, user_client, user):
        url = self.url_login
        password = ("1234567",)
        valid_data = {"email": user.email, "password": password}
        response = user_client.post(url, data=valid_data)
        field_in_response = "auth_token"
        token = response.json().get(field_in_response)
        url = self.url_logout
        code_expected = status.HTTP_201_CREATED
        headers = {
            "HTTP_AUTHORIZATION": f"Token {token}",
        }
        response = user_client.post(url, **headers)
        code_expected = status.HTTP_204_NO_CONTENT
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся аутентификацией, "
            f"возвращается код {code_expected}."
        )
