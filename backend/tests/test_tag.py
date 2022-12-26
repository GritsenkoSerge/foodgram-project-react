from django.db import models

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

    def test_tag_model(self):
        check_model_field_names(self.MODEL, self.MODEL_FIELDS)
