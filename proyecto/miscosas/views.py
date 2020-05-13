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

from django.db.models import Sum, Count, Q

from urllib import request

from .forms import RegistrationForm, PagUsForm, AlimForm, ComentarioForm
from .models import PagUsuario, tamano, estilous, Alimentador, Item, Comentario, Like
from .ytalim import YTChannel

# Create your views here.

path_foto_votar = "/static/miscosas/"
archivo_like={1:  ['like_sel.jpg', 'dis.jpg'],
            0:  ['like.jpg', 'dis.jpg'],
            -1:  ['like.jpg', 'dis_sel.jpg'],
}

def usuarios(request):
    lista = User.objects.all()
    context = {'lista': lista, 'recurso_us': "/usuarios", 'nav_users': 'active'}
    return render(request, 'miscosas/usuarios.html', context)

def alimentadores(request):
    lista = Alimentador.objects.all()
    context = {'lista': lista, 'recurso_us': "/alimentadores", 'nav_alims': 'active'}
    return render(request, 'miscosas/alimentadores.html', context)

def alim_yaexiste(id, tipo):
    try:
        alim = Alimentador.objects.get(nombre=id)
        print("el alimentador elegido ya existe")
        return True #ya existe el alimentador
    except ObjectDoesNotExist:
        alim = Alimentador(tipo=tipo, nombre=id)
        return False

def gestionar_alims(request):
    form = AlimForm(request.POST)
    if not form.is_valid():
         print("hay un error")
         return "0"
    else:
        print("no hay error")

    tipo = form.cleaned_data['tipo_alimentador']
    nombre = form.cleaned_data['identificador_o_nombre']
    if not alim_yaexiste(nombre, tipo):
        if tipo == "yt":
            nombre = str(YTChannel(nombre))
        elif tipo == "reddit":
            print("holi2")
    else:
        # actualizar_alim()
        print("el alimentador elegido ya existe2")
    return nombre

def alimentador(request, id=0):
    if request.method == "POST":
        id = gestionar_alims(request)
        return redirect('/alimentador/'+id)
    elif request.method == "GET":
        try:
            alim = Alimentador.objects.get(nombre=id)
        except ObjectDoesNotExist:
            return render(request, 'miscosas/alimentador.html', {'error': "El alimentador pedido no existe"})

        context = {'alim': alim, "error": "", 'recurso_us': '/alimentador/'+alim.nombre}
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

    return archivo_like[valor]

def mostrar_item(request, id):
    try:
        item = Item.objects.get(id_item=id)
        nombre = item.id_item
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
    context = {'item': item, "error": "", 'recurso_us': '/item/'+nombre,
                'lista': lista, 'user': request.user, 'form': ComentarioForm(),
                'boton_like': path_foto_votar+boton_like, 'boton_dislike': path_foto_votar+boton_dislike}
    return render(request, 'miscosas/item.html', context)

def index(request):
    #visto en: https://stackoverflow.com/questions/18198977/django-sum-a-field-based-on-foreign-key
    # y en: https://docs.djangoproject.com/en/3.0/topics/db/aggregation/
    top10=Item.objects.annotate(npos=Count('like', filter=Q(like__boton=1)),
                                nneg= Count('like', filter=Q(like__boton=-1)),
                                nlikes=Sum('like__boton')).order_by('-nlikes')[0:10]
    top5=[]
    if request.user.is_authenticated:
        # top5=Item.objects.annotate(npos=Count('like', filter=Q(like__boton=1)),
        #                             nneg= Count('like', filter=Q(like__boton=-1)).order_by('-nlikes')[0:10]
        top5=[]
    form = AlimForm()
    context = {'user': request.user, 'recurso_us': '/', 'form': form,
                'nav_index': 'active', 'top10': top10}
    return render(request, 'miscosas/index.html', context)


def logout_view(request):
    logout(request)
    recurso_us = request.GET['recurso']
    print(recurso_us)
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
            msg = "Informacion de autenticacioin no valida, o el usuario ya tiene cuenta"
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


def cuenta_usuario(request, us):
    try:
        usuario = User.objects.get(username=us)
    except ObjectDoesNotExist:
        return render(request, 'miscosas/usuario.html', {'error': "El usuario pedido no existe"})

    pagUsEstilo = PagUsuario.objects.get(usuario=usuario)
    if request.method == 'POST':
        action = request.POST['action']
        if action=="foto":
            pagUsEstilo.foto = request.POST['url']
            pagUsEstilo.save()
        elif action=="formato":
            form = PagUsForm(request.POST)
            if form.is_valid():
                pagUsEstilo.tamLetra = form.cleaned_data['tamano']
                pagUsEstilo.estilo = form.cleaned_data['estilo']
                pagUsEstilo.save()
    form = PagUsForm()
    context = {'form': form, 'usuario': us, 'recurso_us': '/usuario/'+us,
                'foto': pagUsEstilo.foto, 'error': ""}
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
