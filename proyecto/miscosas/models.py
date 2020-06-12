from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


tamano = {'pequena':{'p': 13, 'h3': 25, 'h2':31},
            'mediana':{'p': 16, 'h3': 28, 'h2':35},
            'grande':{'p': 19, 'h3':32, 'h2': 40}
        }

estilous = {'oscuro': {'color_letra': 'white', 'fondo_cabec': 'fondo_cabecera_oscuro.jpg',
                        'fondo': 'fondo_oscuro.jpg'},
            'ligero': {'color_letra': 'black', 'fondo_cabec': 'fondo_cabecera2.jpg',
                        'fondo': 'fondo.jpg'}}
# Create your models here.
class Alimentador(models.Model):
    tipo = models.CharField(max_length=10, default="")
    nombre = models.CharField(max_length=64)
    enlace = models.TextField(default="") #al canal o al subreddit
    elegido = models.BooleanField(default=True)
    #en el caso del reddit sera igual al nombre del subrredit
    #en el caso del youtube sera el id del id_canal
    #en el caso de fm sera el nombre del artista
    id_canal = models.CharField(max_length=64, default="")
    usuario = models.ManyToManyField(User)


    def __str__(self):
        return self.nombre

    def count_likes(self):
        count = 0
        for item in self.item_set.all():
            count = item.count_likes() + count
        return count

    def total_it(self):
        return self.item_set.all().count()


class PagUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="img_users")
    tamLetra =  models.CharField(max_length=10, default='mediana')
    estilo = models.CharField(default='ligero', max_length=100)


class Item(models.Model):
    titulo = models.CharField(max_length=64)
    enlace = models.TextField()
    descrip = models.TextField()
    alimentador =  models.ForeignKey(Alimentador, on_delete=models.CASCADE)
    id_item = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.titulo

    def count_likes(self):
        count = 0
        for like in self.like_set.all():
            count = like.boton + count
        return count

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now)
    texto =  models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="img_comens", blank=True)

    def __str__(self):
        return "Comentario del item:"+self.item.titulo


class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    boton = models.IntegerField(default=0)
    fecha = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "Like de "+ self.usuario.username +" en el item: "+self.item.titulo
