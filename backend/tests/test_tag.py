import pytest
from django.db import models
from rest_framework import status

from tests.utils import check_model_field_names

try:
    from tags.models import Tag
except ImportError:
    assert False, "Не найдена модель `Tag` в приложении `tags`"


class TestTag:
    MODEL = Tag
    MODEL_FIELDS = {
        "name": (models.CharField, None),
        "color": (models.CharField, None),
        "slug": (models.SlugField, None),
    }
    URL_TAGS = "/api/tags/"
    URL_TAGS_ID = "/api/tags/{}/"

    def test_tag_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)

    # get /api/tags/ 200
    @pytest.mark.django_db(transaction=True)
    def test_tag__get(self, client, tag):
        url = self.URL_TAGS
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert (
            isinstance(json, list) and len(json) == 1
        ), f"Убедитесь, что при запросе `{url}`, возвращается список с одним тегом."
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )
        assert all(map(json[0].get, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается тег с полями {fields}"
        )

    # get /api/tags/{id}/ 200
    @pytest.mark.django_db(transaction=True)
    def test_tag__valid_id_get(self, client, tag):
        url = self.URL_TAGS_ID.format(tag.id)
        response = client.get(url)
        code_expected = status.HTTP_200_OK
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )
        assert all(map(json.get, fields)), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается тег с полями {fields}"
        )

    # get /api/tags/{id}/ 404
    @pytest.mark.django_db(transaction=True)
    def test_tag__not_found_id_get(self, client):
        not_found_id = "404"
        url = self.URL_TAGS_ID.format(not_found_id)
        response = client.get(url)
        code_expected = status.HTTP_404_NOT_FOUND
        assert (
            response.status_code == code_expected
        ), f"Убедитесь, что при запросе `{url}`, возвращается код {code_expected}."
        json = response.json()
        assert json.get("detail"), (
            f"Убедитесь, что при запросе `{url}`, "
            f"возвращается сообщение с деталями ошибки."
        )
