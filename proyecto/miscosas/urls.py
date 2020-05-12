from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [

    path('logout', views.logout_view, name="logout_view"),
    path('login', views.login_view, name="login_view"),
    path('style.css', views.procesar_css, name="procesar_css"),
    path('alimentador/<str:id>', views.alimentador, name="procesar_alimentador"),
    path('item/<str:id>', views.mostrar_item, name="mostrar_item"),
    path('usuario/<str:us>', views.cuenta_usuario, name="cuenta_usuario"),
    path('alimentadores', views.alimentadores, name="alimentadores"),
    path('usuarios', views.usuarios, name="usuarios"),
    path('', views.index, name="index"),
]
