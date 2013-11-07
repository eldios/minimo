from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *


from minimo.diario.models import Attivita, Riga as RigaAttivita
from minimo.documento.models import Documento, Ritenuta
from minimo.cliente.models import *

class AttivitaForm(forms.ModelForm):
    
    class Meta:
        model = Attivita
        exclude = ('cliente', )
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('descrizione'),
            Field('stato'),
            FormActions(
                Submit('save', 'Aggiungi', css_class="btn-primary")
            )
        )
        super( AttivitaForm, self).__init__(*args, **kwargs)


class AttivitaRigaForm(forms.ModelForm):
    
    class Meta:
        model = RigaAttivita
        exclude = ('attivita', 'fatturata', 'imposta', )
        
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('tipo'),
            Field('descrizione'),
            Field('inizio'),
            Field('fine'),
            Field('quantita'),
            Field('prezzo'),
            FormActions(
                Submit('save', 'Aggiungi', css_class="btn-primary")
            )
        )
        super( AttivitaRigaForm, self).__init__(*args, **kwargs)
 


def get_ritenute():
    output = [('---', '---')]
    for ritenuta in Ritenuta.objects.all():
        output.append((ritenuta.nome, ritenuta.nome))
    return output

class FatturaAttivitaForm(forms.ModelForm):
    stato = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    
    class Meta:
        model = Documento
    
        
    def __init__(self, *args, **kwargs):
        
        super(FatturaAttivitaForm, self).__init__(*args, **kwargs)
  
        self.fields['descrizione_ritenuta'] = forms.ChoiceField(choices=get_ritenute(), required=False )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('tipo'),
                    AppendedText('data', '<i class="icon-calendar"></i>'),
                    Field('stato'),
                    Field('template'),
                    Field('data_consegna'),
                    Field('sconto'),
                css_class="span6"),
                Div(
                    #Field('imposte'),
                    Field('descrizione_ritenuta'),
                    Field('bollo'),
                    Field('valore_bollo'),
                    Field('pagamento'),
                    Field('note'),
                css_class="span6"),
            css_class="row-fluid"),
            FormActions(
                Submit('save', 'Salva', css_class="btn-primary")
            )
        )