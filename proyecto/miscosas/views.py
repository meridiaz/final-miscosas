from datetime import datetime

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

#from .forms import GrupoForm, MusicoForm, ConciertoForm
#from .models import Grupo, Musico, Concierto

# Create your views here.

def index(request):
    #lista = Concierto.objects.all()
    form = AuthenticationForm(request)
    context = {'form': form, 'user': request.user}
    print(request.user.is_authenticated)
    return render(request, 'miscosas/index.html', context)


def logout_view(request):
    logout(request)
    return redirect("/")
