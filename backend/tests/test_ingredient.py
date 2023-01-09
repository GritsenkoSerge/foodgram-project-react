import pytest
from django.db import models
from rest_framework import status


from tests.utils import check_model_field_names

try:
    from ingredients.models import Ingredient
except ImportError:
    assert False, "Не найдена модель `Ingredient` в приложении `ingredients`"


class TestIngredient:
    MODEL = Ingredient
    MODEL_FIELDS = {
        "name": (models.CharField, None),
        "measurement_unit": (models.CharField, None),
    }
    URL_INGREDIENTS = "/api/ingredients/"
    URL_INGREDIENTS_ID = "/api/ingredients/{}/"

    def test_ingredient_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)

    # get /api/ingredients/ 200
    @pytest.mark.django_db(transaction=True)
    def test_ingredient__get(self, client, few_ingredients):
        url = self.URL_INGREDIENTS
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        amount = Ingredient.objects.count()
        json = response.json()
        assert (
            isinstance(json, list) and len(json) == amount
        ), f"Убедитесь, что при запросе `{url}`, возвращается список ингредиентов."
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
        assert all(map(json[0].get, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается ингредиент с полями {fields}"
        )
        contains = few_ingredients.name[:2]
        url = self.URL_INGREDIENTS + f"?name={contains}"
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        amount = Ingredient.objects.filter(name__icontains=contains).count()
        json = response.json()
        assert (
            len(json) == amount
        ), f"Убедитесь, что при запросе `{url}`, корректно фильтруются ингредиенты."

    # get /api/ingredients/{id}/ 200
    @pytest.mark.django_db(transaction=True)
    def test_ingredient__id_get(self, client, ingredient):
        url = self.URL_INGREDIENTS_ID.format(ingredient.id)
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
        assert all(map(json.get, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается ингредиент с полями {fields}"
        )
