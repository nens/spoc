import os

DJANGO_SETTINGS_MODULE = 'spoc.windows'
BUILDOUT_DIR = r'D:\Lizard\spoc\windows_build' # vitens
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')
STATIC_URL = '/static/'

def setup_env():
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
    os.environ['BUILDOUT_DIR'] = BUILDOUT_DIR
