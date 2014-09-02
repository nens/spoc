#!/bin/sh

echo "Note: This needs \"sudo apt-get install zip rsync\"."
echo "Note: must be in the \"spoc\" root directory."
echo "Deleting the old \"windows_build/\" subdirectory."
sleep 5

rm -rf windows_build/

mkdir windows_build/
mkdir windows_build/var/
mkdir windows_build/var/log/
mkdir windows_build/var/static/
mkdir windows_build/lib/

# These are all pure Python packages. We can copy them straight from Linux to Windows.

for pkg in ampq anyjson billiard celery corsheaders dbfpy django django_extensions \
	    django_nose djcelery funtests jsonfield kombu markdown nose pytz \
	    rest_framework south spoc werkzeug cherrypy gunicorn
do
  rsync -r --verbose --exclude "*.pyc" --exclude "*.pyo" --exclude ".git" --exclude "settings/local.py" parts/omelette/${pkg}/ windows_build/lib/${pkg}/
done

for fil in six.py
do
  cp -R parts/omelette/${fil} windows_build/lib/${fil}
done

cp windows/*.cmd windows_build/

rm spoc-windows.zip
zip -r spoc-windows.zip windows_build -x \*.pyc \*.pyo .git local.py
