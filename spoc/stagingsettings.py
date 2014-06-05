# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from spoc.settings import *

DATABASES = {
    # Changed server from production to staging
    'default': {
        'NAME': 'spoc',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'spoc',
        'PASSWORD': 'v+_=bg*x*y',
        'HOST': 's-web-db-00-d03.external-nens.local',
        'PORT': '5432',
        },
    }

# TODO: add staging gauges ID here.
UI_GAUGES_SITE_ID = ''  # Staging has a separate one.
