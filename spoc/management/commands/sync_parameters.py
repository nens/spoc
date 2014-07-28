import os
import csv
import glob

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from spoc.models import Parameter

class Command(BaseCommand):
    help = '''Import or update parameters from csv-file where row
    <parameterid>,<parametername>'''
    
    option_list = BaseCommand.option_list + (
        make_option('--f',
                    default=None,
                    help='csv-filepath with parameters.'),
    )                
        
    def handle(self, *args, **options):
        filepath = options.get('f', None)
        if filepath is None:
            self.stdout.write('Tell me where is the csv-file with parameters.')
            return
        updated = 0
        created = 0
        self.stdout.write('Start synchronization.')
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                try:
                    parameter = Parameter.objects.get(id=row[0])
                    parameter.name = row[1]
                    parameter.save()
                    updated = updated + 1
                except Parameter.DoesNotExist:
                    Parameter(id=row[0], name=row[1]).save()
                    created = created + 1

        self.stdout.write(
            'Successfully passed: updated={0}, created={1}.'.format(updated, created))
