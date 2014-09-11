
from django.core.management.base import BaseCommand, CommandError
from spoc import config_to_dbf, debiet_to_dbf

class Command(BaseCommand):
    help = 'Create fews configuration dbf-file'
  
    def handle(self, *args, **options):
        self.stdout.write('Start creating configuration.dbf.')
        #config_to_dbf.create_dbf()
        self.stdout.write('Start creating debietberekening.dbf.')
        debiet_to_dbf.create_dbf()
