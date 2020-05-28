import string
from .models import Item, Alimentador, Comentario
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
        element['enlace_miscosas'] = "/alimentador/"+str(alim.id)
        return element

    def insertar_top10_json(self, item):
        """Inserta un item en el diccionario para el JSON"""
        element = {}
        element['nombre'] = item.titulo
        element['enlace'] = item.enlace
        element['id'] = str(item.id)
        element['npos'] = str(item.npos)
        element['nneg'] = str(item.nneg)
        element['enlace_miscosas'] = "/item/"+str(item.id)
        return element

    def insertar_top5_json(self, item):
        """Inserta un item en el diccionario para el JSON"""
        element = {}
        element['nombre'] = item.titulo
        element['enlace'] = item.enlace
        element['id'] = str(item.id)
        element['enlace_miscosas'] = "/item/"+str(item.id)
        return element

    def insertar_users_json(self, elemento):
        """Inserta un usuario en el diccionario para el JSON"""
        element = {}
        element['nombre'] = elemento.usuario.username
        element['items_votados'] = str(elemento.usuario.like_set.all().count())
        element['items_comentados'] = str(elemento.usuario.comentario_set.all().count())
        element['enlace_miscosas'] = "/usuario/"+elemento.usuario.username
        return element

    def insert_comen_json(self, elemento):
        """Inserta un usuario en el diccionario para el JSON"""
        element = {}
        element['nombre'] = elemento.usuario.username
        element['texto'] = elemento.texto
        element['fecha'] = str(elemento.fecha)
        if elemento.foto:
            element['foto'] = '/static/miscosas/'+ elemento.foto.url
        else:
            element['foto'] = ''
        return element

    def insert_lista_json(self, lista, dic, etiqueta):
        for i in lista:
            if etiqueta == "top5" or etiqueta == "lista_items" \
                    or etiqueta == "lista_vot" or etiqueta == "lista_comen":
                dic[etiqueta].append(self.insertar_top5_json(i))
            elif etiqueta == "top10":
                dic['top10'].append(self.insertar_top10_json(i))
            elif etiqueta == "alimentadores":
                dic['alimentadores'].append(self.insertar_alims_json(i))
            elif etiqueta == "usuarios":
                dic['usuarios'].append(self.insertar_users_json(i))
            elif etiqueta == "comentarios":
                dic['comentarios'].append(self.insert_comen_json(i))


    def __init__ (self):
        self.dic = {}

    def json_alims(self, lista):
        self.dic['alimentadores'] = []
        self.insert_lista_json(lista, self.dic, "alimentadores")
        return json.dumps(self.dic, indent=4)

    def json_users(self, lista):
        self.dic['usuarios'] = []
        self.insert_lista_json(lista, self.dic, "usuarios")
        return json.dumps(self.dic, indent=4)

    def json_index(self, top10, top5, lista):
        self.dic['top10'] = []
        self.dic['top5'] = []
        self.dic['alimentadores'] = []
        self.insert_lista_json(top10, self.dic, "top10")
        self.insert_lista_json(top5, self.dic, "top5")
        self.insert_lista_json(lista, self.dic, "alimentadores")
        return json.dumps(self.dic, indent=4)

    def insert_alim_json(self, elemento):
        """Inserta un usuario en el diccionario para el JSON"""
        element = {}
        element['nombre'] = elemento.nombre
        element['enlace'] = elemento.enlace
        element['elegido'] = str(elemento.elegido)
        element['enlace_miscosas'] = "/alimentador/"+str(elemento.id)
        return element


    def insert_us_json(self, elemento):
        """Inserta un usuario en el diccionario para el JSON"""
        element = {}
        element['nombre'] = elemento.usuario.username
        if elemento.foto:
            element['foto'] = '/static/miscosas/'+elemento.foto.url
        else:
            element['foto'] = ''
        return element

    def json_alim(self, alim):
        self.dic['alimentador'] = []
        self.dic['lista_items'] = []
        self.insert_lista_json(alim.item_set.all(), self.dic, "lista_items")
        self.dic['alimentador'].append(self.insert_alim_json(alim))
        return json.dumps(self.dic, indent=4)

    def json_us(self, pagus):
        self.dic['usuario'] = []
        self.dic['lista_comen'] = []
        self.dic['lista_vot'] = []
        lista_vot = Item.objects.filter(like__usuario = pagus.usuario)
        lista_comen = Item.objects.filter(comentario__usuario = pagus.usuario).distinct()
        self.insert_lista_json(lista_vot, self.dic, "lista_vot")
        self.insert_lista_json(lista_comen, self.dic, "lista_comen")
        self.dic['usuario'].append(self.insert_us_json(pagus))
        return json.dumps(self.dic, indent=4)

    def json_item(self, item):
        self.dic['item'] = []
        self.dic['comentarios'] = []
        self.dic['alimentador'] = []
        self.dic['alimentador'].append(self.insert_alim_json(item.alimentador))
        self.dic['item'].append(self.insertar_top5_json(item))
        element = {}
        element['descrip'] = item.descrip
        self.dic['item'].append(element)
        self.insert_lista_json(Comentario.objects.filter(item=item), self.dic, "comentarios")
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
        self.insertar_atributo_xml(child, "ENLACE_MISCOSAS", "/item/"+str(elemento.id))

    def insertar_elemento_xml_top5(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "NOMBRE", elemento.titulo)
        self.insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        self.insertar_atributo_xml(child, "ID", str(elemento.id))
        self.insertar_atributo_xml(child, "ENLACE_MISCOSAS", "/item/"+str(elemento.id))

    def insertar_elemento_xml_alims(self, child, elemento):
        """Inserto cada alimentador de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "NOMBRE", elemento.nombre)
        self.insertar_atributo_xml(child, "ENLACE", elemento.enlace)
        self.insertar_atributo_xml(child, "ID", str(elemento.id))
        self.insertar_atributo_xml(child, "NITEMS", str(elemento.total_it()))
        self.insertar_atributo_xml(child, "NPUNT", str(elemento.count_likes()))
        self.insertar_atributo_xml(child, "ENLACE_MISCOSAS", "/alimentador/"+str(elemento.id))

    def insert_lista_alim(self, alim):
        child = ET.SubElement(self.root, 'alimentador')
        self.insertar_atributo_xml(child, "NOMBRE", alim.nombre)
        self.insertar_atributo_xml(child, "ENLACE", alim.enlace)
        self.insertar_atributo_xml(child, "ELEGIDO", str(alim.elegido))
        self.insertar_atributo_xml(child, "ENLACE_MISCOSAS", "/alimentador/"+str(alim.id))


    def insertar_elemento_xml_us(self, child, elemento):
        """Inserto cada elemento de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "NOMBRE", elemento.usuario.username)
        self.insertar_atributo_xml(child, "ITEMS_VOTADOS", str(elemento.usuario.like_set.all().count()))
        self.insertar_atributo_xml(child, "ITEMS_COMENTADOS", str(elemento.usuario.comentario_set.all().count()))
        self.insertar_atributo_xml(child, "ENLACE_MISCOSAS", "/usuario/"+elemento.usuario.username)

    def insert_us(self, pag_us):
        child = ET.SubElement(self.root, "usuario")
        self.insertar_atributo_xml(child, "NOMBRE", pag_us.usuario.username)
        if pag_us.foto:
            self.insertar_atributo_xml(child, "FOTO", '/static/miscosas/'+pag_us.foto.url)
        else:
            self.insertar_atributo_xml(child, "FOTO", '')

    def insertar_elemento_xml_comen(self, child, elemento):
        """Inserto cada comentario de la lista en el arbol XML"""
        self.insertar_atributo_xml(child, "TEXTO", elemento.texto)
        self.insertar_atributo_xml(child, "USUARIO", elemento.usuario.username)
        self.insertar_atributo_xml(child, "FECHA", str(elemento.fecha))
        if elemento.foto:
            self.insertar_atributo_xml(child, "FOTO", '/static/miscosas/'+ elemento.foto.url)
        else:
            self.insertar_atributo_xml(child, "FOTO", '')

    def insert_lista(self ,lista, etiqueta):
        recurso = ET.SubElement(self.root, etiqueta)
        for i in lista:
            if etiqueta == "top5" or etiqueta =="lista_items" \
                            or etiqueta =="lista_vot" or etiqueta =="lista_comen":
                child = ET.SubElement(recurso, 'item')
                self.insertar_elemento_xml_top5(child, i)
            elif etiqueta == "top10":
                child = ET.SubElement(recurso, 'item')
                self.insertar_elemento_xml_top10(child, i)
            elif etiqueta == "alimentadores":
                child = ET.SubElement(recurso, 'alimentador')
                self.insertar_elemento_xml_alims(child, i)
            elif etiqueta == "usuarios":
                child = ET.SubElement(recurso, 'usuario')
                self.insertar_elemento_xml_us(child, i)
            elif etiqueta == "comentarios":
                child = ET.SubElement(recurso, 'comentario')
                self.insertar_elemento_xml_comen(child, i)


    def __init__ (self):
        self.root = ET.Element('data')


    def xml_users(self, lista):
        self.insert_lista(lista, 'usuarios')
        return ET.tostring(self.root)


    def xml_index(self, top10, top5, lista):
        self.insert_lista(top10, 'top10')
        self.insert_lista(top5, 'top5')
        self.insert_lista(lista, 'alimentadores')
        return ET.tostring(self.root)

    def xml_alims(self, lista):
        self.insert_lista(lista, 'alimentadores')
        return ET.tostring(self.root)

    def xml_alim(self, alim):
        self.insert_lista_alim(alim)
        self.insert_lista(alim.item_set.all(),'lista_items')
        return ET.tostring(self.root)

    def xml_us(self, pag_us):
        lista_vot = Item.objects.filter(like__usuario = pag_us.usuario)
        lista_comen = Item.objects.filter(comentario__usuario = pag_us.usuario).distinct()
        self.insert_us(pag_us)
        self.insert_lista(lista_vot, 'lista_vot')
        self.insert_lista(lista_comen, 'lista_comen')
        return ET.tostring(self.root)

    def xml_item(self, item):
        child = ET.SubElement(self.root, 'alimentador')
        self.insertar_elemento_xml_alims(child, item.alimentador)
        child = ET.SubElement(self.root, 'item')
        self.insertar_elemento_xml_top5(child, item)
        self.insertar_atributo_xml(child, "DESCRIP", item.descrip)
        self.insert_lista(Comentario.objects.filter(item=item), 'comentarios')
        return ET.tostring(self.root)
