from spoc.settings import *

ENVIRONMENT = 'production'

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

SECRET_KEY = 'liu%(qb17(uvqc7f44i=_^e0bbv^gq11s0q5agzwrxv=c0ufd6'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'HHNK1',
        'USER': 'SPOC',
        'PASSWORD': 'spoc123',
        'HOST': '192.168.1.133',
        'PORT': '1521',
        },
    'default_': {
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
