import string
from .models import Item, Alimentador
import xml.etree.ElementTree as ET
import json

class JSON_create():
    def insertar_alims_json(self, alim):
        """Inserta un alimentador en el diccionario para el JSON"""
        element = {}
        element['nombre'] = alim.nombre
        element['enlace'] = alim.enlace
        element['id'] = str(alim.id)
        element['tot_items'] = str(alim.total_it())
        element['nlikes'] = str(alim.count_likes())
        return element

    def insertar_top10_json(self, item):
        """Inserta un aparcamiento en el diccionario para el JSON"""
        element = {}
        element['nombre'] = item.titulo
        element['enlace'] = item.enlace
        element['id'] = str(item.id)
        element['npos'] = str(item.npos)
        element['nneg'] = str(item.nneg)
        return element

    def insertar_top5_json(self, item):
        """Inserta un aparcamiento en el diccionario para el JSON"""
        element = {}
        element['nombre'] = item.titulo
        element['enlace'] = item.enlace
        element['id'] = str(item.id)
        return element

    def insert_lista_json(self, lista, dic, etiqueta):
        for i in lista:
            if etiqueta == "top5":
                dic['top5'].append(self.insertar_top5_json(i))
            elif etiqueta == "top10":
                dic['top10'].append(self.insertar_top10_json(i))
            elif etiqueta == "alimentadores":
                dic['alimentadores'].append(self.insertar_alims_json(i))


    def __init__ (self, top10, top5, lista):
            self.dic = {}
            self.dic['top10'] = []
            self.dic['top5'] = []
            self.dic['alimentadores'] = []
            self.insert_lista_json(top10, self.dic, "top10")
            self.insert_lista_json(top5, self.dic, "top5")
            self.insert_lista_json(lista, self.dic, "alimentadores")


    def json_to_string(self):
            return json.dumps(self.dic, indent=4)


class XML_create():
    def insertar_atributo_xml(self, child, atributo, valor):
        """Inserta un atributo en el arbol XML"""
        atrib = ET.SubElement(child, 'atributo', {'nombre': atributo})
        atrib.text = valor

    def insertar_elemento_xml_top10(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "NOMBRE", elemento.titulo)
        self.insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        self.insertar_atributo_xml(child, "ID", str(elemento.id))
        self.insertar_atributo_xml(child, "NPOS", str(elemento.npos))
        self.insertar_atributo_xml(child, "NNEG", str(elemento.nneg))

    def insertar_elemento_xml_top5(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "NOMBRE", elemento.titulo)
        self.insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        self.insertar_atributo_xml(child, "ID", str(elemento.id))

    def insertar_elemento_xml_alims(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "NOMBRE", elemento.nombre)
        self.insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        self.insertar_atributo_xml(child, "ID", str(elemento.id))
        self.insertar_atributo_xml(child, "NITEMS", str(elemento.total_it()))
        self.insertar_atributo_xml(child, "NPUNT", str(elemento.count_likes()))

    def insert_lista(self ,lista, etiqueta):
        recurso = ET.SubElement(self.root, etiqueta)
        for i in lista:
            if etiqueta == "top5":
                child = ET.SubElement(recurso, 'item')
                self.insertar_elemento_xml_top5(child, i)
            elif etiqueta == "top10":
                child = ET.SubElement(recurso, 'item')
                self.insertar_elemento_xml_top10(child, i)
            elif etiqueta == "alimentadores":
                child = ET.SubElement(recurso, 'alimentador')
                self.insertar_elemento_xml_alims(child, i)


    def __init__ (self, top10, top5, lista):
        self.root = ET.Element('data')
        self.insert_lista(top10, 'top10')
        self.insert_lista(top5, 'top5')
        self.insert_lista(lista, 'alimentadores')


    def xml_to_string(self):
        return ET.tostring(self.root)
