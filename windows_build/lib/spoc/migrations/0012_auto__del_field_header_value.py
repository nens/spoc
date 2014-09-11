# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Header.value'
        db.delete_column(u'spoc_header', 'value')


    def backwards(self, orm):
        # Adding field 'Header.value'
        db.add_column(u'spoc_header', 'value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True),
                      keep_default=False)


    models = {
        u'spoc.fews_oei_sluizen': {
            'GPGIN': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'GPGINWP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'GPGINZP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'GPGUIT': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'GPGUITWP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'GPGUITZP': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'HYPERLINK': ('django.db.models.fields.CharField', [], {'max_length': '240', 'null': 'True', 'blank': 'True'}),
            'ID_INT': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'primary_key': 'True'}),
            'KSLBOKBE': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSLBOKBO': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSLFUNPA': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSLIDENT': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'KSLINLAT': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSLKOLBR': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSLKOLHG': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSLLENGT': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSLNAAM': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'KSLOMSCH': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'KSLPASBR': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSLSOORT': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSLSTATU': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'MEMO': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'METBRON': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'METINWDAT': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'METINWWYZ': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'METOPMERK': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'FEWS_OEI_SLUIZEN', 'db_table': "u'FEWS_OEI_SLUIZEN'", 'managed': 'False'},
            'OBJDERDE': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'OPMERKING': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'RICHTING': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'Y': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        u'spoc.fews_oei_stuwen': {
            'GPGBES': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'GPGBESWP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'GPGBESZP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'GPGBOS': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'GPGBOSWP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'GPGBOSZP': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'HYPERLINK': ('django.db.models.fields.CharField', [], {'max_length': '240', 'null': 'True', 'blank': 'True'}),
            'ID_INT': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'primary_key': 'True'}),
            'KSTAANT': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTBREED': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSTDSBRE': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSTFUNCT': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTHOOGT': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSTIDENT': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'KSTINLAT': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTJAAR': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'KSTKRVRM': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTMAXKH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSTMINKH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'KSTNAAM': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'KSTNAPD': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'KSTNAPH': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'KSTOMSCH': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'KSTPASBR': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTREGEL': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTSOORT': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'KSTSTATU': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'MEMO': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'METBRON': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'METINWDAT': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'METINWWYZ': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'METOPMERK': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'FEWS_OEI_STUWEN', 'db_table': "u'FEWS_OEI_STUWEN'", 'managed': 'False'},
            'OBJDERDE': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'OPMERKING': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'RICHTING': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'Y': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        u'spoc.field': {
            'Meta': {'object_name': 'Field'},
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'spoc.header': {
            'Meta': {'ordering': "[u'location__locationid']", 'unique_together': "((u'location', u'parameter'),)", 'object_name': 'Header'},
            'begintime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'headers'", 'to': u"orm['spoc.ScadaLocation']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Parameter']", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'spoc.headerformula': {
            'Meta': {'object_name': 'HeaderFormula'},
            'coef1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef4': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef5': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef6': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef7': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'coef8': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'dstart': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dstop': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'formula_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Header']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'spoc.location': {
            'Meta': {'ordering': "[u'created']", 'object_name': 'Location'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fews': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forward': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oei_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.OEILocation']", 'null': 'True', 'blank': 'True'}),
            'scada_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.ScadaLocation']", 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'spoc.locationsort': {
            'Meta': {'ordering': "[u'sort']", 'object_name': 'LocationSort'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'spoc.oeilocation': {
            'Meta': {'ordering': "[u'locationname']", 'object_name': 'OEILocation'},
            'gpgident': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'gpgwntpl': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'gpgzmrpl': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'locationname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'sort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.LocationSort']"}),
            'x': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '3', 'blank': 'True'}),
            'y': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'})
        },
        u'spoc.parameter': {
            'Meta': {'ordering': "[u'id']", 'object_name': 'Parameter'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'spoc.scadalocation': {
            'Meta': {'ordering': "[u'locationname']", 'object_name': 'ScadaLocation'},
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'locationname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Source']", 'null': 'True', 'blank': 'True'})
        },
        u'spoc.source': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Source'},
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'spoc.validation': {
            'Meta': {'object_name': 'Validation'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.ValidationField']"}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Header']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        u'spoc.validationfield': {
            'Meta': {'unique_together': "((u'field', u'parameter'),)", 'object_name': 'ValidationField'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Parameter']"})
        }
    }

    complete_apps = ['spoc']