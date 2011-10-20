
# -*- coding: utf-8 -*-

from lxml import objectify, etree

import switching

XSD_DATA = {'F1': 'Facturacion.xsd'}

class Message(object):
    """Classe base"""
    def __init__(self, xml):
        """Construeix un missatge base.
        """
        if isinstance(xml, file):
            self.check_fpos(xml)
            self.str_xml = xml.read()
        else:
            self.str_xml = xml
        self.f_xsd = ''
        self.tipus = ''

    def set_xsd(self):
        """Setejar el fitxer xsd"""
        xsd = switching.get_data(XSD_DATA[self.tipus])
        self.f_xsd = open(xsd,'r')

    def check_fpos(self, f_obj):
        """Setejar la posició actual dels fixers
        """
        if (isinstance(f_obj, file) and f_obj.tell() != 0):
            f_obj.seek(0)
    
    def get_tipus_xml(self):
        """Obtenir el tipus de missatge
        """
        obj = objectify.fromstring(self.str_xml)
        self.tipus = obj.Cabecera.CodigoDelProceso
        return self.tipus

    def parse_xml(self):
        """Retornar l'objectify amb el contingut de l'xml
        """
        self.set_xsd()
        self.check_fpos(self.f_xsd)
        schema = etree.XMLSchema(file=self.f_xsd)
        parser = objectify.makeparser(schema=schema)
        obj = objectify.fromstring(self.str_xml, parser)
        return obj
    
