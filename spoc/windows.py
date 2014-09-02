from spoc.settings import *

ENVIRONMENT = 'production'

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'NAME': 'spoc',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'buildout',
        'PASSWORD': 'buildout',
        'HOST': 'localhost',
        'PORT': '5432',
        },
    'kwk': {
        'NAME': 'oei',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'buildout',
        'PASSWORD': 'buildout',
        'HOST': 'localhost',
        'PORT': '5432',
        },
    }

try:
    from spoc.localsettings import *
except ImportError:
    pass
