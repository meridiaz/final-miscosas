#!/usr/bin/python3

# Simple XML parser for YouTube XML channels
# Jesus M. Gonzalez-Barahona <jgb @ gsyc.es> 2020
# SARO and SAT subjects (Universidad Rey Juan Carlos)
#
# Example of XML document for a YouTube channel:
# https://www.youtube.com/feeds/videos.xml?channel_id=UC300utwSVAYOoRLEqmsprfg

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
from urllib.request import urlopen
from django.core.exceptions import ObjectDoesNotExist
from urllib.error import URLError

class SUBHandler(ContentHandler):
    def meterBSVideo(self):
        from .models import Item, Alimentador

        if self.sub == "":
            try:
                self.sub = Alimentador.objects.get(enlace=self.SubLink)
            except ObjectDoesNotExist:
                self.sub= Alimentador(nombre=self.SubTit, enlace=self.SubLink, tipo="reddit")
                self.sub.save()

        try:
            v = Item.objects.get(enlace=self.link)
        except ObjectDoesNotExist:
            v = Item(alimentador=self.sub, titulo=self.title, enlace=self.link,
                      descrip=self.descrip)
            v.save()

    def __init__ (self):

        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""

        self.id = ""

        self.link = ""

        self.inContentCanal = False
        self.sub = ""
        self.inSub = False
        self.SubLink = ""
        self.descrip = ""
        self.SubTit = ""

    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title' or name == "media:description":
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == "content":
                self.inContent = True
        elif name == "feed":
            self.inSub = True
        elif self.inSub:
            if name == "title":
                self.inContent = True
            elif name == "link" and (attrs.get('rel') == "alternate"):
                self.SubLink = attrs.get('href')

    def endElement (self, name):
        if name == 'entry':
            self.inEntry = False
            self.meterBSVideo()
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == "content":
                self.descrip = self.content
                self.content = ""
                self.inContent = False
        elif name == "feed":
            self.inSub = False
        elif self.inSub:
            if name == "title":
                self.SubTit = self.content
                self.inContent = False
                self.content = ""

    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class SubReddit:

    def __init__(self, nombre):

        url = 'https://www.reddit.com/'+ nombre+".rss"
        print("--------------------"+url)
        self.id = -1
        try:
            xmlStream = urlopen(url)
            self.parser = make_parser()
            self.handler = SUBHandler()
            self.parser.setContentHandler(self.handler)
            self.parser.parse(xmlStream)
            self.handler.sub.id_canal = nombre
            self.handler.sub.save()
            self.id= self.handler.sub.id
        except URLError as e:
            print("Error al abrir la url")
            print(e)


    def id_reddit(self):
        return self.id
