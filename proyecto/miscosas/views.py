from datetime import datetime

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from .forms import RegistrationForm, PagUsForm
from django.contrib.auth.models import User

from .models import PagUsuario, tamano, estilous

# Create your views here.

def index(request):
    #lista = Concierto.objects.all()
    #form = AuthenticationForm(request)
    #<!--"{% url 'login_view' recurso=recurso_us %}"> -->
    context = {'user': request.user, 'recurso_us': '/'}
    print(request.user.is_authenticated)
    return render(request, 'miscosas/index.html', context)


def logout_view(request):
    logout(request)
    recurso_us = request.GET['recurso']
    return redirect(recurso_us)


def login_view(request):
    if request.method == "POST":
        recurso_us = request.GET['recurso']
        action = request.POST['action']
        request.POST =  request.POST.copy()
        if action=="Registrar":
            request.POST['password1'] = request.POST['password']
            form = RegistrationForm(data=request.POST)
        else:
            # Añadimos los datos recibidos al formulario
            form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            if action=="Registrar":
                user = form.save()
            else:
                # Recuperamos las credenciales validadas
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Verificamos las credenciales del usuario
                user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña, o se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)

    return redirect(recurso_us)


def cuenta_usuario(request, us):
    try:
        usuario = User.Objects.get(us)
        if request.method == 'GET':
            form = PagUsForm()
            #request.POST, instance=contenido
            context = {'form': form, 'usario': us}
            return render(request, 'miscosas/usuario.html', context)
        elif request.methon == 'POST':
            form = PagUsForm(request.POST)
            if form.is_valid():
                pagUsEstilo = PagUsuario(tamletra=form.cleaned_data['tamano'],
                                        estilo=form.cleaned_data['estilo'],
                                        usuario = usuario)
                pagUsEstilo.save()
                return redirect('usuario', us=usuario)
    except User.ObjectDoesNotExist:
        return redirect('/')
