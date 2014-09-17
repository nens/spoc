from django.core.management.base import BaseCommand, CommandError

from spoc.models import (
    OEILocation,
    LocationSort,
    FEWS_OEI_SLUIZEN,
    FEWS_OEI_STUWEN,
	FEWS_OEI_GEMALEN,
	FEWS_OEI_MEETPUNTEN,
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
        self.sync_gemalen()
        self.sync_meetpunten()

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
                oei_location.gpginzp = location.GPGINZP or None
                oei_location.gpginwp = location.GPGINWP or None
                oei_location.gpguit = location.GPGUIT or None
                oei_location.gpguitzp = location.GPGUITZP or None
                oei_location.gpguitwp = location.GPGUITWP or None
                oei_location.x = location.X or None
                oei_location.y = location.Y or None
                oei_location.status = location.KSLSTATU
                oei_location.debitf = location.KSLFUNPA # ?????
                oei_location.datumbg = location.METINWDAT or None
                oei_location.regelbg = '' # ?????
                oei_location.inlaatf = location.KSLINLAT
                oei_location.save()
                self.stdout.write('Update a ksl "%s"' % location.KSLIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new ksl "%s, %s"' % (location.KSLIDENT, location.KSLINLAT))
                
                OEILocation(
                    locationid=location.KSLIDENT,
                    locationname=location.KSLNAAM,
                    sort=self.get_location_sort(location.KSLSOORT),
                    objectid=location.ID_INT,
                    gpgin=location.GPGIN,
                    gpginzp=location.GPGINZP or None,
                    gpginwp=location.GPGINWP or None,
                    gpguit=location.GPGUIT or None,
                    gpguitzp=location.GPGUITZP or None,
                    gpguitwp=location.GPGUITWP or None,
                    x=location.X or None,
                    y=location.Y or None,
                    status=location.KSLSTATU,
                    debitf=location.KSLFUNPA, # ?????
                    datumbg=location.METINWDAT or None,
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
                oei_location.gpginzp = location.GPGBOSZP or None
                oei_location.gpginwp = location.GPGBOSWP or None
                oei_location.x = location.X or None
                oei_location.y = location.Y or None
                oei_location.status = location.KSTSTATU
                oei_location.debitf = location.KSTFUNCT
                oei_location.datumbg = location.METINWDAT or None
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
                    gpginzp=location.GPGBOSZP or None,
                    gpginwp=location.GPGBOSWP or None,
                    x=location.X or None,
                    y=location.Y or None,
                    status=location.KSTSTATU,
                    debitf=location.KSTFUNCT,
                    datumbg=location.METINWDAT or None,
                    regelbg=location.KSTREGEL,
                    inlaatf=location.KSTINLAT
                ).save()
        self.stdout.write('Successfully passed.')

    def sync_gemalen(self):
        locations = FEWS_OEI_GEMALEN.objects.using('ws_lezen').all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.KGMIDENT)
                oei_location.locationname = location.KGMNAAM
                oei_location.sort = self.get_location_sort(location.KGMSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgin = location.GPGIN
                oei_location.gpginzp = location.GPGINZP or None
                oei_location.gpginwp = location.GPGINWP or None
                oei_location.gpguit = location.GPGUIT or None
                oei_location.gpguitzp = location.GPGUITZP or None
                oei_location.gpguitwp = location.GPGUITWP or None
                oei_location.x = location.X or None
                oei_location.y = location.Y or None
                oei_location.status = location.KGMSTATU
                oei_location.debitf = location.KGMFUNPA # ?????
                oei_location.datumbg = location.METINWDAT or None
                oei_location.regelbg = '' # ?????
                oei_location.inlaatf = location.KGMINLAT
                oei_location.save()
                self.stdout.write('Update a kgm "%s"' % location.KGMIDENT)
            except OEILocation.DoesNotExist:
                self.stdout.write('Insert a new kgm "%s"' % location.KGMIDENT)
                
                OEILocation(
                    locationid=location.KGMIDENT,
                    locationname=location.KGMNAAM,
                    sort=self.get_location_sort(location.KGMSOORT),
                    objectid=location.ID_INT,
                    gpgin=location.GPGIN,
                    gpginzp=location.GPGINZP or None,
                    gpginwp=location.GPGINWP or None,
                    gpguit=location.GPGUIT or None,
                    gpguitzp=location.GPGUITZP or None,
                    gpguitwp=location.GPGUITWP or None,
                    x=location.X or None,
                    y=location.Y or None,
                    status=location.KGMSTATU,
                    debitf=location.KGMFUNPA, # ?????
                    datumbg=location.METINWDAT or None,
                    regelbg='', # ?????
                    inlaatf=location.KGMINLAT
                ).save()

    def sync_meetpunten(self):
        locations = FEWS_OEI_MEETPUNTEN.objects.using('ws_lezen').all()
        for location in locations:
            try:
                oei_location = OEILocation.objects.get(locationid=location.MPNIDENT)
                oei_location.locationname = location.MPNNAAM
                oei_location.sort = self.get_location_sort(location.MPNSOORT)
                oei_location.objectid = location.ID_INT
                oei_location.gpgin = location.GPG
                oei_location.gpginzp = location.GPGZP or None
                oei_location.gpginwp = location.GPGWP or None
                oei_location.x = location.X or None
                oei_location.y = location.Y or None
                oei_location.status = location.MPNSTATU
                oei_location.debitf = location.MPNDEBMT # ?????
                oei_location.datumbg = location.METINWDAT or None
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
                    gpginzp=location.GPGZP or None,
                    gpginwp=location.GPGWP or None,
                    x=location.X or None,
                    y=location.Y or None,
                    status=location.MPNSTATU,
                    debitf=location.MPNDEBMT, # ?????
                    datumbg=location.METINWDAT or None,
                    regelbg='', # ?????
                    inlaatf='',
                ).save()
