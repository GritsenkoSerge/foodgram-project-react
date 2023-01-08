import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from ...models import Ingredient

TABLES = ((Ingredient, "ingredients.json"),)


class Command(BaseCommand):
    help = "Загружает данные из файлов (../data/*.json) в базу данных"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-b",
            "--batch_size",
            type=int,
            help="Set batch_size for bulk_create. Default 500.",
            default=500,
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        verbosity = options["verbosity"]
        batch_size = options.get("batch_size", "500")
        if verbosity > 0:
            self.stdout.write("Загрузка тестовых данных...")
        for model, file_name in TABLES:
            file_path = settings.BASE_DIR.parent / "data" / file_name
            try:
                with open(file_path, "rt", encoding="utf-8") as json_file:
                    json_data = json.load(json_file)
                    model.objects.all().delete()
                    bulk_objs = []
                    for data in json_data:
                        if verbosity > 1:
                            self.stdout.write(self.style.NOTICE(f"  {data}"))
                        bulk_objs.append(model(**data))
                    model.objects.bulk_create(
                        bulk_objs, batch_size, ignore_conflicts=True
                    )
                    if verbosity > 0:
                        self.stdout.write(self.style.SUCCESS(f"  {file_name} - готово"))
            except Exception as error:
                raise CommandError(
                    f"При загрузке файла {file_name} произошла ошибка." f"\r\n{error}"
                )
