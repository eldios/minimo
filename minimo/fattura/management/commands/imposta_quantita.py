import logging
import sys, os, socket, re
from django.core.management.base import NoArgsCommand
from django.db.models import Avg, Sum

from minimo.fattura.models import *

from datetime import datetime, timedelta


class Command(NoArgsCommand):
    help = "genera le medie."
    
    def handle_noargs(fattura, **options):
        prestazioni = Prestazione.obejects.all()
        for p in prestazioni:
            p.quantita = 1
            p.save()