# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Max, Avg
from django.core.urlresolvers import reverse
from minimo.tassa.models import *
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from minimo.cliente.models import *
from minimo.tassa.models import *


class Progetto(models.Model):
    pass

class Attivita(models.Model):
    cliente = models.ForeignKey(Cliente)
    descrizione = models.TextField('Descrizione')
    stato = models.BooleanField('Stato', default=False)
    
    def __unicode__(self):
        return '%s-%s' % (self.cliente, self.descrizione)

    def _get_fatturate(self):
        return Riga.objects.filter(attivita=self, fatturata=False)
        
    def _get_da_fatturare(self):
        return Riga.objects.filter(attivita=self, fatturata=True)
    
    
TIPO_RIGA = (
    ('MO', 'Manodopera'),
    ('MA', 'Materiale')
)

class Riga(models.Model):
    
    tipo = models.CharField('Tipo riga', max_length=5, choices=TIPO_RIGA)
    attivita = models.ForeignKey('Attivita')
    descrizione = models.TextField('Descrizione')
    inizio = models.DateTimeField('Inizio', blank=True, null=True, default=None)
    fine = models.DateTimeField('Fine', blank=True, null=True, default=None)
    quantita = models.FloatField('quantità', default=0.0, blank=True, null=True,)
    prezzo = models.FloatField('Costo unitario', default=0.0, blank=True, null=True)
    imposta = models.IntegerField('Imposta', blank=True, null=True, default=None)
    fatturata = models.BooleanField(default=False)
    data_creazione = models.DateTimeField('Data creazione', auto_now_add=True)
    
    def __unicode__(self):
        return '%s-%s' % (self.tipo, self.descrizione)
    
    def _calcola_intervallo(self):
        if self.fine > self.inizio:
            r = (self.fine - self.inizio).total_seconds()
            return r/3600 #ritorna il tempo in ore
        else:
            return 0
    
    def _totale(self):
        r = self.quantita * self.prezzo
        if self.imposta:
            r = r * (1.00 + self.imposta/100)
        return r
    
    def save(self, *args, **kwargs):          
        if self.inizio and self.fine:
            self.quantita = self._calcola_intervallo()
        super(Riga, self).save(*args, **kwargs)