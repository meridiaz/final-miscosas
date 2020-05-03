from django.db import models

# Create your models here.
class Alimentador(models.Model):
    nombre = models.CharField(max_length=64)
    enlace = models.TextField()
    elegido = models.Boolean()

    def __str__(self):
        return self.nombre


#class LastAlim(Alimentador):
class Usuario(models.Model):
    nombre = models.CharField(max_length=64)
    foto = models.TextField()
    tamLetra =  models.CharField(max_length=10)
    estilo = models.CharField(max_length=10)
    alimentadores = models.ArrayField(Alimentador)

    def __str__(self):
        return "Soy el usuario con nombre: "+ self.nombre


class Item(models.Model):
    titulo = models.CharField(max_length=64)
    enlace = models.TextField()
    descrip = models.TextField()
    alimentador =  models.ForeignKey(Alimentador, on_delete=models.CASCADE)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    texto =  models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Like(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    #el campo de a continuacion indica si el video tiene un like por parte del usuario: 1
    #no lo ha votado : 0
    #o le ha dado a dislike: -1
    class Answer(models.IntegerChoices):
        like = 1,
        dislike = -1
        __empty__ = 0

    boton = models.IntegerField(choices=Answer.choices, default=0)
