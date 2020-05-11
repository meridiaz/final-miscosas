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

class YTHandler(ContentHandler):
    """Class to handle events fired by the SAX parser
    Fills in self.videos with title, link and id for videos
    in a YT channel XML document.
    """

    def __init__ (self):
        """Initialization of variables for the parser
        * inEntry: within <entry>
        * inContent: reading interesting target content (leaf strings)
        * content: target content being readed
        * title: title of the current entry
        * id: id of the current entry
        * link: link of the current entry
        * videos: list of videos (<entry> elements) in the channel,
            each video is a dictionary (title, link, id)
        """
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""
        self.id = ""
        self.link = ""
        self.videos = []

    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == 'yt:videoId':
                self.inContent = True

    def endElement (self, name):
        global videos

        if name == 'entry':
            self.inEntry = False
            self.videos.append({'link': self.link,
                                'title': self.title,
                                'id': self.id})
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == 'yt:videoId':
                self.id = self.content
                self.content = ""
                self.inContent = False

    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class YTChannel:
    """Class to get videos in a YouTube channel.
    Extracts video links and titles from the XML document for a YT channel.
    The list of videos found can be retrieved lated by calling videos()
    """

    def __init__(self, stream):
        self.parser = make_parser()
        self.handler = YTHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(stream)

    def videos (self):

        return self.handler.videos
