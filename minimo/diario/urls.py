from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('minimo.diario.views',
    #righe
    #(r'^attivita/riga/$', 'righe'),
    (r'^attivita/riga/nuova/$', 'nuovarigattivita'),
    (r'^attivita/riga/nuova/(?P<id_a>\w+)/$', 'nrigattivita'),
    (r'^attivita/riga/modifica/(?P<id_a>\w+)/$', 'mrigattivita'),
    (r'^attivita/riga/elimina/(?P<a_id>\w+)/$', 'erigattivita'),
    #attivita

    #(r'^attivita/esporta/(?P<attivita>\w+)/$', 'esportaattivita'),
    (r'^attivita/nuova/$', 'nuovattivita'),
    (r'^attivita/nuovacliente/(?P<id_c>\w+)/$', 'nuovattivitacliente'),
    (r'^attivita/elimina/(?P<a_id>\w+)/$', 'eattivita'),
    (r'^attivita/eliminacliente/(?P<a_id>\w+)/$', 'eattivitacliente'),
    (r'^attivita/lista/$', 'listarighe'),
    (r'^attivita/listacliente/(?P<id_c>\w+)/$', 'listaattivitacliente'),
    (r'^attivita/dettaglioattivita/(?P<id_c>\w+)/$', 'dettaglioattivita'),
    (r'^attivita/fattura/(?P<id_a>\w+)/$', 'fattura_attivita'),
    )
