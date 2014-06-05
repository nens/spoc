# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Location(models.Model):
    locationId = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "location"
        ordering = ['name']
    
