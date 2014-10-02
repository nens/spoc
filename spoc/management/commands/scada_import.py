import os
import csv
import glob

from lxml import objectify
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from spoc.models import ScadaLocation, Header, Source, Parameter
from spoc.import_mon import ExtractLocationParameterFromMonDir


class Command(BaseCommand):
    help = '''Import location, headers from scada. Actions on import: update, create.'''
    
    option_list = BaseCommand.option_list + (
        make_option('--scada',
                    default=None,
                    help='''Pass scadas separated with ",". Do not use spaces in the name of scada. Case sensitive.'''),
    )

    def get_parameter(self, parameterid):
        parameter = None
        try:
            parameter = Parameter.objects.get(id__iexact=parameterid)
        except Parameter.DoesNotExist:
            self.stdout.write("Parameter {} does not exist.".format(parameterid))
        return parameter

    def get_or_create_scadalocation(self, id, name, source):
        try:
            location = ScadaLocation.objects.get(locationid__iexact=id)
        except ScadaLocation.DoesNotExist:
            location = ScadaLocation(
                locationid=id, locationname=name, source=source)
            location.save()
        return location
            
    def get_or_create_header(self, location, parameterid):
        header = None
        try:
            header = Header.objects.get(
                location=location, parameter__id__iexact=parameterid)
        except Header.DoesNotExist:
            parameter = self.get_parameter(parameterid)
            if parameter is not None:
                header = Header(location=location,
                                parameter=self.get_parameter(parameterid))
        return header

    def import_pixml_source(self, source):
        filenames = glob.glob1(source.directory, '*.xml')
        for filename in filenames:
            filepath = os.path.join(source.directory, filename)
            with open(filepath, 'rb') as f:
                root = objectify.fromstring(f.read())
                series = root.getchildren()
                for s in series:
                    locationid = s.header.locationId
                    locationname = s.header.stationName
                    parameterid = s.header.parameterId
                    location = self.get_or_create_scadalocation(
                        locationid, locationname, source)
                    header = self.get_or_create_header(location, parameterid)
                    if header is None:
                        continue
                    header.locationname = locationname
                    header.save()

    def import_scv_source(self, source):
        filenames = glob.glob1(source.directory, '*.csv')
        for filename in filenames:
            filepath = os.path.join(source.directory, filename)
            with open(filepath, 'rb') as f:
                reader = csv.reader(f, delimiter=';')
                locationname = reader.next()[1]
                locationid = reader.next()[1]
                parameterid = reader.next()[1]
                location = self.get_or_create_scadalocation(locationid, locationname, source)
                header = self.get_or_create_header(location, parameterid)
                if header is None:
                    continue
                header.locationname = locationname
                header.save()

    
    def import_mon_source(self, source):
        extractor = ExtractLocationParameterFromMonDir()
        result_dir = extractor.__call__(source.directory)
        for k, v in result_dir.iteritems():
            locationname = ''
            locationid = k[0]
            parameterid = k[1]
            location = self.get_or_create_scadalocation(locationid, locationname, source)
            header = self.get_or_create_header(location, parameterid)
            if header is None:
                continue
            header.locationname = locationname
            header.save()

                
    def handle(self, *args, **options):
        scadas = options.get('scada', None)
        if scadas is None:
            self.stdout.write('Import all scadas.')
            sources = Source.objects.all()
        else:
            scadas = scadas.replace(' ', '')
            scadas_list = scadas.split(',')
            sources = Source.objects.filter(name__in=scadas_list)
        
        if not sources.exists():
            self.stdout.write(
                "No scada configured. Add scadas to Sources table using admin interface.")

        for source in sources:
            if not os.path.isdir(source.directory):
                self.stdout.write(
                    "Source directory {} does not exist.".format(source.directory))
                continue

            if source.source_type == Source.SCADA_CSV:
                self.import_scv_source(source)
            elif source.source_type == Source.SCADA_PIXML:
                self.import_pixml_source(source)
            elif source.source_type == Source.SCADA_MON:
                self.import_mon_source(source)

            self.stdout.write('Successfully passed scade "%s"' % source.name)
