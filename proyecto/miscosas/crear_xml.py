import string
from .models import Item, Alimentador
import xml.etree.ElementTree as ET


class XML_create():
    def insertar_atributo_xml(self, child, atributo, valor):
        """Inserta un atributo en el arbol XML"""
        atrib = ET.SubElement(child, 'atributo', {'nombre': atributo})
        atrib.text = valor

    def insertar_elemento_xml_top10(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        insertar_atributo_xml(child, "NOMBRE", elemento.titulo)
        insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        insertar_atributo_xml(child, "ID", str(elemento.id))
        insertar_atributo_xml(child, "NPOS", str(elemento.npos))
        insertar_atributo_xml(child, "NNEG", str(elemento.nneg))

    def insertar_elemento_xml_top5(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        insertar_atributo_xml(child, "NOMBRE", elemento.titulo)
        insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        insertar_atributo_xml(child, "ID", str(elemento.id))

    def insertar_elemento_xml_alims(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        insertar_atributo_xml(child, "NOMBRE", elemento.nombre)
        insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        insertar_atributo_xml(child, "ID", str(elemento.id))
        insertar_atributo_xml(child, "NITEMS", str(elemento.total_it))
        insertar_atributo_xml(child, "NPUNT", str(elemento.count_likes))

    def insert_lista_top10(self, lista, etiqueta, root):
        top10 = ET.SubElement(root, etiqueta)
        for i in lista:
            child = ET.SubElement(top10, 'item')
            insertar_elemento_xml_top10(child, i)

    def insert_lista_top5(self, lista, etiqueta, root):
        top5 = ET.SubElement(root, etiqueta)
        for i in lista:
            child = ET.SubElement(top5, 'item')
            insertar_elemento_xml_top5(child, i)

    def insert_lista_alims(self, lista, etiqueta, root):
        alims = ET.SubElement(root, etiqueta)
        for i in lista:
            child = ET.SubElement(alims, 'alimentador')
            insertar_elemento_xml_alims(child, i)

    def __init__ (self, top10, top5, lista):
        self.root = ET.Element('data')
        insert_lista_top10(top10, 'top10', self.root)
        insert_lista_top5(top5, 'top5', self.root)
        insert_lista_alims(lista, 'alimentadores', self.root)


    def respuesta_htthp(self):
        return HttpResponse(ET.tostring(self.root), content_type="text/xml")
