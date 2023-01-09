import pytest
from django.db import models
from rest_framework import status

from tests.utils import check_model_field_names

try:
    from users.models import User
except ImportError:
    assert False, "Не найдена модель `User` в приложении `users`"
try:
    from tags.models import Tag
except ImportError:
    assert False, "Не найдена модель `Tag` в приложении `tags`"
try:
    from ingredients.models import Ingredient
except ImportError:
    assert False, "Не найдена модель `Ingredient` в приложении `ingredients`"
try:
    from recipes.models import Recipe
except ImportError:
    assert False, "Не найдена модель `Recipe` в приложении `recipes`"


class TestRecipe:
    MODEL = Recipe
    MODEL_FIELDS = {
        "created": (models.DateTimeField, None),
        "author": (models.ForeignKey, User),
        "name": (models.CharField, None),
        "image": (models.ImageField, None),
        "text": (models.TextField, None),
        "cooking_time": (models.PositiveIntegerField, None),
        "ingredients": (models.ManyToManyField, Ingredient),
        "tags": (models.ManyToManyField, Tag),
        "favorites": (models.ManyToManyField, User),
        "shopping_carts": (models.ManyToManyField, User),
    }
    URL_RECIPES = "/api/recipes/"
    URL_RECIPES_ID = "/api/recipes/{}/"

    def test_recipe_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)

    @pytest.mark.django_db(transaction=True)
    def test_recipe__get_valid(self, client, recipe, recipe_ingredient):
        url = self.URL_RECIPES
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        amount = Recipe.objects.count()
        json = response.json()
        assert (
            json.get("count") == amount
        ), f"Убедитесь, что при запросе `{url}`, возвращается список рецептов."
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        recipes = json.get("results")
        assert isinstance(recipes, list) and isinstance(recipes[0], dict), (
            f"Убедитесь, что при запросе `{url}`, " f"возвращается список рецептов."
        )
        assert all(map(lambda x: x in recipes[0], fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращаются рецепты с полями {fields}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe__get_by_filter(
        self, client, user, recipe, recipe_ingredient, denied_recipe, tag, lunch_tag
    ):
        url = self.URL_RECIPES + "?is_favorited=1"
        response = client.get(url, format="json")
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        amount = 0
        json = response.json()
        assert (
            json.get("count") == amount
        ), f"Убедитесь, что при запросе `{url}`, рецепты фильтруются по избранным."
        url = self.URL_RECIPES + "?is_in_shopping_cart=1"
        response = client.get(url, format="json")
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        amount = 0
        json = response.json()
        assert json.get("count") == amount, (
            f"Убедитесь, что при запросе `{url}`, "
            "рецепты фильтруются по наличию в корзине."
        )
        url = self.URL_RECIPES + f"?author={user.id}"
        response = client.get(url, format="json")
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        amount = Recipe.objects.filter(author=user).count()
        json = response.json()
        assert json.get("count") == amount, (
            f"Убедитесь, что при запросе `{url}`, "
            f"рецепты фильтруются по автору `{user.get_name()}`."
        )
        url = self.URL_RECIPES + f"?tags={tag.slug}&tags={lunch_tag.slug}"
        response = client.get(url, format="json")
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        amount = 1
        json = response.json()
        assert (
            json.get("count") == amount
        ), f"Убедитесь, что при запросе `{url}`, рецепты фильтруются по тегам."

    # post /api/recipes/ 201
    @pytest.mark.django_db(transaction=True)
    def test_recipe__create_valid(self, api_client, tag, lunch_tag, ingredient):
        url = self.URL_RECIPES
        recipe_name = "Recipe name"
        data = {
            "ingredients": list([{"id": ingredient.id, "amount": 10}]),
            "tags": list([tag.id, lunch_tag.id]),
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": recipe_name,
            "text": "string",
            "cooking_time": 1,
        }
        response = api_client.post(url, data=data, format="json")
        code_expected = status.HTTP_201_CREATED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        assert all(map(lambda x: x in json, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с полями {fields}"
        )
        assert json.get("name") == recipe_name, (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с названием `{fields}`"
        )

    # post /api/recipes/ 400
    @pytest.mark.django_db(transaction=True)
    def test_recipe__create_invalid(self, api_client):
        url = self.URL_RECIPES
        data = {
            "image": "",
            "name": "",
            "text": "",
            "cooking_time": 0,
        }
        response = api_client.post(url, data=data, format="json")
        code_expected = status.HTTP_400_BAD_REQUEST
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "image",
            "name",
            "text",
            "cooking_time",
        )
        assert all(map(lambda x: x in json, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается ошибки с полями {fields}"
        )

    # post /api/recipes/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipe__create_unauthorized(self, client, tag, ingredient):
        url = self.URL_RECIPES
        recipe_name = "Recipe name"
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 10}],
            "tags": [tag.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": recipe_name,
            "text": "string",
            "cooking_time": 1,
        }
        response = client.post(url, data=data, format="json")
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        # assert (
        #     not response.content
        # ), f"Убедитесь, что при запросе `{url}`, возвращается пустой content."

    # post /api/recipes/ 404
    @pytest.mark.django_db(transaction=True)
    def test_recipe__create_not_found(self, api_client):
        not_found_id = 404
        url = self.URL_RECIPES
        data = {
            "ingredients": [{"id": not_found_id, "amount": 10}],
            "tags": [not_found_id],
            "image": (
                "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA"
                "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
                "9TXL0Y4OHwAAAABJRU5ErkJggg=="
            ),
            "name": "recipe_name",
            "text": "string",
            "cooking_time": 1,
        }
        response = api_client.post(url, data=data, format="json")
        code_expected = status.HTTP_404_NOT_FOUND
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # get /api/recipes/{id}/ 200
    @pytest.mark.django_db(transaction=True)
    def test_recipe__get_detail_valid(self, client, recipe, recipe_ingredient):
        url = self.URL_RECIPES_ID.format(recipe.id)
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        assert all(map(lambda x: x in json, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с полями {fields}"
        )

    # patch /api/recipes/{id}/ 200
    @pytest.mark.django_db(transaction=True)
    def test_recipe__update_valid(self, api_client, recipe, ingredient, tag):
        url = self.URL_RECIPES_ID.format(recipe.id)
        recipe_name = "Recipe name"
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 10}],
            "tags": [tag.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": recipe_name,
            "text": "string",
            "cooking_time": 1,
        }
        response = api_client.patch(url, data=data, format="json")
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        assert all(map(lambda x: x in json, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с полями {fields}"
        )
        assert json.get("name") == recipe_name, (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с названием `{fields}`"
        )

    # patch /api/recipes/{id}/ 400
    @pytest.mark.django_db(transaction=True)
    def test_recipe__update_invalid(
        self, api_client, recipe, ingredient, tag, few_ingredients
    ):
        url = self.URL_RECIPES_ID.format(recipe.id)
        data = {
            "image": "",
            "name": "",
            "text": "",
            "cooking_time": 0,
        }
        response = api_client.patch(url, data=data, format="json")
        code_expected = status.HTTP_400_BAD_REQUEST
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "name",
            "image",
            "text",
            "cooking_time",
        )
        assert all(map(lambda x: x in json, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с полями {fields}"
        )
        data = {
            "ingredients": [
                {"id": ingredient.id, "amount": 10},
                {"id": few_ingredients.id, "amount": 0},
            ],
        }
        response = api_client.patch(url, data=data, format="json")
        code_expected = status.HTTP_400_BAD_REQUEST
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        ingredients = json.get("ingredients")
        assert isinstance(ingredients, list) and len(ingredients), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается список ingredients с двумя записями."
        )
        assert ingredients[0] == {} and ingredients[1].get("amount"), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается список ingredients с указанием ошибочной записи."
        )

    # patch /api/recipes/{id}/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipe__update_unauthorized(self, client, recipe, ingredient, tag):
        url = self.URL_RECIPES_ID.format(recipe.id)
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 10}],
            "tags": [tag.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "recipe_name",
            "text": "string",
            "cooking_time": 1,
        }
        response = client.patch(url, data=data, format="json")
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # patch /api/recipes/{id}/ 403
    @pytest.mark.django_db(transaction=True)
    def test_recipe__update_denied(self, api_client, denied_recipe, ingredient, tag):
        url = self.URL_RECIPES_ID.format(denied_recipe.id)
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 10}],
            "tags": [tag.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "recipe_name",
            "text": "string",
            "cooking_time": 1,
        }
        response = api_client.patch(url, data=data, format="json")
        code_expected = status.HTTP_403_FORBIDDEN
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # patch /api/recipes/{id}/ 404
    @pytest.mark.django_db(transaction=True)
    def test_recipe__update_not_found(self, client, recipe, ingredient, tag):
        not_found_id = 404
        url = self.URL_RECIPES_ID.format(recipe.id)
        data = {
            "ingredients": [{"id": not_found_id, "amount": 10}],
            "tags": [not_found_id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "recipe_name",
            "text": "string",
            "cooking_time": 1,
        }
        response = client.patch(url, data=data, format="json")
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."
        url = self.URL_RECIPES_ID.format(not_found_id)
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 10}],
            "tags": [tag.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAA"
                "CVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
                "AAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "recipe_name",
            "text": "string",
            "cooking_time": 1,
        }
        response = client.patch(url, data=data, format="json")
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/recipes/{id}/ 204
    @pytest.mark.django_db(transaction=True)
    def test_recipe__delete_valid(self, api_client, recipe):
        url = self.URL_RECIPES_ID.format(recipe.id)
        response = api_client.delete(url)
        code_expected = status.HTTP_204_NO_CONTENT
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        assert (
            not response.content
        ), f"Убедитесь, что при запросе `{url}`, возвращается пустой content."

    # delete /api/recipes/{id}/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipe__delete_unauthorized(self, client, recipe):
        url = self.URL_RECIPES_ID.format(recipe.id)
        response = client.delete(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/recipes/{id}/ 403
    @pytest.mark.django_db(transaction=True)
    def test_recipe__delete_denied(self, api_client, denied_recipe):
        url = self.URL_RECIPES_ID.format(denied_recipe.id)
        response = api_client.delete(url)
        code_expected = status.HTTP_403_FORBIDDEN
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/recipes/{id}/ 404
    @pytest.mark.django_db(transaction=True)
    def test_recipe__delete_not_found(self, api_client):
        not_found_id = 404
        url = self.URL_RECIPES_ID.format(not_found_id)
        response = api_client.delete(url)
        code_expected = status.HTTP_404_NOT_FOUND
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."
