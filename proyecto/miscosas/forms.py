from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PagUsuario

class RegistrationForm(UserCreationForm):
    password2 = None

class PagUsForm(forms.Form):
    CHOICES = [('pequena', 'Pequeño'), ('mediana', 'Mediana'), ('grande', 'Grande')]
    tamano = forms.ChoiceField(widget = forms.Select, choices = CHOICES)
    CHOICES2 = [('oscuro', 'Oscuro'), ('ligero', 'Ligero')]
    estilo = forms.ChoiceField(widget = forms.Select, choices = CHOICES2)
