# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from spoc.settings import *

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
# By default, var/log/django.log gets WARN level logging, the console gets
# DEBUG level logging.

# ENGINE: 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# In case of geodatabase, prepend with:
# django.contrib.gis.db.backends.(postgis)
DATABASES = {
    # If you want to use another database, consider putting the database
    # settings in localsettings.py. Otherwise, if you change the settings in
    # the current file and commit them to the repository, other developers will
    # also use these settings whether they have that database or not.
    # One of those other developers is Jenkins, our continuous integration
    # solution. Jenkins can only run the tests of the current application when
    # the specified database exists. When the tests cannot run, Jenkins sees
    # that as an error.
    'default': {
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'sqlite', 'test.db'),
        'ENGINE': 'django.db.backends.sqlite3',
        # If you want to use postgres, use the two lines below.
        # 'NAME': 'spoc',
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # empty string for localhost.
        'PORT': '',  # empty string for default.
        },
    'kwk': {
        'NAME': 'oei',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'buildout',
        'PASSWORD': 'buildout',
        'HOST': 'vmhost',
        'PORT': '5432',
        },
    'kwk-oracle': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'HHNK1',
        'USER': 'SPOC',
        'PASSWORD': 'spoc123',
        'HOST': '192.168.1.133',
        'PORT': '1521',
        },
    }


try:
    from spoc.localsettings import *
    # For local dev overrides.
except ImportError:
    pass
