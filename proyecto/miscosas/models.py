from django.db import models
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField

tamano = {'pequena': 30,
            'mediana': 40,
            'grande': 50}

estilous = {'oscuro': {'color_letra': 'white', 'fondo_cabec': 'fondo_cabecera_oscuro.jpg',
                        'fondo': 'fondo_oscuro.jpg'},
            'ligero': {'color_letra': 'black', 'fondo_cabec': 'fondo_cabecera2.jpg',
                        'fondo': 'fondo.jpg'}}
# Create your models here.
class Alimentador(models.Model):
    nombre = models.CharField(max_length=64)
    enlace = models.TextField()
    elegido = models.BooleanField()

    def __str__(self):
        return self.nombre

#class LastAlim(Alimentador):

# class estiloPag(models.Model):
#     color_letra = models.CharField(max_length=10)
#     fondo_cabec = models.CharField(max_length=20)

class PagUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.TextField(default="")
    tamLetra =  models.CharField(max_length=10, default='mediana')
    estilo = models.CharField(default='ligero', max_length=100)
    #alimentadores = ArrayField(ArrayField(Alimentador))


class Item(models.Model):
    titulo = models.CharField(max_length=64)
    enlace = models.TextField()
    descrip = models.TextField()
    alimentador =  models.ForeignKey(Alimentador, on_delete=models.CASCADE)

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    texto =  models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    #el campo de a continuacion indica si el video tiene un like por parte del usuario: 1
    #no lo ha votado : 0
    #o le ha dado a dislike: -1
    class Answer(models.IntegerChoices):
        like = 1,
        dislike = -1
        __empty__ = 0

    boton = models.IntegerField(choices=Answer.choices, default=0)
