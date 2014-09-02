import os

if not 'DJANGO_SETTINGS_MODULE' in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'spoc.windows'

from django.core import management

if __name__ == '__main__':
    management.execute_from_command_line()

