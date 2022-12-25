from django.db.models import fields

from tests.utils import check_model_field_names

try:
    from tags.models import Tag
except ImportError:
    assert False, 'Не найдена модель `Tag` в приложении `tags`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestTag:
    MODEL = Tag
    FIELDS = {
        'name': (fields.CharField, None),
        'color': (fields.CharField, None),
        'slug': (fields.CharField, None),
    }

    def test_tag_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
