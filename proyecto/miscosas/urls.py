from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [

    path('logout', views.logout_view, name="logout_view"),
    path('login', views.login_view, name="login_view"),
    path('', views.index, name="index"),
]
