# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin

from spoc import models

admin.site.register(models.Location)
admin.site.register(models.LocationSort)
admin.site.register(models.OEILocation)
admin.site.register(models.ScadaLocation)
admin.site.register(models.Parameter)
admin.site.register(models.Source)
admin.site.register(models.Header)
