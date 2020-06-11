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
from django.utils.translation import gettext_lazy as _

#from urllib import request
import urllib.request

from .forms import RegistrationForm, PagUsForm, AlimForm, ComentarioForm, UploadImageForm
from .models import PagUsuario, tamano, estilous, Alimentador, Item, Comentario, Like
from .ytalim import YTChannel
from .redalim import SubReddit
from .fmalim import FMArtista
from .crear_docs import XML_create, JSON_create

# Create your views here.

path_foto_votar = "/static/miscosas/"
archivo_like={1:  ['like_sel.jpg', 'dis.jpg'],
            0:  ['like.jpg', 'dis.jpg'],
            -1:  ['like.jpg', 'dis_sel.jpg'],
}

def devolver_404(request, url, context):
    resp = render(request, url, context)
    resp.status_code = 404
    return resp

def info(request):
    return render(request, 'miscosas/info.html', {'nav_info': "active", 'recurso_us': "/informacion"})

def procesar_docs_users(request, lista):
    doc = request.GET['format']
    if doc == "xml":
        return HttpResponse(XML_create().xml_users(lista)
                            , content_type="text/xml")
    elif doc == "json":
        return HttpResponse(JSON_create().json_users(lista)
                            , content_type="application/json")
    else:
        context = {'error': _("No se soporta ese tipo de documento"), 'recurso_us': '/usuarios'}
        return devolver_404(request, 'miscosas/pag_error.html', context)

def usuarios(request):
    lista = PagUsuario.objects.all()
    if 'format' in request.GET.keys():
        return procesar_docs_users(request, lista)
    context = {'lista': lista, 'recurso_us': "/usuarios", 'nav_users': 'active'}
    return render(request, 'miscosas/usuarios.html', context)

def procesar_docs_alims(request, lista):
    doc = request.GET['format']
    if doc == "xml":
        return HttpResponse(XML_create().xml_alims(lista)
                            , content_type="text/xml")
    elif doc == "json":
        return HttpResponse(JSON_create().json_alims(lista)
                            , content_type="application/json")
    else:
        context = {'error': _("No se soporta ese tipo de documento"), 'recurso_us': '/alimentadores'}
        return devolver_404(request, 'miscosas/pag_error.html', context)

def alimentadores(request):
    lista = Alimentador.objects.all()
    if 'format' in request.GET.keys():
        return procesar_docs_alims(request, lista)
    context = {'lista': lista, 'recurso_us': "/alimentadores", 'nav_alims': 'active'}
    return render(request, 'miscosas/alimentadores.html', context)

def nombre_persona(user):
    #funcion que devuelve el nombre del usuario si esta registrado
    #o el codigo de la cookie en caso de no estarlo
    if user.is_authenticated:
        return user
    else:
        return ""

def guardar_us_enalim(user, id):
    #funcion que guarda el usuario al que le ha dado a elegir al alimentador
    alim = Alimentador.objects.get(id=id)
    if nombre_persona(user) != "":
        alim.usuario.add(nombre_persona(user))

def leer_xml(tipo, nombre):
    if tipo == "yt":
        id = YTChannel(nombre).id_canal()
    elif tipo == "reddit":
        id = SubReddit(nombre).id_reddit()
    elif tipo == "fm":
        id = FMArtista(nombre).id_artista()
    return id

def gestionar_alims(request):
    form = AlimForm(request.POST)
    if not form.is_valid():
         return -1

    tipo = form.cleaned_data['tipo_alimentador']
    nombre = form.cleaned_data['identificador_o_nombre']

    return leer_xml(tipo, nombre)
#if 'enviar' in request.GET:
    #return redirect('/alimentador/'+str(alim.id))
#un solo boton
#elegio = False --> elegido= True, #añado a la lista de usuarios, actualizar datos
#elegido = True--> elegido = False,
def procesar_docs_alim(request, alim):
    doc = request.GET['format']
    if doc == "xml":
        return HttpResponse(XML_create().xml_alim(alim)
                            , content_type="text/xml")
    elif doc == "json":
        return HttpResponse(JSON_create().json_alim(alim)
                            , content_type="application/json")
    else:
        context = {'error': _("No se soporta ese tipo de documento"), 'recurso_us': '/alimentador'+str(alim.id)}
        return devolver_404(request, 'miscosas/pag_error.html', context)

def alimentador(request, id=-1):
    if request.method == "POST":
        id = gestionar_alims(request)
        if id == -1:
            context = {'error': _("No se ha podido encontrar la URL para ese alimentador"),
                        'recurso_us': '/'}
            return devolver_404(request, 'miscosas/pag_error.html', context)
        else:
            guardar_us_enalim(request.user, id)
        return redirect('/alimentador/'+str(id))

    try:
        alim = Alimentador.objects.get(id=id)
    except ObjectDoesNotExist:
        context = {'error': _("El alimentador pedido no se encuentra"),
                'recurso_us': '/'}
        return devolver_404(request, 'miscosas/pag_error.html', context)

    if 'format' in request.GET.keys():
        return procesar_docs_alim(request, alim)

    context = {'alim': alim, 'recurso_us': '/alimentador/'+str(alim.id)}
    return render(request, 'miscosas/alimentador.html', context)

def gestionar_voto(action, request, item):
    if action == "like":
        num =  1
    elif action == "dislike":
        num = -1
    try:
        voto = Like.objects.get(usuario=request.user, item=item)
        if voto.boton != num:
            voto.boton = num
            voto.fecha = datetime.now()
    except ObjectDoesNotExist:
        voto = Like(usuario=request.user, item=item, boton=num)
    voto.save()

def gestionar_comen(request, item):
    form = ComentarioForm(request.POST, request.FILES)
    if form.is_valid():
        comen = Comentario(texto= form.cleaned_data['texto'], usuario=request.user,
                            item=item, foto=form.cleaned_data['foto'])
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

def procesar_docs_item(request, item):
    doc = request.GET['format']
    if doc == "xml":
        return HttpResponse(XML_create().xml_item(item)
                            , content_type="text/xml")
    elif doc == "json":
        return HttpResponse(JSON_create().json_item(item)
                            , content_type="application/json")
    else:
        context = {'error': _("No se soporta ese tipo de documento"), 'recurso_us': '/alimentador'+str(item.id)}
        return devolver_404(request, 'miscosas/pag_error.html', context)

def mostrar_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist:
        context = {"error": _("El item pedido no existe"), 'recurso_us': '/'}
        return devolver_404(request, 'miscosas/pag_error.html', context)

    if request.method == "POST":
        action = request.POST['action']
        if action=="comentario":
            gestionar_comen(request, item)
        elif action=="like" or action =="dislike":
            gestionar_voto(action, request, item)

    if 'format' in request.GET.keys():
        return procesar_docs_item(request, item)

    boton_like, boton_dislike = iluminar_voto(request, item)
    lista = Comentario.objects.filter(item=item)
    context = {'item': item, 'recurso_us': '/item/'+str(item.id),
                'lista': lista, 'user': request.user, 'form': ComentarioForm(),
                'boton_like': boton_like, 'boton_dislike': boton_dislike}
    return render(request, 'miscosas/item.html', context)

def add_boton_voto(top, request):
    for it in top:
        it.boton_like, it.boton_dislike = iluminar_voto(request, it)

def procesar_post_index(request):
    action = request.POST['action']
    if action == "elegir":
        alim = Alimentador.objects.get(id=request.POST['alim'])
        id = leer_xml(alim.tipo, alim.id_canal)
        alim.elegido = True
        alim.save()
        if id != -1:
            guardar_us_enalim(request.user, id)
        return redirect('/alimentador/'+str(alim.id))
    elif action == "eliminar":
        alim = Alimentador.objects.get(id=request.POST['alim'])
        alim.elegido = False
        alim.save()
        if 'enviar' in request.GET:
            return redirect('/alimentador/'+str(alim.id))
    elif action == "like" or action == "dislike":
        item = Item.objects.get(id=request.POST['item'])
        gestionar_voto(action, request, item)

    return redirect('/')

def procesar_docs(request, top10, top5, lista):
    doc = request.GET['format']
    if doc == "xml":
        return HttpResponse(XML_create().xml_index(top10, top5, lista)
                            , content_type="text/xml")
    elif doc == "json":
        return HttpResponse(JSON_create().json_index(top10, top5, lista)
                            , content_type="application/json")
    else:
        context = {'error': _("No se soporta ese tipo de documento"), 'recurso_us': '/'}
        return devolver_404(request, 'miscosas/pag_error.html', context)

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

    lista = Alimentador.objects.all().filter(elegido=True)
    if 'format' in request.GET.keys():
        return procesar_docs(request, top10, top5, lista)

    #print(User.objects.get(username="daniel").alimentador_set.all())

    context = {'user': request.user, 'recurso_us': '/', 'form': AlimForm(),
                'nav_index': 'active', 'top10': top10, 'top5': top5, 'alims': lista}
    return render(request, 'miscosas/index.html', context)


def logout_view(request):
    logout(request)
    if 'recurso' in request.GET:
        recurso_us = request.GET['recurso']
    else:
        recurso_us = '/'
    return redirect(recurso_us)


def login_view(request):
    if 'recurso' in request.GET:
        recurso_us = request.GET['recurso']
    else:
        recurso_us = '/'

    if request.method == "POST":
        action = request.POST['action']
        request.POST =  request.POST.copy()
        if action=="Registrar":
            request.POST['password1'] = request.POST['password']
            form = RegistrationForm(data=request.POST)
            msg = _("Informacion de autenticacion no valida, o el usuario ya tiene cuenta")
        else:
            form = AuthenticationForm(data=request.POST)
            msg = _("El usuario o la contraseña no son correctos")
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
            context = {'recurso_us': recurso_us, 'error': msg, 'recurso_us': '/'}
            return devolver_404(request, 'miscosas/pag_error.html', context)

    return redirect(recurso_us)

def procesar_post_pagus(request):
    action = request.POST['action']
    pagUsEstilo = PagUsuario.objects.get(usuario=request.user)

    if action == "foto":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            pagUsEstilo.foto = form.cleaned_data['foto']
    elif action == "formato":
        form = PagUsForm(request.POST)
        if form.is_valid():
            pagUsEstilo.tamLetra = form.cleaned_data['tamano']
            pagUsEstilo.estilo = form.cleaned_data['estilo']
    pagUsEstilo.save()

def procesar_docs_us(request, pag_us):
    doc = request.GET['format']
    if doc == "xml":
        return HttpResponse(XML_create().xml_us(pag_us)
                            , content_type="text/xml")
    elif doc == "json":
        return HttpResponse(JSON_create().json_us(pag_us)
                            , content_type="application/json")
    else:
        context = {'error': _("No se soporta ese tipo de documento"), 'recurso_us': '/'+pag_us.usuario.username}
        return devolver_404(request, 'miscosas/pag_error.html', context)

def cuenta_usuario(request, us):
    if request.method == 'POST':
        procesar_post_pagus(request)

    try:
        usuario = User.objects.get(username=us)
        pagUsEstilo = PagUsuario.objects.get(usuario=usuario)
    except ObjectDoesNotExist:
        context = {'error': _("El usuario pedido no existe"), 'recurso_us': '/'}
        return devolver_404(request, 'miscosas/pag_error.html', context)

    if 'format' in request.GET.keys():
        return procesar_docs_us(request, pagUsEstilo)

    lista_vot = Item.objects.filter(like__usuario=usuario)
    lista_comen = Item.objects.filter(comentario__usuario=usuario).distinct()
    context = {'form_estilo': PagUsForm(), 'usuario': usuario, 'recurso_us': '/usuario/'+us,
                'pag_us': pagUsEstilo, 'form_foto': UploadImageForm(),
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
    tam.update(estilo)
    context = Context(tam)
    return HttpResponse(template.render(tam), content_type="text/css")
