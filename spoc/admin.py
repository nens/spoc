# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin

from spoc import models


admin.site.register(models.OEI)
admin.site.register(models.WNSAttribute)
