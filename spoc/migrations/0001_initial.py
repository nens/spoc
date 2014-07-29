# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationSort'
        db.create_table(u'spoc_locationsort', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'spoc', ['LocationSort'])

        # Adding model 'OEILocation'
        db.create_table(u'spoc_oeilocation', (
            ('locationid', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('locationname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.LocationSort'])),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('gpgzmrpl', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
            ('gpgwntpl', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['OEILocation'])

        # Adding model 'Parameter'
        db.create_table(u'spoc_parameter', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['Parameter'])

        # Adding model 'Source'
        db.create_table(u'spoc_source', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('directory', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'spoc', ['Source'])

        # Adding model 'ScadaLocation'
        db.create_table(u'spoc_scadalocation', (
            ('locationid', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('locationname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['ScadaLocation'])

        # Adding model 'Header'
        db.create_table(u'spoc_header', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.ScadaLocation'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Parameter'], null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
            ('begintime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('endtime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Source'])),
        ))
        db.send_create_signal(u'spoc', ['Header'])

        # Adding model 'Location'
        db.create_table(u'spoc_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oei_location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.OEILocation'], null=True, blank=True)),
            ('scada_location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.ScadaLocation'], null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['Location'])


    def backwards(self, orm):
        # Deleting model 'LocationSort'
        db.delete_table(u'spoc_locationsort')

        # Deleting model 'OEILocation'
        db.delete_table(u'spoc_oeilocation')

        # Deleting model 'Parameter'
        db.delete_table(u'spoc_parameter')

        # Deleting model 'Source'
        db.delete_table(u'spoc_source')

        # Deleting model 'ScadaLocation'
        db.delete_table(u'spoc_scadalocation')

        # Deleting model 'Header'
        db.delete_table(u'spoc_header')

        # Deleting model 'Location'
        db.delete_table(u'spoc_location')


    models = {
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
            'Meta': {'ordering': "[u'location__locationid']", 'object_name': 'Header'},
            'begintime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.ScadaLocation']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Parameter']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Source']"}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        u'spoc.location': {
            'Meta': {'ordering': "[u'oei_location__locationid']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oei_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.OEILocation']", 'null': 'True', 'blank': 'True'}),
            'scada_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.ScadaLocation']", 'null': 'True', 'blank': 'True'})
        },
        u'spoc.locationsort': {
            'Meta': {'ordering': "[u'sort']", 'object_name': 'LocationSort'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'spoc.oeilocation': {
            'Meta': {'object_name': 'OEILocation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gpgwntpl': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'gpgzmrpl': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'locationname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'sort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.LocationSort']"})
        },
        u'spoc.parameter': {
            'Meta': {'ordering': "[u'id']", 'object_name': 'Parameter'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'spoc.scadalocation': {
            'Meta': {'ordering': "[u'locationname']", 'object_name': 'ScadaLocation'},
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'locationname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'spoc.source': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Source'},
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['spoc']