# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationWNS'
        db.create_table(u'spoc_locationwns', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.OEI'])),
            ('wnsid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spoc.WNSAttribute'])),
        ))
        db.send_create_signal(u'spoc', ['LocationWNS'])

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


    def backwards(self, orm):
        # Deleting model 'LocationWNS'
        db.delete_table(u'spoc_locationwns')

        # Deleting model 'OEI'
        db.delete_table(u'spoc_oei')

        # Deleting model 'WNSAttribute'
        db.delete_table(u'spoc_wnsattribute')


    models = {
        u'spoc.location': {
            'Meta': {'ordering': "[u'created']", 'object_name': 'Location'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'python'", 'max_length': '100'}),
            'linenos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locationId': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "u'friendly'", 'max_length': '100'})
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