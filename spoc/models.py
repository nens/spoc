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


class OEILocation(models.Model):
    """Contain location imported from OEI management system."""
 
    locationid = models.CharField(primary_key=True, max_length=100)
    locationname = models.CharField(max_length=255, null=True, blank=True)
    gpgident = models.CharField(max_length=10, null=True, blank=True)
    sort = models.ForeignKey(LocationSort)
    objectid = models.IntegerField()
    gpgzmrpl = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    gpgwntpl = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    x = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=19)
    y = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=19)
    def __unicode__(self):
        return self.locationid

    class Meta:
        ordering = ['locationname']


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


class ScadaLocation(models.Model):
    """Location from scada."""

    locationid = models.CharField(primary_key=True, max_length=100)
    locationname = models.CharField(max_length=255, null=True, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)

    def __unicode__(self):
        if self.locationname is None:
            return self.locationid
        else:
            return self.locationname

    class Meta:
        ordering = ['locationname']


class Header(models.Model):
    """Locations, parameter from scada."""
    location = models.ForeignKey(ScadaLocation, related_name='headers')
    parameter = models.ForeignKey(Parameter, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    value = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    begintime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    hardmax = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    hardmin = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)

    class Meta:
        ordering = ['location__locationid']
        unique_together = (('location', 'parameter'),)

    def __unicode__(self):
        parameterid = None
        if self.parameter is not None:
            parameterid = self.parameter.id
        return "{0} -- {1}".format(self.location.locationid, parameterid)

    @property
    def validations(self):
        self.add_validations()
        return self.validation_set.all()

    def add_validations(self):
        """Add or delete validations."""
        validationfields = self.parameter.validationfield_set.all()
        validations = self.validation_set.all()
        for validationfield in validationfields:
            if validationfield not in [v.field for v in validations]:
                validation = Validation(**{'field': validationfield, 'header': self})
                validation.save()
                self.validation_set.add(validation)


class Location(models.Model):
    """Location from management end real-world envarement."""
    oei_location = models.ForeignKey(OEILocation, null=True, blank=True,
                                     help_text='Locations from oei management system.')
    scada_location = models.ForeignKey(ScadaLocation, null=True, blank=True,
                                   help_text='Locations from scadas.')
    fews = models.BooleanField(default=False)
    forward = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        m = None
        r = None
        if self.oei_location is not None:
            m = self.oei_location.locationid
        if self.scada_location is not None:
            r = self.scada_location.locationid
        return "OEI: {0} -- SCADA: {1}".format(m, r)

    class Meta:
        ordering = ['created']


class Field(models.Model):
    """The field for validation or formule."""
    VALIDATION = 'VALIDATION'
    FORMULA = ''
    TYPE_CHOICES = (
        ('VALIDATION', 'Validation'),
        ('FORMULA', 'Formula'),
    )
    name = models.CharField(max_length=50)
    field_type = models.CharField(max_length=15, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.name


class ValidationField(models.Model):
    
    field = models.ForeignKey(Field)
    parameter = models.ForeignKey(Parameter)

    def __inicode__(self):
        return "{0}:{1}".format(
            self.field.name, self.parameter.id)

    def __str__(self):
        return str(self.field.name)

    class Meta:
        unique_together = (('field', 'parameter'),)
        

class Validation(models.Model):

        field = models.ForeignKey(ValidationField)
        header = models.ForeignKey(Header)
        value = models.DecimalField(null=True, blank=True,
                                    decimal_places=3, max_digits=9)

        def __unicode__(self):
            return self.field.field.name

    
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
