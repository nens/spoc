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

        # Adding model 'Location'
        db.create_table(u'spoc_location', (
            ('locationid', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('locationname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.LocationSort'])),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('gpgzmrpl', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
            ('gpgwntpl', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['Location'])

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

        # Adding model 'Header'
        db.create_table(u'spoc_header', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locationid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('locationname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Parameter'], null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
            ('begintime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('endtime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Source'])),
        ))
        db.send_create_signal(u'spoc', ['Header'])

        # Adding model 'LocationHeader'
        db.create_table(u'spoc_locationheader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oei_location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Location'], null=True, blank=True)),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.Header'], null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['LocationHeader'])

        # Adding model 'OEI'
        db.create_table(u'spoc_oei', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('mpnident', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('mpnomschr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mpnsoort', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mpndatin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('diffinfo', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['OEI'])

        # Adding model 'WNSAttribute'
        db.create_table(u'spoc_wnsattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wnsid', self.gf('django.db.models.fields.IntegerField')()),
            ('wnsname', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('wnshmax', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wnshmin', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wnssmax', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wnssmin', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['WNSAttribute'])

        # Adding model 'LocationWNS'
        db.create_table(u'spoc_locationwns', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.OEI'])),
            ('wnsid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.WNSAttribute'])),
        ))
        db.send_create_signal(u'spoc', ['LocationWNS'])


    def backwards(self, orm):
        # Deleting model 'LocationSort'
        db.delete_table(u'spoc_locationsort')

        # Deleting model 'Location'
        db.delete_table(u'spoc_location')

        # Deleting model 'Parameter'
        db.delete_table(u'spoc_parameter')

        # Deleting model 'Source'
        db.delete_table(u'spoc_source')

        # Deleting model 'Header'
        db.delete_table(u'spoc_header')

        # Deleting model 'LocationHeader'
        db.delete_table(u'spoc_locationheader')

        # Deleting model 'OEI'
        db.delete_table(u'spoc_oei')

        # Deleting model 'WNSAttribute'
        db.delete_table(u'spoc_wnsattribute')

        # Deleting model 'LocationWNS'
        db.delete_table(u'spoc_locationwns')


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
            'Meta': {'ordering': "[u'locationid']", 'object_name': 'Header'},
            'begintime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'locationname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Parameter']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Source']"}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        u'spoc.location': {
            'Meta': {'object_name': 'Location'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gpgwntpl': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'gpgzmrpl': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'locationid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'locationname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'sort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.LocationSort']"})
        },
        u'spoc.locationheader': {
            'Meta': {'ordering': "[u'oei_location__locationid']", 'object_name': 'LocationHeader'},
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Header']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oei_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.Location']", 'null': 'True', 'blank': 'True'})
        },
        u'spoc.locationsort': {
            'Meta': {'ordering': "[u'sort']", 'object_name': 'LocationSort'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'spoc.locationwns': {
            'Meta': {'object_name': 'LocationWNS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.OEI']"}),
            'wnsid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spoc.WNSAttribute']"})
        },
        u'spoc.oei': {
            'Meta': {'object_name': 'OEI'},
            'diffinfo': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpndatin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mpnident': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'mpnomschr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mpnsoort': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {})
        },
        u'spoc.parameter': {
            'Meta': {'ordering': "[u'id']", 'object_name': 'Parameter'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'spoc.source': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Source'},
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'spoc.wnsattribute': {
            'Meta': {'ordering': "[u'wnsname']", 'object_name': 'WNSAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wnshmax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wnshmin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wnsid': ('django.db.models.fields.IntegerField', [], {}),
            'wnsname': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'wnssmax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wnssmin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spoc']