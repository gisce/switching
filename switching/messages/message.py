
# -*- coding: utf-8 -*-

from lxml import objectify, etree

class Message(object):
    """Classe base"""
    def __init__(self, xml, f_xsd):
        """Construeix un missatge base.
        """
        self.f_xsd = f_xsd
        if isinstance(xml, file):
            self.str_xml = xml.read()
        else:
            self.str_xml = xml
        self.tipus = ''

    def check_fpos(self):
        """Setejar la posició actual dels fixers
        """
        if (isinstance(self.f_xsd, file) and self.f_xsd.tell() != 0):
            self.f_xsd.seek(0)
    
    def get_tipus_xml(self):
        """Obtenir el tipus de missatge
        """
        obj = objectify.fromstring(self.str_xml)
        self.tipus = obj.Cabecera.CodigoDelProceso
        return self.tipus

    def parse_xml(self):
        """Retornar l'objectify amb el contingut de l'xml
        """
        self.check_fpos()
        schema = etree.XMLSchema(file=self.f_xsd)
        parser = objectify.makeparser(schema=schema)
        obj = objectify.fromstring(self.str_xml, parser)
        return obj
    
