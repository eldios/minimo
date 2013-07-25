# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Fattura.template'
        db.alter_column(u'fattura_fattura', 'template_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['fattura.TemplateFattura']))

        # Changing field 'Fattura.cliente'
        db.alter_column(u'fattura_fattura', 'cliente_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['fattura.Cliente']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Fattura.template'
        raise RuntimeError("Cannot reverse this migration. 'Fattura.template' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Fattura.cliente'
        raise RuntimeError("Cannot reverse this migration. 'Fattura.cliente' and its values cannot be restored.")

    models = {
        u'fattura.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'cod_fiscale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'p_iva': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ragione_sociale': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'telefono': ('django.db.models.fields.IntegerField', [], {})
        },
        u'fattura.fattura': {
            'Meta': {'ordering': "['data']", 'object_name': 'Fattura'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fattura_cliente'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['fattura.Cliente']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stato': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fattura_template'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['fattura.TemplateFattura']"})
        },
        u'fattura.fatturaminimo': {
            'Meta': {'ordering': "['data']", 'object_name': 'FatturaMinimo', '_ormbases': [u'fattura.Fattura']},
            'bollo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'fattura_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fattura.Fattura']", 'unique': 'True', 'primary_key': 'True'}),
            'valore_bollo': ('django.db.models.fields.IntegerField', [], {})
        },
        u'fattura.fatturastandard': {
            'IVA': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'Meta': {'ordering': "['data']", 'object_name': 'FatturaStandard', '_ormbases': [u'fattura.Fattura']},
            u'fattura_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fattura.Fattura']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'fattura.prestazione': {
            'Meta': {'object_name': 'Prestazione'},
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            'fattura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prestazione_fattura'", 'to': u"orm['fattura.Fattura']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importo': ('django.db.models.fields.FloatField', [], {})
        },
        u'fattura.templatefattura': {
            'Meta': {'object_name': 'TemplateFattura'},
            'descrizione': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fattura']