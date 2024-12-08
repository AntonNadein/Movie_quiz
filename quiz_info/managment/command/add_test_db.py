from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):

        call_command("loaddata", "films_fixture.json")
        self.stdout.write(self.style.SUCCESS("Фикстуры успешно загружены"))