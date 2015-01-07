# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'user_leave'
        db.create_table(u'leaveform_user_leave', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('leave_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('From_date', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('To_date', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('Timeoff', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('WDay_apply', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('Remarks', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'leaveform', ['user_leave'])

        # Adding model 'Leave_status'
        db.create_table(u'leaveform_leave_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('LeaveID', self.gf('django.db.models.fields.IntegerField')()),
            ('From_date', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('To_date', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('Status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('leave_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'leaveform', ['Leave_status'])

        # Adding model 'new_user'
        db.create_table(u'leaveform_new_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('available_leave', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('auth', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('dob', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mail', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('mob', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal(u'leaveform', ['new_user'])


    def backwards(self, orm):
        # Deleting model 'user_leave'
        db.delete_table(u'leaveform_user_leave')

        # Deleting model 'Leave_status'
        db.delete_table(u'leaveform_leave_status')

        # Deleting model 'new_user'
        db.delete_table(u'leaveform_new_user')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leaveform.leave_status': {
            'From_date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'LeaveID': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'Leave_status'},
            'Status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'To_date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'leaveform.new_user': {
            'Meta': {'object_name': 'new_user'},
            'auth': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'available_leave': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dob': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'mob': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'leaveform.user_leave': {
            'From_date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Meta': {'object_name': 'user_leave'},
            'Remarks': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Timeoff': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'To_date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'WDay_apply': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['leaveform']