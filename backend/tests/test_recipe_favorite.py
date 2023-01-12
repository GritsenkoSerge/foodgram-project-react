import pytest
from rest_framework import status

from recipes.models import FavoriteRecipe


class TestRecipe:
    URL_RECIPES_ID_FAVORITE = "/api/recipes/{}/favorite/"

    # post /api/recipes/{id}/favorite/ 201
    @pytest.mark.django_db(transaction=True)
    def test_recipes_favorite__create_valid(self, api_client, recipe, user):
        url = self.URL_RECIPES_ID_FAVORITE.format(recipe.id)
        assert not FavoriteRecipe.objects.filter(
            recipe=recipe, user=user
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
        assert FavoriteRecipe.objects.filter(
            recipe=recipe, user=user
        ).exists(), (
            f"Убедитесь, что после запроса `{url}`, рецепт находится в избранном."
        )

    # post /api/recipes/{id}/favorite/ 400
    @pytest.mark.django_db(transaction=True)
    def test_recipes_favorite__create_invalid(self, api_client, favorite_recipe, user):
        url = self.URL_RECIPES_ID_FAVORITE.format(favorite_recipe.id)
        assert FavoriteRecipe.objects.filter(
            recipe=favorite_recipe, user=user
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

    # post /api/recipes/{id}/favorite/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipes_favorite__create_unauthorized(self, client, recipe):
        url = self.URL_RECIPES_ID_FAVORITE.format(recipe.id)
        response = client.post(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."

    # delete /api/recipes/{id}/favorite/ 204
    @pytest.mark.django_db(transaction=True)
    def test_recipes_favorite__delete_valid(self, api_client, favorite_recipe, user):
        url = self.URL_RECIPES_ID_FAVORITE.format(favorite_recipe.id)
        assert FavoriteRecipe.objects.filter(
            recipe=favorite_recipe, user=user
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
        assert not FavoriteRecipe.objects.filter(
            recipe=favorite_recipe, user=user
        ).exists(), (
            f"Убедитесь, что при запросе `{url}`, рецепт удаляется из избранного."
        )

    # delete /api/recipes/{id}/favorite/ 400
    @pytest.mark.django_db(transaction=True)
    def test_recipes_favorite__delete_invalide(self, api_client, recipe, user):
        url = self.URL_RECIPES_ID_FAVORITE.format(recipe.id)
        assert not FavoriteRecipe.objects.filter(
            recipe=recipe, user=user
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

    # delete /api/recipes/{id}/favorite/ 401
    @pytest.mark.django_db(transaction=True)
    def test_recipes_favorite__delete_unauthorized(self, client, favorite_recipe):
        url = self.URL_RECIPES_ID_FAVORITE.format(favorite_recipe.id)
        response = client.delete(url)
        code_expected = status.HTTP_401_UNAUTHORIZED
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get(
            "detail"
        ), f"Убедитесь, что при запросе `{url}`, возвращается текст ошибки."
