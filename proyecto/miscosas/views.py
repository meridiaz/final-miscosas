from django.shortcuts import render
from datetime import datetime

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader

#from .forms import GrupoForm, MusicoForm, ConciertoForm
#from .models import Grupo, Musico, Concierto

# Create your views here.

def index(request):
    #lista = Concierto.objects.all()
    #form = ConciertoForm()
    context = {}#{'objects_list': lista, 'form': form, 'type': "conciertos"}
    return render(request, 'miscosas/index.html', context)
