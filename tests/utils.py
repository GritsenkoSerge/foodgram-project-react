def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def check_model_field_names(model, fields):
    model_fields = model._meta.fields

    for field_name, (field_type, related_model) in fields.items():
        field = search_field(model_fields, field_name)
        assert field is not None, (
            f'Добавьте поле `{field_name}` '
            f'модели `{model.__name__}`'
        )
        assert type(field) == field_type, (
            f'Свойство `{field_name}` модели `{model.__name__}` '
            f'должно быть типа `{field_type.__name__}`'
        )
        if related_model:
            assert field.related_model == related_model, (
                f'Свойство `{field_name}` '
                f'модели `{model.__name__}` '
                f'должно быть ссылкой на модель `{related_model.__name__}`'
            )
