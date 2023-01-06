import pytest
from rest_framework import status


class TestRecipe:
    URL_RECIPES_ID_SHOPPING_CART = "/api/recipes/{}/shopping_cart/"
    URL_RECIPES_DOWNLOAD_SHOPPING_CART = "/api/recipes/download_shopping_cart/"

    # post /api/recipes/{id}/shopping_cart/ 201
    @pytest.mark.django_db(transaction=True)
    def test_recipes_shopping_cart__create_valid(self, api_client, recipe, user):
        url = self.URL_RECIPES_ID_SHOPPING_CART.format(recipe.id)
        assert not user.cart_recipes.filter(
            id=recipe.id
        ).exists(), (
            "Убедитесь, что перед запросом `{url}`, рецепт не находится в избранном."
        )
        response = api_client.post(url)
        code_expected = status.HTTP_201_CREATED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
        assert all(map(lambda x: x in json, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с полями {fields}"
        )
        assert json.get("id") == recipe.id, (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается рецепт с названием `{fields}`"
        )
        assert user.shopping_cart_recipes.filter(
            id=recipe.id
        ).exists(), (
            f"Убедитесь, что после запроса `{url}`, рецепт находится в избранном."
        )

    # post /api/recipes/{id}/shopping_cart/ 400
    @pytest.mark.django_db(transaction=True)
    def test_recipes_shopping_cart__create_invalid(
        self, api_client, shopping_cart_recipe, user
    ):
        url = self.URL_RECIPES_ID_SHOPPING_CART.format(shopping_cart_recipe.id)
        assert user.shopping_cart_recipes.filter(
            id=shopping_cart_recipe.id
        ).exists(), (
            f"Убедитесь, что перед запросом `{url}`, рецепт находится в избранном."
        )
        response = api_client.post(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "errors"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # post /api/recipes/{id}/shopping_cart/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipes_shopping_cart__create_unauthorized(self, client, recipe):
        url = self.URL_RECIPES_ID_SHOPPING_CART.format(recipe.id)
        response = client.post(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/recipes/{id}/shopping_cart/ 204
    @pytest.mark.django_db(transaction=True)
    def test_recipes_shopping_cart__delete_valid(
        self, api_client, shopping_cart_recipe, user
    ):
        url = self.URL_RECIPES_ID_SHOPPING_CART.format(shopping_cart_recipe.id)
        assert user.shopping_cart_recipes.filter(
            id=shopping_cart_recipe.id
        ).exists(), (
            f"Убедитесь, что перед запросом `{url}`, рецепт находится в избранном."
        )
        response = api_client.delete(url)
        code_expected = status.HTTP_204_NO_CONTENT
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        assert (
            not response.content
        ), f"Убедитесь, что при запросе `{url}`, возвращается пустой content."
        assert not user.shopping_cart_recipes.filter(
            id=shopping_cart_recipe.id
        ).exists(), (
            f"Убедитесь, что при запросе `{url}`, рецепт удаляется из избранного."
        )

    # delete /api/recipes/{id}/shopping_cart/ 400
    @pytest.mark.django_db(transaction=True)
    def test_recipes_shopping_cart__delete_invalide(self, api_client, recipe, user):
        url = self.URL_RECIPES_ID_SHOPPING_CART.format(recipe.id)
        assert not user.shopping_cart_recipes.filter(
            id=recipe.id
        ).exists(), (
            "Убедитесь, что перед запросом `{url}`, рецепт не находится в избранном."
        )
        response = api_client.delete(url)
        code_expected = status.HTTP_400_BAD_REQUEST
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "errors"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/recipes/{id}/shopping_cart/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipes_shopping_cart__delete_unauthorized(
        self, client, shopping_cart_recipe
    ):
        url = self.URL_RECIPES_ID_SHOPPING_CART.format(shopping_cart_recipe.id)
        response = client.delete(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."
