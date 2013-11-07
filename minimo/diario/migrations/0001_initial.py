# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Progetto'
        db.create_table(u'diario_progetto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'diario', ['Progetto'])

        # Adding model 'Attivita'
        db.create_table(u'diario_attivita', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cliente.Cliente'])),
            ('descrizione', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'diario', ['Attivita'])

        # Adding model 'Riga'
        db.create_table(u'diario_riga', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('attivita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diario.Attivita'])),
            ('descrizione', self.gf('django.db.models.fields.TextField')()),
            ('inizio', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('fine', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('quantita', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True, blank=True)),
            ('prezzo', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True, blank=True)),
            ('imposta', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('fatturata', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_creazione', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'diario', ['Riga'])


    def backwards(self, orm):
        # Deleting model 'Progetto'
        db.delete_table(u'diario_progetto')

        # Deleting model 'Attivita'
        db.delete_table(u'diario_attivita')

        # Deleting model 'Riga'
        db.delete_table(u'diario_riga')


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
        u'cliente.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'cap': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'citta': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'cod_fiscale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'p_iva': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'provincia': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ragione_sociale': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cliente_user'", 'to': u"orm['auth.User']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'diario.attivita': {
            'Meta': {'object_name': 'Attivita'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cliente.Cliente']"}),
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'diario.progetto': {
            'Meta': {'object_name': 'Progetto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'diario.riga': {
            'Meta': {'object_name': 'Riga'},
            'attivita': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['diario.Attivita']"}),
            'data_creazione': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            'fatturata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fine': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imposta': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'inizio': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'prezzo': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'quantita': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['diario']