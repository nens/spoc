
from django.core.management.base import BaseCommand, CommandError
from spoc.models import OEILocation, LocationSort, Gemal

class Command(BaseCommand):
    help = 'Import oei locations.'

    def get_location_sort(self, l_sort):
        location_sorts = LocationSort.objects.filter(sort=l_sort)
        
        if location_sorts.exists():
            location_sort = location_sorts[0]
        else:
            self.stdout.write("Create a new location sort {}.".format(l_sort))
            location_sort = LocationSort(sort=l_sort)
            location_sort.save()
        return location_sort               
        
    def handle(self, *args, **options):
        locations = Gemal.objects.using('kwk').all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.KWKIDENT)
                oei_location.locationname = location.KWKNAAM
                oei_location.sort=self.get_location_sort(location.KWKSOORT)
                oei_location.objectid=location.ID_INT
                oei_location.gpgzmrpl=location.GPGZMRPL
                oei_location.gpgwntpl=location.GPGWNTPL
                oei_location.save()
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new kwk "%s"' % location.KWKIDENT)
                
                OEILocation(locationid=location.KWKIDENT,
                         locationname=location.KWKNAAM,
                         sort=self.get_location_sort(location.KWKSOORT),
                         objectid=location.ID_INT,
                         gpgzmrpl=location.GPGZMRPL,
                         gpgwntpl=location.GPGWNTPL
                ).save()
                
        self.stdout.write('Successfully passed.')
