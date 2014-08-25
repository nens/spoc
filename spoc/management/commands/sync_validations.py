import os
import csv
import glob

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from spoc import models

class Command(BaseCommand):
    help = '''Import or update parameters from csv-file where row
    <parameterid>,<parametername>'''
    
    option_list = BaseCommand.option_list + (
        make_option('--f',
                    default=None,
                    help='csv-filepath with validations.'),
    )                
        
    def handle(self, *args, **options):
        filepath = options.get('f', None)
        if filepath is None:
            self.stdout.write('Tell me where is the csv-file with validations.')
            return
        self.stdout.write('Start synchronization.')
        with open(filepath, 'rb') as f:
            reader = csv.DictReader(f,skipinitialspace=True, delimiter=';')
            count = 0
            for row in reader:
                if count == 0:
                    self.insert_fields(row)
                    count= count + 1
                self.insert_validation_field(row)
        self.stdout.write('Successfully passed.')

    def insert_validation_field(self, row):
        parameter = self.get_or_create_parameter(row['WNS-code'], row['WNS-naam'])
        fields = models.Field.objects.filter(field_type=models.Field.VALIDATION)
        for field in fields:
            if row[field.name] == '':
                continue
            filter = {'field': field, 'parameter': parameter}
            if models.ValidationField.objects.filter(**filter).exists():
                continue
            models.ValidationField(**filter).save()
                
    def insert_fields(self, row):
        headers = row.keys()
        for header in headers:
            if header in ['WNS-code', 'WNS-naam', 'Formule']:
                continue
            try:
                models.Field.objects.get(name=header, field_type=models.Field.VALIDATION)
            except models.Field.DoesNotExist:
                models.Field(
                    name=header, field_type=models.Field.VALIDATION).save()
                self.stdout.write('Field created')
                
    def get_or_create_parameter(self, code, name):
        try:
            parameter = models.Parameter.objects.get(id=code)
            parameter.name = name
            parameter.save()
        except models.Parameter.DoesNotExist:
            parameter = models.Parameter(id=code, name=name)
            parameter.save()
            self.stdout.write("Parameter created")
        return parameter
