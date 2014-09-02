from django.core.management.base import BaseCommand, CommandError

from spoc.models import (
    OEILocation,
    LocationSort,
    FEWS_OEI_SLUIZEN,
    FEWS_OEI_STUWEN,
)

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
        self.sync_sluizen()
        self.sync_stuwen()

    def sync_sluizen(self):
        locations = FEWS_OEI_SLUIZEN.objects.all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.KSLIDENT)
                oei_location.locationname = location.KSLNAAM
                oei_location.sort = self.get_location_sort(location.KSLSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgident = location.GPGIN
                oei_location.gpgzmrpl = location.GPGINZP
                oei_location.gpgwntpl = location.GPGUITWP
                oei_location.x = location.X
                oei_location.y = location.Y
                oei_location.save()
                self.stdout.write('Update a new ksl "%s"' % location.KSLIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new ksl "%s"' % location.KSLIDENT)
                
                OEILocation(locationid=location.KSLIDENT,
                         locationname=location.KSLNAAM,
                         sort=self.get_location_sort(location.KSLSOORT),
                         objectid=location.ID_INT,
                         gpgzmrpl=location.GPGINZP,
                         gpgwntpl=location.GPGUITWP
                ).save()
    
    def sync_stuwen(self):
        locations = FEWS_OEI_STUWEN.objects.all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.KSTIDENT)
                oei_location.locationname = location.KSTNAAM
                oei_location.sort = self.get_location_sort(location.KSTSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgident = location.GPGBOS
                oei_location.gpgzmrpl = location.GPGBOSZP
                oei_location.gpgwntpl = location.GPGBOSWP
                oei_location.x = location.X
                oei_location.y = location.Y
                oei_location.save()
                self.stdout.write('Update a new kst "%s"' % location.KSTIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new kst "%s"' % location.KSTIDENT)
                
                OEILocation(locationid=location.KSTIDENT,
                         locationname=location.KSTNAAM,
                         sort=self.get_location_sort(location.KSTSOORT),
                         objectid=location.ID_INT,
                         gpgzmrpl=location.GPGBOSZP,
                         gpgwntpl=location.GPGBOSWP
                ).save()
        self.stdout.write('Successfully passed.')
