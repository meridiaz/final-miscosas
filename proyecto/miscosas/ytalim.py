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

class YTHandler(ContentHandler):
    def meterBSVideo(self):
        from .models import Item, Alimentador

        if self.canal == "":
            c = Alimentador(nombre=self.CanalTit, enlace=self.CanalLink, tipo="yt")
            c.save()
            self.canal = c
        print("-----------en ytalim:"+self.canal.nombre)
        v = Item(alimentador=self.canal, titulo=self.title, enlace=self.link,
                  descrip=self.descrip, id_item=self.ytid)
        v.save()

    def __init__ (self):

        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""

        self.id = ""

        self.link = ""
        self.videos = []

        self.inContentCanal = False
        self.canal = ""
        self.inCanal = False
        self.CanalLink = ""
        self.descrip = ""
        self.CanalTit = ""
        self.ytid = ""

    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title' or name == "media:description" or name == 'yt:videoId':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
        elif name == "feed":
            self.inCanal = True
        elif self.inCanal:
            if name == "title":
                self.inContent = True
            elif name == "link" and (attrs.get('rel') == "alternate"):
                self.CanalLink = attrs.get('href')

    def endElement (self, name):
        global videos

        if name == 'entry':
            self.inEntry = False
            self.meterBSVideo()
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == "media:description":
                self.descrip = self.content
                self.content = ""
                self.inContent = False
            elif name == "yt:videoId":
                self.ytid = self.content
                self.content = ""
                self.inContent = False
        elif name == "feed":
            self.inCanal = False
        elif self.inCanal:
            if name == "title":
                self.CanalTit = self.content
                self.inContent = False
                self.content = ""

    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class YTChannel:

    def __init__(self, nombre):

        url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
        + nombre
        xmlStream = urlopen(url)
        self.parser = make_parser()
        self.handler = YTHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(xmlStream)

    def __str__(self):
        print("----en yt parser:"+ self.handler.canal.nombre)
        return self.handler.canal.nombre
