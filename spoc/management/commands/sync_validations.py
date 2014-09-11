import os
import csv
import glob

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from spoc import models

class Command(BaseCommand):
    help = '''Insert or update parameters, fields, validationfields, formulas
    from csv-file.'''
    
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
                if row['WNS-code'] in [None, '']:
                    continue
                if count == 0:
                    self.insert_fields(row)
                    count= count + 1
                self.insert_validation_field(row)
                self.insert_formula(row)
        self.stdout.write('Successfully passed.')

    def insert_formula(self, row):
        """Add a formula if it not exists."""
        if row['Formule'] == '':
            return
        headers = models.Header.objects.filter(parameter__id=row['WNS-code'])
        count = 0
        print row['WNS-code'], row['Formule'], headers.count()
        for header in headers:
            if not header.headerformula_set.exists():
                formula = models.HeaderFormula(header=header)
                formula.save()
                header.headerformula_set.add(formula)
                count = count + 1
        self.stdout.write("{} Formulas created.".format(count))

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
                prefix = self.get_unused_prefix()
                if prefix is None:
                    raise Exception("Error on insert a field: No field prefix available.")
                models.Field(
                    name=header, field_type=models.Field.VALIDATION, prefix=prefix).save()
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

    def get_unused_prefix(self):
        validation_fields = models.Field.objects.filter(
            field_type=models.Field.VALIDATION)
        used_prefixes = validation_fields.values_list('prefix', flat=True)
        unused_prefixes = [i for i in models.Field.PREFIXES if i not in used_prefixes]
        
        if len(unused_prefixes) > 0:
            return unused_prefixes[0]
        else:
            return None
               
