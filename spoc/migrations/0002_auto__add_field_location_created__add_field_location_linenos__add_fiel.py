# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Location.created'
        db.add_column(u'spoc_location', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 6, 6, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Location.linenos'
        db.add_column(u'spoc_location', 'linenos',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Location.language'
        db.add_column(u'spoc_location', 'language',
                      self.gf('django.db.models.fields.CharField')(default=u'python', max_length=100),
                      keep_default=False)

        # Adding field 'Location.style'
        db.add_column(u'spoc_location', 'style',
                      self.gf('django.db.models.fields.CharField')(default=u'friendly', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Location.created'
        db.delete_column(u'spoc_location', 'created')

        # Deleting field 'Location.linenos'
        db.delete_column(u'spoc_location', 'linenos')

        # Deleting field 'Location.language'
        db.delete_column(u'spoc_location', 'language')

        # Deleting field 'Location.style'
        db.delete_column(u'spoc_location', 'style')


    models = {
        u'spoc.location': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Location'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'python'", 'max_length': '100'}),
            'linenos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locationId': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "u'friendly'", 'max_length': '100'})
        }
    }

    complete_apps = ['spoc']