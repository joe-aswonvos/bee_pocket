from django.core.management.base import BaseCommand
from pocket_app.models import Weekday

class Command(BaseCommand):
    help = 'Check and add days of the week to the database if they are not present'

    def handle(self, *args, **kwargs):
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in weekdays:
            if not Weekday.objects.filter(name=day).exists():
                Weekday.objects.create(name=day)
                self.stdout.write(self.style.SUCCESS(f'Added {day} to Weekday model'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{day} already exists in Weekday model'))