from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PagUsuario, Comentario
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
    password2 = None

class PagUsForm(forms.Form):
    CHOICES = [('pequena', _('Pequeño')), ('mediana', _('Mediana')), ('grande', _('Grande'))]
    tamano = forms.ChoiceField(widget = forms.Select, choices = CHOICES, label=_('Tamaño'))
    CHOICES2 = [('oscuro', _('Oscuro')), ('ligero', _('Ligero'))]
    estilo = forms.ChoiceField(widget = forms.Select, choices = CHOICES2, label=_('Estilo'))

class AlimForm(forms.Form):
    CHOICES = [('reddit', 'Reddit'), ('yt', 'Youtube'), ('fm', 'LastFm')]
    tipo_alimentador = forms.ChoiceField(widget = forms.Select, choices = CHOICES, label=_('Tipo de alimentador'))
    identificador_o_nombre = forms.CharField(label=_('Identificador o nombre')) #este sera el nombre en el modelo


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('texto', 'foto')
        labels = {
                    'texto': _('Texto'),
                    'foto': _('Foto')
        }

class UploadImageForm(forms.ModelForm):

    class Meta:
        model = PagUsuario
        fields = ['foto']
        labels = {'foto': _('Foto') }
