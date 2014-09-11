
from django.core.management.base import BaseCommand, CommandError
from spoc.models import Location, ScadaLocation, OEILocation

class Command(BaseCommand):
    help = 'Merge location from oei and header tables.'
            
    def handle(self, *args, **options):
        oei_locations = OEILocation.objects.all()
        
        for oei_location in oei_locations:
            m_oei_locations = Location.objects.filter(oei_location=oei_location)
            m_scada_locations = Location.objects.filter(
                scada_location__locationid=oei_location.locationid)

            if not m_oei_locations.exists() and m_scada_locations.exists():
                location = m_scada_locations[0]
                location.oei_location = oei_location
                location.save()
            elif not m_oei_locations.exists() and not m_scada_locations.exists():
                location = Location(oei_location=oei_location)
                location.save()
            else:
                # m_oei_locations.exists() and not m_scada_locations.exists()
                # m_oei_locations.exists() and m_scada_locations.exists()
                # update or doe nothing
                continue

        scada_locations = ScadaLocation.objects.all()
        for scada_location in scada_locations:
            m_oei_locations = Location.objects.filter(
                oei_location__locationid=scada_location.locationid)
            m_scada_locations = Location.objects.filter(scada_location=scada_location)

            if m_oei_locations.exists() and not m_scada_locations.exists():
                location = m_oei_locations[0]
                location.scada_location = scada_location
                location.save()
            elif not m_oei_locations.exists() and not m_scada_locations.exists():
                location = Location(scada_location=scada_location)
                location.save()
            else:
                # m_oei_locations.exists() and not m_scada_locations.exists()
                # m_oei_locations.exists() and m_scada_locations.exists()
                # update or doe nothing
                continue
                            
        self.stdout.write('Successfully merged.')
