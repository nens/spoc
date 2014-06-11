# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _
import jsonfield

# Create your models here.

class Location(models.Model):
    locationId = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "location"
        ordering = ['created']


class OEI(models.Model):

    objectid = models.IntegerField(null=False, blank=False)
    mpnident = models.CharField(max_length=24, null=False, blank=False)
    mpnomschr = models.CharField(max_length=100, null=True, blank=True)
    mpnsoort = models.IntegerField(null=True, blank=True)
    mpndatin = models.DateTimeField(null=True, blank=True)
    diffinfo = jsonfield.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "oei"
        verbose_name_plural = "oei"
        #ordering = ['']


class WNSAttribute(models.Model):
    
    wnsid = models.IntegerField(null=False, blank= False)
    wnsname = models.CharField(max_length=254, null=True, blank=True)
    wnshmax = models.IntegerField(null=True, blank=True)
    wnshmin = models.IntegerField(null=True, blank=True)
    wnssmax = models.IntegerField(null=True, blank=True)
    wnssmin = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = "wnsattribute"
        verbose_name_plural = "wnsattribute"
        ordering = ['wnsname']


class LocationWNS(models.Model):

    objectid = models.ForeignKey(OEI)
    wnsid = models.ForeignKey(WNSAttribute)

    class Meta:
        verbose_name = "locationwns"
        verbose_name_plural = "locationwns"
