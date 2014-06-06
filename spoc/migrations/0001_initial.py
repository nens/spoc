# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'spoc_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locationId', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'spoc', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'spoc_location')


    models = {
        u'spoc.location': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locationId': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spoc']