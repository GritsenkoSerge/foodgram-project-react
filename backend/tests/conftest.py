import tempfile
from pathlib import Path

import pytest
from django.utils.version import get_version
from mixer.backend.django import mixer as _mixer
from rest_framework.test import APIClient

from foodgram.settings import INSTALLED_APPS
from ingredients.models import Ingredient
from recipes.models import (
    Recipe,
    IngredientInRecipe,
    TagRecipe,
    FavoriteRecipe,
    ShoppingCartRecipe,
)
from tags.models import Tag
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


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


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
def another_user(django_user_model, user_password):
    return django_user_model.objects.create_user(
        username="TestUser2",
        password=user_password,
        first_name="FirstName",
        last_name="LastName",
        email="e2@mail.ru",
    )


@pytest.fixture
def one_more_user(django_user_model, user_password):
    return django_user_model.objects.create_user(
        username="TestUser3",
        password=user_password,
        first_name="FirstName",
        last_name="LastName",
        email="e3@mail.ru",
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
def subscription(mixer, user, another_user):
    return mixer.blend(Subscription, user=user, author=another_user)


@pytest.fixture
def tag():
    return Tag.objects.create(name="Завтрак", color="#E26C2D", slug="breakfast")


@pytest.fixture
def lunch_tag():
    return Tag.objects.create(name="Обед", color="#E26CFF", slug="lunch")


@pytest.fixture
def dinner_tag():
    return Tag.objects.create(name="Ужин", color="#FF6CFF", slug="dinner")


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(name="Капуста", measurement_unit="кг")


@pytest.fixture
def few_ingredients(mixer):
    ingredients = mixer.cycle(10).blend(Ingredient)
    return ingredients[-1]


@pytest.fixture
def recipe(mixer, user, tag, lunch_tag):
    instance = mixer.blend(Recipe, author=user)
    mixer.blend(TagRecipe, recipe=instance, tag=tag)
    mixer.blend(TagRecipe, recipe=instance, tag=lunch_tag)
    return instance


@pytest.fixture
def recipe_ingredient(mixer, recipe, few_ingredients):
    return mixer.blend(
        IngredientInRecipe, recipe=recipe, ingredient=few_ingredients, amount=2
    )


@pytest.fixture
def denied_recipe(
    mixer, another_user, ingredient, few_ingredients, dinner_tag, lunch_tag
):
    instance = mixer.blend(Recipe, author=another_user)
    mixer.blend(IngredientInRecipe, recipe=instance, ingredient=ingredient, amount=1)
    mixer.blend(
        IngredientInRecipe, recipe=instance, ingredient=few_ingredients, amount=3
    )
    mixer.blend(TagRecipe, recipe=instance, tag=dinner_tag)
    mixer.blend(TagRecipe, recipe=instance, tag=lunch_tag)
    return instance


@pytest.fixture
def one_more_denied_recipe(mixer, another_user, ingredient, few_ingredients):
    instance = mixer.blend(Recipe, author=another_user)
    mixer.blend(IngredientInRecipe, recipe=instance, ingredient=ingredient, amount=3)
    mixer.blend(
        IngredientInRecipe, recipe=instance, ingredient=few_ingredients, amount=4
    )
    return instance


@pytest.fixture
def favorite_recipe(denied_recipe, user):
    instance = FavoriteRecipe(recipe=denied_recipe, user=user)
    instance.save()
    return denied_recipe


@pytest.fixture
def shopping_cart_recipe(denied_recipe, user):
    instance = ShoppingCartRecipe(recipe=denied_recipe, user=user)
    instance.save()
    return denied_recipe


@pytest.fixture
def one_more_shopping_cart_recipe(recipe, user, recipe_ingredient):
    instance = ShoppingCartRecipe(recipe=recipe, user=user)
    instance.save()
    return recipe


@pytest.fixture
def jpg_image():
    return tempfile.NamedTemporaryFile(suffix=".jpg").name
