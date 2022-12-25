from django.core.exceptions import FieldDoesNotExist


def check_model_field_names(model, fields):
    for field_name, (field_type, related_model) in fields.items():
        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            assert False, f"Добавьте поле `{field_name}` " f"модели `{model.__name__}`"
        assert type(field) == field_type, (
            f"Поле `{field_name}` "
            f"модели `{model.__name__}` "
            f"должно быть типа `{field_type.__name__}`"
        )
        if related_model:
            assert field.related_model == related_model, (
                f"Поле `{field_name}` "
                f"модели `{model.__name__}` "
                f"должно быть ссылкой на модель `{related_model.__name__}`"
            )
        assert field.verbose_name, (
            f"Для поля `{field_name}` "
            f"модели `{model.__name__}` "
            f"должно должно быть заполнено свойство `verbose_name`"
        )
        assert field.help_text, (
            f"Для поля `{field_name}` "
            f"модели `{model.__name__}` "
            f"должно должно быть заполнено свойство `help_text`"
        )
