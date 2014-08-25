# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Validation'
        db.create_table(u'spoc_validation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.ValidationField'])),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Header'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['Validation'])

        # Adding model 'ValidationField'
        db.create_table(u'spoc_validationfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Field'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Parameter'])),
        ))
        db.send_create_signal(u'spoc', ['ValidationField'])

        # Adding unique constraint on 'ValidationField', fields ['field', 'parameter']
        db.create_unique(u'spoc_validationfield', ['field_id', 'parameter_id'])

        # Adding model 'Field'
        db.create_table(u'spoc_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'spoc', ['Field'])

        # Adding unique constraint on 'Header', fields ['location', 'parameter']
        db.create_unique(u'spoc_header', ['location_id', 'parameter_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Header', fields ['location', 'parameter']
        db.delete_unique(u'spoc_header', ['location_id', 'parameter_id'])

        # Removing unique constraint on 'ValidationField', fields ['field', 'parameter']
        db.delete_unique(u'spoc_validationfield', ['field_id', 'parameter_id'])

        # Deleting model 'Validation'
        db.delete_table(u'spoc_validation')

        # Deleting model 'ValidationField'
        db.delete_table(u'spoc_validationfield')

        # Deleting model 'Field'
        db.delete_table(u'spoc_field')


    models = {
        u'spoc.field': {
            'Meta': {'object_name': 'Field'},
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'spoc.gemal': {
            'GPGIDENT': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'GPGWNTPL': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'GPGZMRPL': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'ID_INT': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'primary_key': 'True'}),
            'KWKIDENT': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'KWKNAAM': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'KWKSOORT': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'Meta': {'object_name': 'Gemal', 'db_table': "u'oei'", 'managed': 'False'},
            'RICHTING': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'Y': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        u'spoc.header': {
            'Meta': {'ordering': "[u'location__locationid']", 'unique_together': "((u'location', u'parameter'),)", 'object_name': 'Header'},
            'begintime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hardmax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'hardmin': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'headers'", 'to': u"orm['spoc.ScadaLocation']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Parameter']", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
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