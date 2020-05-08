from django.contrib import admin

from .models import Alimentador, PagUsuario, Item, Comentario, Like
# Register your models here.
admin.site.register(Alimentador)
admin.site.register(PagUsuario)
admin.site.register(Item)
admin.site.register(Comentario)
admin.site.register(Like)
