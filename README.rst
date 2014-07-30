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
   
   $ bin/django sync_parameters --f=/path/to/csv/file/paramaters.csv

4. Import or update scada-locations and timeseries headers from scada-files (csv or pixml)

   $ bin/django scada_import

5. Combine the oei-locations with scada-locations

   $ bin/django mearge_locations


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
  optional QueryParameters:
    page=1 (deafault = 1)
    items_per_page=20 (default = 20)
