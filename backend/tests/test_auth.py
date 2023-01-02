import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TestAuth:
    url_login = "/api/auth/token/login/"
    url_logout = "/api/auth/token/logout/"
    url_users_me = "/api/users/me/"

    @pytest.mark.django_db(transaction=True)
    def test_auth_login__invalid_request_data(self, client):
        url = self.url_login
        response = client.post(url)
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
        response = client.post(url, data=data_invalid)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с некорректными параметрами, "
            f"возвращается код {code_expected}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_login__valid_request_data(self, client, user, user_password):
        url = self.url_login
        valid_data = {"email": user.email, "password": user_password}
        response = client.post(url, data=valid_data)
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
        response = client.get(url, **headers)
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся аутентификацей, "
            f"возвращается код {code_expected}."
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_logout__auth_was_not_provided(self, client):
        url = self.url_logout
        response = client.post(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без имеющейся аутентификации, "
            f"возвращается код {code_expected}."
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_logout__auth_was_provided(self, api_client):
        url = self.url_logout
        code_expected = status.HTTP_201_CREATED
        response = api_client.post(url)
        code_expected = status.HTTP_204_NO_CONTENT
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся аутентификацией, "
            f"возвращается код {code_expected}."
        )
