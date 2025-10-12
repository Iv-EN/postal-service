from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from mailing.models import ManagerGroup


class Command(BaseCommand):
    help = "Создание группы менеджеров и добавление к ней прав."

    def handle(self, *args, **kwargs):
        group, created = ManagerGroup.create_group()
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Группа '{group.name}' успешно создана.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Группа '{group.name}' уже существует.")
            )
