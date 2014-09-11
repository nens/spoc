# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import jsonfield
import string

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class LocationSort(models.Model):
    sort = models.CharField(max_length=30)

    def __unicode__(self):
        return self.sort

    class Meta:
        ordering = ['sort']


class OEILocation(models.Model):
    """Contain location imported from OEI management system."""
    
    objectid = models.IntegerField()
    sort = models.ForeignKey(LocationSort, null=True, blank=True)
    locationid = models.CharField(primary_key=True, max_length=100)
    locationname = models.CharField(max_length=255, null=True, blank=True)
    gpgin = models.CharField(max_length=10, null=True, blank=True)
    gpguit = models.CharField(max_length=10, null=True, blank=True)
    gpginzp = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    gpginwp = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    gpguitzp = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    gpguitwp = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    status = models.CharField(max_length=255, null=True, blank=True)
    debitf = models.CharField(max_length=255, null=True, blank=True)
    datumbg = models.DateTimeField(null=True, blank=True)
    regelbg = models.CharField(max_length=255, null=True, blank=True)
    inlaatf = models.CharField(max_length=255, null=True, blank=True)  
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)

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
    #value = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    begintime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)

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
    """
    The field for validation or formule.
    Use prefix to map with parameter for fews configuration.
    """
    VALIDATION = 'VALIDATION'
    FORMULA = 'FORMULA'
    PREFIXES = string.uppercase
    PREFIX_CHOICES = tuple((l, l) for l in PREFIXES)
    TYPE_CHOICES = (
        (VALIDATION, 'Validation'),
        (FORMULA, 'Formula'),
    )
    name = models.CharField(max_length=50)
    field_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    prefix = models.CharField(max_length=1, choices=PREFIX_CHOICES)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('field_type', 'prefix'),)


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
                                    decimal_places=4, max_digits=10)

        def __unicode__(self):
            return self.field.field.name


class FormulaType(models.Model):
    
    DEFAULT_TYPES = ['stuw01','stuw02',  'stuw03', 'stuw04',
                     'stuw05', 'duikerformule', 'inlaat_stuw01', 
                     'polynoom']
    
    code = models.CharField(primary_key=True, max_length=20)

    def __unicode__(self):
        return self.code

    def __str__(self):
        return self.code


class HeaderFormula(models.Model):
    
    header = models.ForeignKey(Header)
    dstart = models.DateField(null=True, blank=True)
    dstop = models.DateField(null=True, blank=True)
    formula_type = models.ForeignKey(FormulaType)
    coef01 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef02 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef03 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef04 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef05 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef06 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef07 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef08 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef09 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef10 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef11 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    coef12 = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)    


class FEWS_OEI_SLUIZEN(models.Model):
    ID_INT = models.CharField(primary_key=True, unique=True, max_length=64)
    KSLIDENT = models.CharField(max_length=24)
    KSLNAAM = models.CharField(max_length=100, null=True, blank=True)
    KSLSOORT = models.IntegerField(max_length=5, null=True, blank=True)
    RICHTING = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    X = models.FloatField(null=True, blank=True)
    Y = models.FloatField(null=True, blank=True)
    GPGIN = models.CharField(max_length=24, null=True, blank=True)
    GPGINZP = models.IntegerField(null=True, blank=True)
    GPGINWP = models.IntegerField(null=True, blank=True)
    GPGUIT = models.CharField(max_length=24, null=True, blank=True)
    GPGUITZP = models.CharField(max_length=24)
    GPGUITWP = models.IntegerField(null=True, blank=True)
    KSLOMSCH = models.CharField(max_length=100, null=True, blank=True)
    OPMERKING = models.CharField(max_length=254, null=True, blank=True)
    KSLSTATU = models.IntegerField(max_length=5, null=True, blank=True)
    KSLINLAT = models.IntegerField(max_length=5, null=True, blank=True)
    KSLBOKBO = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSLBOKBE = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSLLENGT = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSLKOLBR = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSLKOLHG = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSLPASBR = models.IntegerField(max_length=5, null=True, blank=True)
    KSLFUNPA = models.IntegerField(max_length=5, null=True, blank=True)
    OBJDERDE = models.CharField(max_length=100, null=True, blank=True)
    HYPERLINK = models.CharField(max_length=240, null=True, blank=True)
    MEMO = models.TextField(max_length=500, null=True, blank=True)
    METBRON = models.CharField(max_length=100, null=True, blank=True)
    METINWWYZ = models.IntegerField(max_length=5, null=True, blank=True)
    METINWDAT = models.DateTimeField(null=True, blank=True)
    METOPMERK = models.CharField(max_length=254, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'FEWS_OEI_SLUIZEN'


class FEWS_OEI_STUWEN(models.Model):
    ID_INT = models.CharField(primary_key=True, unique=True, max_length=64)
    KSTIDENT = models.CharField(max_length=24)
    KSTNAAM = models.CharField(max_length=100, null=True, blank=True)
    KSTSOORT = models.IntegerField(max_length=5, null=True, blank=True)
    RICHTING = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    X = models.FloatField(null=True, blank=True)
    Y = models.FloatField(null=True, blank=True)
    GPGBOS = models.CharField(max_length=24, null=True, blank=True)
    GPGBOSZP = models.IntegerField(null=True, blank=True)
    GPGBOSWP = models.IntegerField(null=True, blank=True)
    GPGBES = models.CharField(max_length=24, null=True, blank=True)
    GPGBESZP = models.IntegerField(null=True, blank=True)
    GPGBESWP = models.IntegerField(null=True, blank=True)
    KSTOMSCH = models.CharField(max_length=100, null=True, blank=True)
    OPMERKING = models.CharField(max_length=254, null=True, blank=True)
    KSTSTATU = models.IntegerField(max_length=5, null=True, blank=True)
    KSTINLAT = models.IntegerField(max_length=5, null=True, blank=True)
    KSTFUNCT = models.IntegerField(max_length=5, null=True, blank=True)
    KSTAANT = models.IntegerField(max_length=5, null=True, blank=True)
    KSTKRVRM = models.IntegerField(max_length=5, null=True, blank=True)
    KSTREGEL = models.IntegerField(max_length=5, null=True, blank=True)
    KSTMINKH = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSTMAXKH = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSTBREED = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSTHOOGT = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSTDSBRE = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    KSTJAAR = models.IntegerField(max_length=4, null=True, blank=True)
    KSTNAPH = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    KSTNAPD = models.DateTimeField(null=True, blank=True)
    KSTPASBR = models.IntegerField(max_length=5, null=True, blank=True)
    OBJDERDE = models.CharField(max_length=100, null=True, blank=True)
    HYPERLINK = models.CharField(max_length=240, null=True, blank=True)
    MEMO = models.TextField(max_length=500, null=True, blank=True)
    METBRON = models.CharField(max_length=100, null=True, blank=True)
    METINWWYZ = models.IntegerField(max_length=5, null=True, blank=True)
    METINWDAT = models.DateTimeField(null=True, blank=True)
    METOPMERK = models.CharField(max_length=254, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'FEWS_OEI_STUWEN'


class FEWS_OEI_GEMALEN(models.Model):
    ID_INT = models.CharField(primary_key=True, unique=True, max_length=64)
    KGMIDENT = models.CharField(max_length=24)
    KGMNAAM = models.CharField(max_length=100, null=True, blank=True)
    KGMSOORT = models.IntegerField(max_length=5, null=True, blank=True)
    RICHTING = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    X = models.FloatField(null=True, blank=True)
    Y = models.FloatField(null=True, blank=True)
    GPGIN = models.CharField(max_length=24, null=True, blank=True)
    GPGINZP = models.IntegerField(null=True, blank=True)
    GPGINWP = models.IntegerField(null=True, blank=True)
    GPGUIT = models.CharField(max_length=24, null=True, blank=True)
    GPGUITZP = models.IntegerField(null=True, blank=True)
    GPGUITWP = models.IntegerField(null=True, blank=True)
    KGMOMSCH = models.CharField(max_length=100, null=True, blank=True)
    OPMERKING = models.CharField(max_length=254, null=True, blank=True)
    KGMSTATU = models.IntegerField(max_length=5, null=True, blank=True)
    KGMINLAT = models.IntegerField(max_length=5, null=True, blank=True)
    KGMKEREN = models.IntegerField(max_length=5, null=True, blank=True)
    KGMAFSL1 = models.IntegerField(max_length=5, null=True, blank=True)
    KGMAFSL2 = models.IntegerField(max_length=5, null=True, blank=True)
    KGMAAPOM = models.IntegerField(max_length=5, null=True, blank=True)
    KGMAANDR = models.IntegerField(max_length=5, null=True, blank=True)
    KGMLOZBU = models.IntegerField(max_length=5, null=True, blank=True)
    KGMBYPAS = models.IntegerField(max_length=5, null=True, blank=True)
    KGMJAAR = models.IntegerField(max_length=5, null=True, blank=True)
    KGMNAPD = models.DateTimeField(null=True, blank=True)
    KGMPASBR = models.IntegerField(max_length=5, null=True, blank=True)
    KGMFUNPA = models.IntegerField(max_length=5, null=True, blank=True)
    OBJDERDE = models.CharField(max_length=100, null=True, blank=True)
    HYPERLINK = models.CharField(max_length=240, null=True, blank=True)
    MEMO = models.TextField(max_length=500, null=True, blank=True)
    METBRON = models.CharField(max_length=100, null=True, blank=True)
    METINWWYZ = models.IntegerField(max_length=5, null=True, blank=True)
    METINWDAT = models.DateTimeField(null=True, blank=True)
    METOPMERK = models.CharField(max_length=254, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'FEWS_OEI_GEMALEN'


class FEWS_OEI_MEETPUNTEN(models.Model):
    ID_INT = models.CharField(primary_key=True, unique=True, max_length=64)
    MPNIDENT = models.CharField(max_length=24)
    MPNNAAM = models.CharField(max_length=100, null=True, blank=True)
    MPNSOORT = models.IntegerField(max_length=5, null=True, blank=True)
    X = models.FloatField(null=True, blank=True)
    Y = models.FloatField(null=True, blank=True)
    GPG = models.CharField(max_length=24, null=True, blank=True)
    GPGZP = models.IntegerField(null=True, blank=True)
    GPGWP = models.IntegerField(null=True, blank=True)
    MPN_ID = models.IntegerField(null=True, blank=True)
    MPNDATIN = models.DateTimeField(null=True, blank=True)
    MPNDATEI = models.DateTimeField(null=True, blank=True)
    MPNDEBMT = models.IntegerField(null=True, blank=True)
    MPNSTATU = models.IntegerField(max_length=5, null=True, blank=True)
    MPNSYS = models.TextField(max_length=500, null=True, blank=True)
    METBRON = models.CharField(max_length=100, null=True, blank=True)
    METINWWYZ = models.IntegerField(max_length=5, null=True, blank=True)
    METINWDAT = models.DateTimeField(null=True, blank=True)
    METOPMERK = models.CharField(max_length=254, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'FEWS_OEI_MEETPUNTEN'
