
from django.core.management.base import BaseCommand, CommandError
from spoc import models

class Command(BaseCommand):
    help = "Create data if it doesn't exist."
  
    def handle(self, *args, **options):
        self.stdout.write('Start creating initial divers for "WNSHDB35"...')
        headers = models.Header.objects.filter(parameter__id="WNSHDB35")
        count = 0
        for header in headers:
            divers = header.diver_set.all()
            if divers.exists():
                continue
            else:
                diver = models.Diver(header=header)
                diver.save()
                count = count + 1
        self.stdout.write('created {} divers'.format(count) )
        
        
                
