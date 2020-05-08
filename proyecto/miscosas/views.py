from datetime import datetime

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader
from django.template.loader import get_template
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context

from urllib import request

from .forms import RegistrationForm, PagUsForm
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
    print(recurso_us)
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
                pagUs = PagUsuario(usuario = user)
                pagUs.save()
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
        usuario = User.objects.get(username=us)
        pagUsEstilo = PagUsuario.objects.get(usuario=usuario)
        if request.method == 'GET':
            form = PagUsForm()
            context = {'form': form, 'usuario': us, 'recurso_us': '/usuario/'+us,
                        'foto': pagUsEstilo.foto}
            return render(request, 'miscosas/usuario.html', context)
        elif request.method == 'POST':
            action = request.POST['action']
            if action=="foto":
                pagUsEstilo.foto = request.POST['url']
                pagUsEstilo.save()
                return redirect('/usuario/'+us)
            elif action=="formato":
                form = PagUsForm(request.POST)

                if form.is_valid():

                    pagUsEstilo.tamLetra = form.cleaned_data['tamano']
                    pagUsEstilo.estilo = form.cleaned_data['estilo']
                    pagUsEstilo.save()
                    return redirect('/usuario/'+us)
    except ObjectDoesNotExist:
        return redirect('/')


def procesar_css(request):
    print("me han pedido el cass")
    template = get_template("miscosas/micss.css")
    print("me piden el css")
    try:
        username = request.user.get_username()
        pag_usuario = PagUsuario.objects.get(usuario__username=username)
        estilo = estilous[pag_usuario.estilo]
        tam = tamano[pag_usuario.tamLetra]
    except ObjectDoesNotExist:
        estilo = estilous['ligero']
        tam = tamano['mediana']
    dic1= {'tam': tam}
    dic1.update(estilo)
    context = Context(dic1)
    return HttpResponse(template.render(dic1), content_type="text/css")
