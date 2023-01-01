from pathlib import Path

import pytest
from django.utils.version import get_version
from mixer.backend.django import mixer as _mixer
from rest_framework.test import APIClient

from foodgram.settings import INSTALLED_APPS
from users.models import Subscription

BASE_DIR = Path(__file__).resolve().parent.parent.parent
root_dir_content = list(Path(BASE_DIR).iterdir())
PROJECT_DIR_NAME = "backend"
MANAGE_PATH = Path(BASE_DIR, PROJECT_DIR_NAME)
# проверяем, что в корне репозитория лежит папка с проектом
if MANAGE_PATH not in root_dir_content or not Path(MANAGE_PATH).is_dir():
    assert False, (
        f"В директории `{BASE_DIR}` не найдена папка "
        f"c проектом `{PROJECT_DIR_NAME}`. "
        f"Убедитесь, что у вас верная структура проекта."
    )

project_dir_content = list(Path(MANAGE_PATH).iterdir())
FILENAME = "manage.py"
MANAGE_FILE = Path(MANAGE_PATH, FILENAME)
# проверяем, что структура проекта верная, и manage.py на месте
if MANAGE_FILE not in project_dir_content:
    assert False, (
        f"В директории `{MANAGE_PATH}` не найден файл `{FILENAME}`. "
        f"Убедитесь, что у вас верная структура проекта."
    )

assert get_version() < "4.0.0", "Используйте версию Django < 4.0.0"

APPS = ["api", "users", "tags", "ingredients", "recipes"]
assert all(app in INSTALLED_APPS for app in APPS), (
    f'Зарегистрируйте приложения `{"`, `".join(APPS)}` ' f"в `settings.INSTALLED_APPS`"
)


@pytest.fixture
def url_login():
    return "/api/auth/token/login/"


@pytest.fixture
def user_password():
    return "123qwe!@#QWE"


@pytest.fixture
def user(django_user_model, user_password):
    return django_user_model.objects.create_user(
        username="TestUser",
        password=user_password,
        first_name="FirstName",
        last_name="LastName",
        email="e@mail.ru",
    )


@pytest.fixture
def api_client(user, user_password, url_login):
    client = APIClient()
    data = {"email": user.email, "password": user_password}
    response = client.post(url_login, data=data)
    token = response.json().get("auth_token")
    headers = {
        "HTTP_AUTHORIZATION": f"Token {token}",
    }
    client.credentials(**headers)
    return client


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def another_user(mixer):
    from django.contrib.auth.models import User

    return mixer.blend(User, username="AnotherUser")


@pytest.fixture
def subscription(mixer):
    return mixer.blend(Subscription, user=user, author=another_user)
