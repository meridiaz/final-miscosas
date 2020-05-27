#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
from urllib.request import urlopen
from django.core.exceptions import ObjectDoesNotExist
from urllib.error import URLError
from .apikeys import LASTFM_APIKEY

class FMHandler(ContentHandler):
    def meterBSVideo(self):
        from .models import Item, Alimentador

        if self.artista == "":
            try:
                self.artista = Alimentador.objects.get(enlace=self.urlArt)
            except ObjectDoesNotExist:
                self.artista= Alimentador(nombre=self.artistaNombre, enlace=self.urlArt,
                                            tipo="fm")
                self.artista.save()
        print("-----------------"+self.nombre)
        try:
            v = Item.objects.get(enlace=self.urlAlbum)
        except ObjectDoesNotExist:
            v = Item(alimentador=self.artista, titulo=self.nombre, enlace=self.urlAlbum,
                      descrip=self.image, id_item=self.artistaNombre)
            v.save()

    def __init__ (self):

        self.inAlbum = False
        self.inContent = False
        self.content = ""
        self.nombre = ""
        self.artistaNombre = ""
        self.inArtist = False

        self.urlAlbum = ""
        self.urlArt = ""
        self.image = ""

        #variable que contiene el objeto alimentador de tipo artista
        self.artista = ""


    def startElement (self, name, attrs):
        if name == "artist":
            self.inArtist = True
        elif self.inArtist:
            if name == "name" or name == "url":
                self.inContent = True
        elif name == 'album':
            self.inAlbum = True
        elif self.inAlbum and not self.inArtist:
            if name == 'name' or name == "url" \
                    or (name == "image"):
                self.inContent = True


    def endElement (self, name):
        if name == "artist":
            self.inArtist = False
        elif self.inArtist:
            if name == "name":
                self.artistaNombre = self.content
                self.inContent = False
                self.content = ""
            elif name == "url":
                self.urlArt = self.content
                self.inContent = False
                self.content = ""
        elif name == 'album':
            self.inAlbum = False
            self.meterBSVideo()
        elif self.inAlbum:
            if name == 'name':
                self.nombre = self.content
                self.content = ""
                self.inContent = False

            elif name == "url":
                self.urlAlbum = self.content
                self.content = ""
                self.inContent = False

            elif name == "image":
                self.image = self.content
                self.content = ""
                self.inContent = False



    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class FMArtista:

    def __init__(self, nombre):

        url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+\
                nombre+'&api_key=' + LASTFM_APIKEY
        self.id = -1
        try:
            xmlStream = urlopen(url)
            self.parser = make_parser()
            self.handler = FMHandler()
            self.parser.setContentHandler(self.handler)
            self.parser.parse(xmlStream)

            self.handler.artista.id_canal = nombre
            self.handler.artista.elegido = True
            self.handler.artista.save()
            #sentencia que devuelve el id asignado por django para ese objeto artista
            self.id= self.handler.artista.id
        except URLError:
            print("Error al abrir la url")


    def id_artista(self):
        return self.id
