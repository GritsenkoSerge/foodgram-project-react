# Generated by Django 3.2 on 2023-01-12 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tags", "0005_auto_20230111_0006"),
        ("ingredients", "0003_alter_ingredient_options"),
        ("recipes", "0003_auto_20230111_1837"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-created",),
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
        migrations.AlterField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                help_text="Выберите из списка автора",
                on_delete=django.db.models.deletion.RESTRICT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                help_text="Выберите ингредиенты",
                through="recipes.IngredientInRecipe",
                to="ingredients.Ingredient",
                verbose_name="Ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                help_text="Выберите теги",
                through="recipes.TagRecipe",
                to="tags.Tag",
                verbose_name="Теги",
            ),
        ),
    ]
