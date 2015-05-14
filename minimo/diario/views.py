# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.core.urlresolvers import reverse


import cStringIO as StringIO
from django.template.loader import render_to_string
import pdb
import os
from django.conf import settings
from django.db.models import Sum
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import csv, codecs
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core import serializers
from django.utils import simplejson

from minimo.diario.models import Attivita, Riga as RigaAttivita
from minimo.documento.models import Documento, Riga as RigaDocumento
from minimo.documento.utils import *
from minimo.diario.forms import *
from minimo.utils import *

@login_required
def listaattivitacliente(request, id_c):
    azione = 'lista'
    cliente=Cliente.objects.filter(id=id_c)
    attivita = Attivita.objects.filter(cliente=cliente)

    return render_to_response( 'diario/lista_attivita.html', {'request':request, 'attivita': attivita}, RequestContext(request))

@login_required
def listarighe(request):
    azione = 'lista'
    righe_da_fatt = RigaAttivita.objects.filter(fatturata=False).exclude(cliente=None)[:100]
    righe_fatt = RigaAttivita.objects.filter(fatturata=True).exclude(cliente=None)[:100]
    formRiga = RigaForm()
    return render_to_response( 'diario/lista_righe.html', {'request':request, 'righe_da_fatt': righe_da_fatt, 'righe_fatt':righe_fatt, 'form': formRiga,}, RequestContext(request))

@login_required
def listaattivitacliente(request, id_c):
    azione = 'lista'
    cliente=Cliente.objects.filter(id=id_c)
    attivita = RigaAttivita.objects.filter(cliente=cliente, fatturata=False)

    return render_to_response( 'diario/lista_attivita.html', {'request':request, 'attivita': attivita}, RequestContext(request))

@login_required
def dettaglioattivita(request, id_c):
    azione = 'lista'
    attivita = Attivita.objects.get(id=id_c)
    righe = RigaAttivita.objects.filter(attivita=attivita)
    formRiga = AttivitaRigaForm()
    return render_to_response( 'diario/dettaglio_attivita.html', {'request':request, 'righe': righe, 'form': formRiga, 'attivita': attivita}, RequestContext(request))

@login_required
def nuovattivitacliente(request, id_c):
    azione = 'nuovo'
    cliente = Cliente.objects.get(id=id_c)
    if request.method == 'POST':
        form = AttivitaClienteForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.cliente = cliente
            a.save()
            return HttpResponseRedirect(reverse('minimo.diario.views.dettaglioattivita', args=(str(a.id),),))
    else:
        form = AttivitaClienteForm()
    return render_to_response('diario/form_attivita.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))


@login_required
def nuovattivita(request):
    azione = 'nuovo'
    if request.method == 'POST':
        form = AttivitaForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.cliente = None
            a.save()
            return HttpResponseRedirect(reverse('minimo.diario.views.listarighe',))
    else:
        form = AttivitaForm()
    return render_to_response('diario/form_attivita.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

@login_required
def nuovarigattivita(request):
    azione = 'nuovo'

    if request.method == 'POST':
        form = RigaForm(request.POST)
        form.helper.form_action = reverse('minimo.diario.views.nuovarigattivita',)
        if form.is_valid():
            r = form.save(commit=False)
            r.save()
            return HttpResponseRedirect(reverse('minimo.diario.views.listarighe', ))
    else:
        form = RigaForm()
        form.helper.form_action = reverse('minimo.diario.views.nuovarigattivita', args=(str(attivita.id),),)
    return render_to_response('diario/form_attivita.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))


@login_required
def nrigattivita(request, id_a):
    azione = 'nuovo'
    attivita = Attivita.objects.get(id=id_a)
    if request.method == 'POST':
        form = AttivitaRigaForm(request.POST)
        form.helper.form_action = reverse('minimo.diario.views.nrigattivita', args=(str(attivita.id),),)
        if form.is_valid():
            r = form.save(commit=False)
            r.attivita = attivita
            r.save()
            return HttpResponseRedirect(reverse('minimo.diario.views.dettaglioattivita', args=(str(attivita.id),)))
    else:
        form = AttivitaRigaForm()
        form.helper.form_action = reverse('minimo.diario.views.nrigattivita', args=(str(attivita.id),),)
    return render_to_response('diario/form_attivita.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))


@login_required
def fattura_attivita(request, id_a):
    cliente = Cliente.objects.get(id=id_a)
    righe = RigaAttivita.objects.filter(cliente=cliente, fatturata=False)
    azione = 'Nuovo'
    if request.method == 'POST':
        form = FatturaAttivitaForm(request.POST)
        form.helper.form_action = reverse('minimo.diario.views.fattura_attivita', args=(str(cliente.id),),)
        if form.is_valid():
            cliente = cliente
            f=form.save(commit=False)
            try:
                f.descrizione_ritenuta = form.cleaned_data['descrizione_ritenuta']
                f.ritenuta = Ritenuta.objects.get(nome=form.cleaned_data['descrizione_ritenuta']).aliquota
            except Exception:
                pass
            f.user=request.user
            f.save()
            for r in righe:
                riga = RigaDocumento(documento=f)
                riga.descrizione = r.descrizione
                riga.quantita = r.quantita
                riga.importo_unitario = r.prezzo
                if f.tipo == 'FA':
                    riga.imposta = 20.0
                riga.save()
                r.fatturata = True
                r.save()

            copia_dati_fiscali(f, cliente)
            #attivita.stato = True
            #attivita.save()
            return HttpResponseRedirect(reverse('minimo.documento.views.dettagli_documento', args=(str(f.id),),))
    else:
        form = FatturaAttivitaForm()
        form.helper.form_action = reverse('minimo.diario.views.fattura_attivita', args=(str(cliente.id),),)
    return render_to_response('documento/form_documento.html',{'request':request,'form': form,'azione': azione,}, RequestContext(request))


@login_required
def mrigattivita(request, id_a):
    azione = 'modifica'
    riga = RigaAttivita.objects.get(id=id_a)
    attivita = riga.attivita
    if request.method == 'POST':
        form = RigaForm(request.POST, instance=riga)
        form.helper.form_action = reverse('minimo.diario.views.mrigattivita', args=(str(riga.id),),)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse('minimo.diario.views.listarighe',))
    else:
        print 'no post'
        form = RigaForm(instance=riga)
        form.helper.form_action = reverse('minimo.diario.views.mrigattivita', args=(str(riga.id),),)
    return render_to_response('diario/form_attivita.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))


@login_required
def erigattivita(request,a_id):
    riga = RigaAttivita.objects.get(id=a_id)
    a = riga.attivita.id
    riga.delete()
    return HttpResponseRedirect(reverse('minimo.diario.views.listarighe',))

@login_required
def eattivitacliente(request,a_id):
    a = Attivita.objects.get(id=a_id)
    c = a.cliente
    righe = RigaAttivita.objects.filter(attivita=a)
    for r in righe:
        r.delete()
    a.delete()
    return HttpResponseRedirect(reverse('minimo.diario.views.listaattivitacliente', args=(str(c.id,),)))

@login_required
def eattivita(request,a_id):
    a= Attivita.objects.get(id=a_id)
    righe = RigaAttivita.objects.filter(attivita=a)
    for r in righe:
        r.delete()
    a.delete()
    return HttpResponseRedirect(reverse('minimo.diario.views.listaattivita'))
