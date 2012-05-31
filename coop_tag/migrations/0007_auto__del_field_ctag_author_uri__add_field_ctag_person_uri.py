# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Ctag.author_uri'
        db.delete_column('coop_tag_ctag', 'author_uri')

        # Adding field 'Ctag.person_uri'
        db.add_column('coop_tag_ctag', 'person_uri', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Ctag.author_uri'
        db.add_column('coop_tag_ctag', 'author_uri', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True), keep_default=False)

        # Deleting field 'Ctag.person_uri'
        db.delete_column('coop_tag_ctag', 'person_uri')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 30, 15, 56, 3, 325331)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 30, 15, 56, 3, 325215)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'coop_tag.ctag': {
            'Meta': {'object_name': 'Ctag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_tag.TagCategory']", 'null': 'True', 'blank': 'True'}),
            'concept_uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 30, 15, 56, 3, 326471)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'fr'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 30, 15, 56, 3, 326564)', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'person_uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'uri_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'})
        },
        'coop_tag.ctaggeditem': {
            'Meta': {'object_name': 'CtaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coop_tag_ctaggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ctagged_items'", 'to': "orm['coop_tag.Ctag']"})
        },
        'coop_tag.tagcategory': {
            'Meta': {'ordering': "['position']", 'object_name': 'TagCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'label'", 'overwrite': 'False', 'db_index': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['coop_tag']
