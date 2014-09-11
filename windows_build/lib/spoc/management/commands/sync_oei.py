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
        if l_sort is None:
            return None
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
        #self.sync_gemalen()
        #self.sync_meetpunten()

    def sync_sluizen(self):
        locations = FEWS_OEI_SLUIZEN.objects.using('ws_lezen').all()
        for location in locations:
            try:
                #import pdb; pdb.set_trace()
                oei_location = OEILocation.objects.get(locationid=location.KSLIDENT)
                oei_location.locationname = location.KSLNAAM
                oei_location.sort = self.get_location_sort(location.KSLSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgin = location.GPGIN
                oei_location.gpginzp = location.GPGINZP
                oei_location.gpginwp = location.GPGINWP
                oei_location.gpguit = location.GPGUIT
                oei_location.gpguitzp = location.GPGUITZP
                oei_location.gpguitwp = location.GPGUITWP
                oei_location.x = location.X
                oei_location.y = location.Y
                oei_location.status = location.KSLSTATU
                oei_location.debitf = location.KSLFUNPA # ?????
                oei_location.datumbg = location.METINWDAT
                oei_location.regelbg = '' # ?????
                oei_location.inlaatf = location.KSLINLAT
                oei_location.save()
                self.stdout.write('Update a ksl "%s"' % location.KSLIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new ksl "%s"' % location.KSLIDENT)
                
                OEILocation(
                    locationid=location.KSLIDENT,
                    locationname=location.KSLNAAM,
                    sort=self.get_location_sort(location.KSLSOORT),
                    objectid=location.ID_INT,
                    gpgin=location.GPGIN,
                    gpginzp=location.GPGINZP,
                    gpginwp=location.GPGINWP,
                    gpguit=location.GPGUIT,
                    gpguitzp=location.GPGUITZP,
                    gpguitwp=location.GPGUITWP,
                    x=location.X,
                    y=location.Y,
                    status=location.KSLSTATU,
                    debitf=location.KSLFUNPA, # ?????
                    datumbg=location.METINWDAT,
                    regelbg='', # ?????
                    inlaatf=location.KSLINLAT
                ).save()
    
    def sync_stuwen(self):
        locations = FEWS_OEI_STUWEN.objects.using('ws_lezen').all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.KSTIDENT)
                oei_location.locationname = location.KSTNAAM
                oei_location.sort = self.get_location_sort(location.KSTSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgin = location.GPGBOS
                oei_location.gpginzp = location.GPGBOSZP
                oei_location.gpginwp = location.GPGBOSWP
                oei_location.x = location.X
                oei_location.y = location.Y
                oei_location.status = location.KSTSTATU
                oei_location.debitf = location.KSTFUNCT
                oei_location.datumbg = location.METINWDAT
                oei_location.regelbg = location.KSTREGEL
                oei_location.inlaatf = location.KSTINLAT
                oei_location.save()
                self.stdout.write('Update a kst "%s"' % location.KSTIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new kst "%s"' % location.KSTIDENT)
                
                OEILocation(
                    locationid=location.KSTIDENT,
                    locationname=location.KSTNAAM,
                    sort=self.get_location_sort(location.KSTSOORT),
                    objectid=location.ID_INT,
                    gpgin=location.GPGBOS,
                    gpginzp=location.GPGBOSZP,
                    gpginwp=location.GPGBOSWP,
                    x=location.X,
                    y=location.Y,
                    status=location.KSTSTATU,
                    debitf=location.KSTFUNCT,
                    datumbg=location.METINWDAT,
                    regelbg=location.KSTREGEL,
                    inlaatf=location.KSTINLAT
                ).save()
        self.stdout.write('Successfully passed.')

    def sync_gemalen(self):
        locations = FEWS_OEI_GEMALEN.objects.using('ws_lezen').all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.KSLIDENT)
                oei_location.locationname = location.KSLNAAM
                oei_location.sort = self.get_location_sort(location.KSLSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgin = location.GPGIN
                oei_location.gpginzp = location.GPGINZP
                oei_location.gpginwp = location.GPGINWP
                oei_location.gpguit = location.GPGUIT
                oei_location.gpguitzp = location.GPGUITZP
                oei_location.gpguitwp = location.GPGUITWP
                oei_location.x = location.X
                oei_location.y = location.Y
                oei_location.status = location.KSLSTATU
                oei_location.debitf = location.KSLFUNPA # ?????
                oei_location.datumbg = location.METINWDAT
                oei_location.regelbg = '' # ?????
                oei_location.inlaatf = location.KSLINLAT
                oei_location.save()
                self.stdout.write('Update a ksl "%s"' % location.KSLIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new ksl "%s"' % location.KSLIDENT)
                
                OEILocation(
                    locationid=location.KSLIDENT,
                    locationname=location.KSLNAAM,
                    sort=self.get_location_sort(location.KSLSOORT),
                    objectid=location.ID_INT,
                    gpgin=location.GPGIN,
                    gpginzp=location.GPGINZP,
                    gpginwp=location.GPGINWP,
                    gpguit=location.GPGUIT,
                    gpguitzp=location.GPGUITZP,
                    gpguitwp=location.GPGUITWP,
                    x=location.X,
                    y=location.Y,
                    status=location.KSLSTATU,
                    debitf=location.KSLFUNPA, # ?????
                    datumbg=location.METINWDAT,
                    regelbg='', # ?????
                    inlaatf=location.KSLINLAT
                ).save()

    def sync_meetpunten(self):
        locations = FEWS_OEI_MEETPUNTEN.objects.all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.using('ws_lezen').get(locationid=location.MPNIDENT)
                oei_location.locationname = location.MPNNAAM
                oei_location.sort = self.get_location_sort(location.MPNSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgin = location.GPG
                oei_location.gpginzp = location.GPGZP
                oei_location.gpginwp = location.GPGWP
                oei_location.x = location.X
                oei_location.y = location.Y
                oei_location.status = location.MPNSTATU
                oei_location.debitf = location.MPNDEBMT # ?????
                oei_location.datumbg = location.METINWDAT
                oei_location.regelbg = '' # ?????
                oei_location.inlaatf = ''
                oei_location.save()
                self.stdout.write('Update a mpn "%s"' % location.MPNIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new mpn "%s"' % location.MPNIDENT)
                
                OEILocation(
                    locationid=location.MPNIDENT,
                    locationname=location.MPNNAAM,
                    sort=self.get_location_sort(location.MPNSOORT),
                    objectid=location.ID_INT,
                    gpgin=location.GPG,
                    gpginzp=location.GPGZP,
                    gpginwp=location.GPGWP,
                    x=location.X,
                    y=location.Y,
                    status=location.MPNSTATU,
                    debitf=location.MPNDEBMT, # ?????
                    datumbg=location.METINWDAT,
                    regelbg='', # ?????
                    inlaatf='',
                ).save()
