spoc
==========================================

Introduction

Usage, etc.


Post-nensskel project setup TODO
--------------------------------

Here are some instructions on what to do after you've created the project with
nensskel.

- Fill in a short description on https://github.com/nens/spoc if you
  haven't done so already.

- Use the same description in the ``setup.py``'s "description" field.

- Fill in your username and email address in the ``setup.py``, see the
  ``TODO`` fields.

- Check https://github.com/nens/spoc/settings/collaboration if the teams
  "Nelen & Schuurmans" and "Nelen & Schuurmans pull only" have access.

- Add a new jenkins job at
  http://buildbot.lizardsystem.nl/jenkins/view/sites/newJob. Job name should
  be "spoc", make the project a copy of the existing "wro" (for
  instance) project. On the next page, change the "github project" to
  ``https://github.com/nens/spoc/`` and
  "repository url" fields to ``git@github.com:nens/spoc.git``. The rest
  of the settings should be OK.

Later on, before releasing the site, adjust ``fabfile.cfg`` to point at the
correct server and configure raven/sentry and gaug.es in the django settings.


Initial setup
--------------------------------

Initially, there's no ``buildout.cfg``. You need to make that a symlink to the
correct configuration. On your development machine, that is
``development.cfg`` (and ``staging.cfg`` or ``production.cfg``, for instance
on the server)::

    $ ln -s development.cfg buildout.cfg

Then run bootstrap and buildout, as usual::

    $ python bootstrap.py
    $ bin/buildout

Set up a database (and yes, set up an admin user when asked)::

    $ bin/django syncdb
    $ bin/django migrate

And import two fixtures. The background_maps sets up a couple of lizard-map
defaults. Democontent gives you an initial homepage and a link to an example
WMS layer::

    $ bin/django loaddata background_maps
    $ bin/django loaddata democontent

Start the server::

    $ bin/django runserver


Windows
---------
* Check out the ``windows`` subdirectory, and customize it if needed.
* Check out the ``objectenbeheer/cherrypy_service`` subdirectory, and customize it if needed.
* Check out the ``objectenbeheer/settings/windows.py`` module, and customize it if needed.

* Run ``build_windows.sh`` from Linux to wrap everything in a nice zip.

* In Windows, download Python 2.7.x from http://www.python.org/download/.
* In Windows, download Psycopg2 from http://www.stickpeople.com/projects/python/win-psycopg/.
* In Windows, download PyWin32 from http://sourceforge.net/projects/pywin32/files/pywin32/.

* Extract the zip in the configured place, e.g. ``D:\Programs\objectenbeheer``.

* In Windows, configure your ``PYTHONPATH`` environment variable to point to the absolute path of the ``objectenbeheer\lib`` subdirectory.
  If you don't know how to do this, read https://kb.wisc.edu/cae/page.php?id=24500.

* To tune local settings like the database connection, create or edit ``objectenbeheer\lib\objectenbeheer\settings\local.py``.

* Collect static files: go to the install directory, and run ``collectstatic.cmd``.

* Do the usual Django syncdb + migrate stuff: go to the install directory, and run ``django.cmd syncdb`` and ``django.cmd migrate``.

* Want to install it as a service? Open an Administrator command prompt, go to the install directory, and use ``servicecontrol.cmd (install|remove|start|stop)``.

* Point your browser to http://127.0.0.1:8090.


Oracle (Windows)
-----------------

Download and extract http://www.oracle.com/technetwork/topics/winsoft-085727.html:
* instantclient-basic-nt-12.1.0.1.0.zip
* instantclient-sqlplus-nt-12.1.0.1.0.zip

Set environment variables:
ORACLE_HOME = ..\instantclient-sqlplus-nt-12.1.0.1.0\instantclient_12_1
LD_LIBRARY_PATH = ..\instantclient-basic-nt-12.1.0.1.0\instantclient_12_1
PATH = %PATH%;%ORACLE_HOME%;%LD_LABRARY_PATH%;


CORS settings
-------------------------------------
In case of the intraction between different domains set for production

    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ORIGIN_WHITELIST = (
        'http://xxxxx.xx',
    )


Usage
--------------------------------------
1. Add sources using admin interface. There are 2 types of sources: pixml and csv.
2. Synchronize OEI-location running 
   
   $ bin/django sync_oei

3. Import or update parameters from a csv-file running
   
   $ bin/django sync_parameters --f=/{buildout_dir}/spoc/data/paramaters.csv

4. Import or update scada-locations and timeseries headers from scada-files (csv or pixml)

   $ bin/django scada_import

5. Combine the oei-locations with scada-locations

   $ bin/django merge_locations

6. Insert formula types and ... 

   $ bin/django create_initial_data

7. Create configuration file. Exports location and formulas where fews=true.

   $ bin/django export_to_dbf

8. Insert parameters, fields, validation fields, headerformulas
   
   $ bin/django sync_validations --f=/{buildout_dir}/spoc/data/validations.csv

9. Bind validations with headers
   
   $ bin/django create_validations

10. Add initial diver for parameter WNSHDB35

    $ bin/django create_initial_divers


REST
------------------------------
Update locatons:
  curl https://spoc.staging.lizard.net/locations/1155/ -d '{"visible": true, "fews": false}' -X POST -u spoc:spoc
  
  editable fields: "visible", "fews", "forward"

Update headers:
  curl http://spoc.staging.lizard.net/scadalocations/headers/1690/ -d '{"hardmax": -10}' -X POST -u spoc:spoc
  
  editable fields: "hardmax", "hardmin"
  
Retrieve locations:
  https://spoc.staging.lizard.net/locations/?items_per_page=2&page=100
  
  optional QueryParameters: page (deafault = 1), items_per_page (default = 20)


Sorting
---------
Mapping sorting fields:
 
client side                    server side

‘oei_locatie’                  oei_location.loctionid
‘tijdreekscode’                scada_location.loctionid
‘naam’                         scada_location.locationname
‘bron’                         scada_location.source.name
 

example: 
    http://spoc.staging.lizard.net/locations/?page=1&items_per_page=10&sort=oei_locatie&order=asc
    http://spoc.staging.lizard.net/locations/?page=1&items_per_page=10&sort=oei_locatie&order=desc
