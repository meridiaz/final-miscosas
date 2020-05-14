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

from django.db.models import Sum, Count, Q, Case, When, Value
from django.db.models.functions import Coalesce

from urllib import request

from .forms import RegistrationForm, PagUsForm, AlimForm, ComentarioForm, UploadImageForm
from .models import PagUsuario, tamano, estilous, Alimentador, Item, Comentario, Like
from .ytalim import YTChannel
from .redalim import SubReddit

# Create your views here.

path_foto_votar = "/static/miscosas/"
archivo_like={1:  ['like_sel.jpg', 'dis.jpg'],
            0:  ['like.jpg', 'dis.jpg'],
            -1:  ['like.jpg', 'dis_sel.jpg'],
}

def usuarios(request):
    lista = PagUsuario.objects.all()
    context = {'lista': lista, 'recurso_us': "/usuarios", 'nav_users': 'active'}
    return render(request, 'miscosas/usuarios.html', context)

def alimentadores(request):
    lista = Alimentador.objects.all()
    context = {'lista': lista, 'recurso_us': "/alimentadores", 'nav_alims': 'active'}
    return render(request, 'miscosas/alimentadores.html', context)

def leer_xml(tipo, nombre):
    print("en leer xml")
    if tipo == "yt":
        id = YTChannel(nombre).id_canal()
        print(id)
    elif tipo == "reddit":
        id = SubReddit(nombre).id_canal()

    return id

def gestionar_alims(request):
    form = AlimForm(request.POST)
    if not form.is_valid():
         print("hay un error")
         return -1
    else:
        print("no hay error")
    tipo = form.cleaned_data['tipo_alimentador']
    nombre = form.cleaned_data['identificador_o_nombre']
    print(nombre)

    return leer_xml(tipo, nombre)

def alimentador(request, id=-1):
    print("en alimentador")
    if request.method == "POST":
        id = gestionar_alims(request)
        return redirect('/alimentador/'+str(id))
    elif request.method == "GET":
        try:
            alim = Alimentador.objects.get(id=id)
        except ObjectDoesNotExist:
            return render(request, 'miscosas/alimentador.html', {'error': "El alimentador pedido no existe"})

        context = {'alim': alim, "error": "", 'recurso_us': '/alimentador/'+str(alim.id)}
        return render(request, 'miscosas/alimentador.html', context)

def gestionar_voto(action, request, item):
    if action == "like":
        num =  1
    elif action == "dislike":
        num = -1
    try:
        voto = Like.objects.get(usuario=request.user, item=item)
        voto.boton = num
    except ObjectDoesNotExist:
        voto = Like(usuario=request.user, item=item, boton=num)
    voto.save()

def gestionar_comen(request, item):
    form = ComentarioForm(request.POST)
    #print(form)
    if form.is_valid():
        comen = Comentario(texto= form.cleaned_data['texto'], usuario=request.user,
                            item=item)
        comen.save()

def iluminar_voto(request, item):
    if request.user.is_authenticated:
        try:
            valor = request.user.like_set.get(item=item).boton
        except ObjectDoesNotExist:
            valor = 0
    else:
        valor = 0

    return path_foto_votar + archivo_like[valor][0], path_foto_votar +archivo_like[valor][1]

def mostrar_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'miscosas/item.html', {"error": "El item pedido no existe"})

    if request.method == "POST":
        action = request.POST['action']
        if action=="comentario":
            gestionar_comen(request, item)
        elif action=="like" or action =="dislike":
            gestionar_voto(action, request, item)

    boton_like, boton_dislike = iluminar_voto(request, item)
    lista = Comentario.objects.filter(item=item)
    context = {'item': item, "error": "", 'recurso_us': '/item/'+str(item.id),
                'lista': lista, 'user': request.user, 'form': ComentarioForm(),
                'boton_like': boton_like, 'boton_dislike': boton_dislike}
    return render(request, 'miscosas/item.html', context)

def add_boton_voto(top, request):
    for it in top:
        it.boton_like, it.boton_dislike = iluminar_voto(request, it)

def procesar_post_index(request):
    action = request.POST['action']
    if action=="elegir":
        alim = Alimentador.objects.get(id=request.POST['alim'])
        id = leer_xml(alim.tipo, alim.id_canal)
        return redirect('/alimentador/'+str(id))
    elif action=="eliminar":
        alim = Alimentador.objects.get(nombre=request.POST['alim'])
        alim.elegido = not alim.elegido
        alim.save()
    elif action=="like" or action =="dislike":
        item = Item.objects.get(titulo=request.POST['item'])
        gestionar_voto(action, request, item)

    return redirect('/')


def index(request):
    #visto en: https://stackoverflow.com/questions/18198977/django-sum-a-field-based-on-foreign-key
    # y en: https://docs.djangoproject.com/en/3.0/topics/db/aggregation/
    #https://martinpeveri.wordpress.com/2018/06/24/la-funcion-coalesce-en-django/
    if request.method == "POST":
        return procesar_post_index(request)

    top10 = Item.objects.annotate(npos=Count('like', filter=Q(like__boton=1)),
                                    nneg= Count('like', filter=Q(like__boton=-1)),
                                    nlikes=Coalesce(Sum('like__boton'), Value(0))).order_by('-nlikes')[0:10]
    top5 = []
    if request.user.is_authenticated:
        add_boton_voto(top10, request)
        items_user = Item.objects.filter(like__usuario = request.user)
        fixed_date = datetime(2000, 1, 1)
        top5 = items_user.annotate(nueva_fecha=
                                    Coalesce('like__fecha', Value(fixed_date))).order_by('-nueva_fecha')[0:5]
        add_boton_voto(top5, request)

    lista = Alimentador.objects.all()
    context = {'user': request.user, 'recurso_us': '/', 'form': AlimForm(),
                'nav_index': 'active', 'top10': top10, 'top5': top5, 'alims': lista}
    return render(request, 'miscosas/index.html', context)


def logout_view(request):
    logout(request)
    recurso_us = request.GET['recurso']
    return redirect(recurso_us)


def login_view(request):
    recurso_us = request.GET['recurso']
    if request.method == "POST":
        action = request.POST['action']
        request.POST =  request.POST.copy()
        if action=="Registrar":
            request.POST['password1'] = request.POST['password']
            form = RegistrationForm(data=request.POST)
            msg = "El usuario o la contraseña no son correctos"
        else:
            form = AuthenticationForm(data=request.POST)
            msg = "Informacion de autenticacion no valida, o el usuario ya tiene cuenta"
        if form.is_valid():
            if action=="Registrar":
                user = form.save()
                pagUs = PagUsuario(usuario = user)
                pagUs.save()
            else:
                # Verificamos las credenciales del usuario
                user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
            # Si existe un usuario con ese nombre y contraseña, o se crea correctamente
            if user is not None:
                do_login(request, user)
        else:
            context = {'recurso_us': recurso_us, 'error': msg}
            return render(request, 'miscosas/login_err.html', context)

    return redirect(recurso_us)

def procesar_post_pagus(request):
    action = request.POST['action']
    pagUsEstilo = PagUsuario.objects.get(usuario=request.user)

    if action=="foto":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            pagUsEstilo.foto = form.cleaned_data['foto']
    elif action=="formato":
        form = PagUsForm(request.POST)
        if form.is_valid():
            pagUsEstilo.tamLetra = form.cleaned_data['tamano']
            pagUsEstilo.estilo = form.cleaned_data['estilo']
    pagUsEstilo.save()

def cuenta_usuario(request, us):
    if request.method == 'POST':
        procesar_post_pagus(request)

    try:
        usuario = User.objects.get(username=us)
        pagUsEstilo = PagUsuario.objects.get(usuario=usuario)
    except ObjectDoesNotExist:
        return render(request, 'miscosas/usuario.html', {'error': "El usuario pedido no existe"})

    lista_vot = Item.objects.filter(like__usuario = usuario)
    lista_comen = Item.objects.filter(comentario__usuario = usuario)
    context = {'form_estilo': PagUsForm(), 'usuario': usuario, 'recurso_us': '/usuario/'+us,
                'pag_us': pagUsEstilo, 'error': "", 'form_foto': UploadImageForm(),
                'us_log': request.user, 'lista_vot': lista_vot, 'lista_comen': lista_comen}
    return render(request, 'miscosas/usuario.html', context)


def procesar_css(request):
    template = get_template("miscosas/micss.css")
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
