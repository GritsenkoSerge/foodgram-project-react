from pathlib import Path
import pytest

from django.utils.version import get_version

from foodgram.settings import INSTALLED_APPS

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
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="TestUser",
        password="1234567",
        first_name="FirstName",
        last_name="LastName",
        email="e@mail.ru",
    )


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def another_user(mixer):
    from django.contrib.auth.models import User

    return mixer.blend(User, username="AnotherUser")
