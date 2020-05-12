from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PagUsuario, Comentario

class RegistrationForm(UserCreationForm):
    password2 = None

class PagUsForm(forms.Form):
    CHOICES = [('pequena', 'Pequeño'), ('mediana', 'Mediana'), ('grande', 'Grande')]
    tamano = forms.ChoiceField(widget = forms.Select, choices = CHOICES)
    CHOICES2 = [('oscuro', 'Oscuro'), ('ligero', 'Ligero')]
    estilo = forms.ChoiceField(widget = forms.Select, choices = CHOICES2)

class AlimForm(forms.Form):
    CHOICES = [('reddit', 'Reddit'), ('yt', 'Youtube')]
    tipo_alimentador = forms.ChoiceField(widget = forms.Select, choices = CHOICES)
    identificador_o_nombre = forms.CharField() #este sera el nombre en el modelo


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('texto', )
