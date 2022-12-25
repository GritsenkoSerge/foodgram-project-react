from django.db.models import fields

from tests.utils import check_model_field_names

try:
    from recipes.models import Recipe
except ImportError:
    assert False, 'Не найдена модель `Recipe` в приложении `recipes`'
try:
    from tags.models import Tag
except ImportError:
    assert False, 'Не найдена модель `Tag` в приложении `tags`'
try:
    from recipes.models import Favorite
except ImportError:
    assert False, 'Не найдена модель `Favorite` в приложении `recipes`'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestFavorite:
    MODEL = Favorite
    FIELDS = {
        'recipe': (fields.ForeignKey, Recipe),
        'tag': (fields.ForeignKey, Tag),
    }

    def test_recipe_tag_model(self):
        check_model_field_names(self.MODEL, self.FIELDS)
