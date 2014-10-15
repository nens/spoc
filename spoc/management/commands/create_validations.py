
from django.core.management.base import BaseCommand, CommandError
from spoc import models

class Command(BaseCommand):
    help = "Create data if it doesn't exist."
  
    def handle(self, *args, **options):
        self.stdout.write('Start creating validations.')
        count = 0
        for header in models.Header.objects.all():
            count_before = header.validation_set.count()
            header.add_validations()
            count_after = header.validation_set.count()
            count = count + (count_after - count_before)
        self.stdout.write('Added validations {}'.format(count))