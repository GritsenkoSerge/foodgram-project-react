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
        valid_data = {"email": user.email, "password": user.password}
        response = user_client.post(url, data=valid_data)
        code_expected = status.HTTP_201_CREATED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с валидными данными, "
            f"возвращается код {code_expected}"
        )
        field_in_response = "auth_token"
        assert field_in_response, (
            f"Убедитесь, что при запросе `{url}` с валидными данными, "
            f" в ответе возвращается код {code_expected} и данные с токеном"
        )
        url = self.url_users_me
        token = response.json().get(field_in_response)
        code_expected = status.HTTP_200_OK
        headers = {
            "Authorization": f"Token {token}",
        }
        response = user_client.post(url, headers=headers)
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся аутентификацей, "
            f"возвращается код {code_expected}."
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_logout__auth_was_not_provided(self, user_client):
        url = self.url_logout
        response = user_client.post(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` без имеющейся аутентификации, "
            f"возвращается код {code_expected}."
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_logout__auth_was_provided(self, user_client, user):
        url = self.url_login
        valid_data = {"email": user.email, "password": user.password}
        response = user_client.post(url, data=valid_data)
        field_in_response = "auth_token"
        token = response.json().get(field_in_response)
        url = self.url_logout
        code_expected = status.HTTP_201_CREATED
        headers = {
            "Authorization": f"Token {token}",
        }
        response = user_client.post(url, headers=headers)
        code_expected = status.HTTP_204_NO_CONTENT
        assert response.status_code == code_expected, (
            f"Убедитесь, что при запросе `{url}` с имеющейся аутентификацией, "
            f"возвращается код {code_expected}."
        )
