# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _
import jsonfield

# Create your models here.


class LocationSort(models.Model):
    sort = models.CharField(max_length=30)

    def __unicode__(self):
        return self.sort

    class Meta:
        ordering = ['sort']


class Location(models.Model):
    """Contain location imported from OEI management system."""
 
    locationid = models.CharField(primary_key=True, max_length=100)
    locationname = models.CharField(max_length=255, null=True, blank=True)
    sort = models.ForeignKey(LocationSort)
    objectid = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    gpgzmrpl = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    gpgwntpl = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)

    def __unicode__(self):
        return self.locationid

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "location"
        #ordering = ['created']


class Parameter(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
    

class Source(models.Model):
    """Scada. """
    SCADA_CSV = 'CSV'
    SCADA_PIXML = 'PIXML'
    SOURCE_CHOICES = (
        (SCADA_CSV, 'Scada csv'),
        (SCADA_PIXML, 'Scade pixml'),
    )
    name = models.CharField(primary_key=True, max_length=255)
    directory = models.CharField(max_length=255, null=True, blank=True)
    source_type = models.CharField(max_length=50, choices=SOURCE_CHOICES)

    def __unicode__(self):
        return "{0} | {1}".format(self.name, self.directory) 
    
    class Meta:
        ordering = ['name']


class Header(models.Model):
    """Locations, parameter from scada."""
    locationid = models.CharField(max_length=100)
    locationname = models.CharField(max_length=255, null=True, blank=True)
    parameter = models.ForeignKey(Parameter, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    value = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    begintime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    source = models.ForeignKey(Source)

    class Meta:
        ordering = ['locationid']

    def __unicode__(self):
        parameterid = None
        if self.parameter is not None:
            parameterid = self.parameter.id
        return "{0} -- {1}".format(self.locationid, parameterid)


class LocationHeader(models.Model):
    """Location from management end real-world envarement."""
    oei_location = models.ForeignKey(Location, null=True, blank=True,
                                     help_text='Locations from oei management system.')
    header = models.ForeignKey(Header, null=True, blank=True,
                                   help_text='TimeSeries headers from scadas.')

    def __unicode__(self):
        m = None
        r = None
        if self.oei_location is not None:
            m = self.oei_location.locationid
        if self.header is not None:
            r = self.header.locationid
        return "OEI: {0} -- SCADA: {1}".format(m, r)

    class Meta:
        ordering = ['oei_location__locationid']


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


class Gemal(models.Model):
    
    ID_INT = models.CharField(primary_key=True, unique=True, max_length=64)
    KWKNAAM = models.CharField(max_length=64)
    GPGIDENT = models.CharField(max_length=64)
    KWKIDENT = models.CharField(max_length=64)
    KWKSOORT = models.CharField(max_length=64)
    RICHTING = models.CharField(max_length=64)
    X = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    Y = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    GPGZMRPL = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    GPGWNTPL = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)

    class Meta:
        managed = False
        db_table = 'oei'

    def __unicode__(self):
        return u'%s' % self.GPGIDENT
