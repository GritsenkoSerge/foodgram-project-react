# Generated by Django 3.2 on 2023-01-08 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                help_text="Выберите картинку",
                upload_to="recipes/",
                verbose_name="Картинка",
            ),
        ),
    ]