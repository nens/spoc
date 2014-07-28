
from django.core.management.base import BaseCommand, CommandError
from spoc.models import Location, LocationHeader, Header

class Command(BaseCommand):
    help = 'Merge location from oei and header tables.'
            
    def handle(self, *args, **options):
        locations = Location.objects.all()
        
        for location in locations:
            oei_locations = LocationHeader.objects.filter(oei_location=location)
            headers = LocationHeader.objects.filter(header__locationid=location.locationid)

            if not oei_locations.exists() and headers.exists():
                location_header = headers[0]
                location_header.oei_location = location
                location_header.save()
            elif not oei_locations.exists() and not headers.exists():
                location_header = LocationHeader(oei_location=location)
                location_header.save()
            else:
                # oei_locations.exists() and not headers.exists()
                # oei_locations.exists() and headers.exists()
                # update or doe nothing
                continue

        headers = Header.objects.all()
        for header in headers:
            oei_locations = LocationHeader.objects.filter(
                oei_location__locationid=header.locationid)
            headers = LocationHeader.objects.filter(header=header)

            if oei_locations.exists() and not headers.exists():
                location_header = oei_locations[0]
                location_header.header = header
                location_header.save()
            elif not oei_locations.exists() and not headers.exists():
                location_header = LocationHeader(header=header)
                location_header.save()
            else:
                # oei_locations.exists() and not headers.exists()
                # oei_locations.exists() and headers.exists()
                # update or doe nothing
                continue
                            
        self.stdout.write('Successfully merged.')
