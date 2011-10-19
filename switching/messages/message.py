
# -*- coding: utf-8 -*-

from lxml import objectify, etree

class Message(object):
    """Classe base"""
    def __init__(self, f_xml, f_xsd):
        """Construeix un missatge base.
        """
        self.f_xsd = f_xsd
        self.f_xml = f_xml
        self.tipus = ''

    def check_fpos(self):
        """Setejar la posició actual dels fixers
        """
        if (isinstance(self.f_xsd, file) and self.f_xsd.tell() != 0):
            self.f_xsd.seek(0)
        if (isinstance(self.f_xml, file) and self.f_xml.tell() != 0):
            self.f_xml.seek(0)
    
    def get_tipus_xml(self):
        """Obtenir el tipus de missatge
        """
        self.check_fpos()
        obj = objectify.fromstring(self.f_xml.read())
        self.tipus = obj.Cabecera.CodigoDelProceso
        return self.tipus

    def parse_xml(self):
        """Retornar l'objectify amb el contingut de l'xml
        """
        self.check_fpos()
        schema = etree.XMLSchema(file=self.f_xsd)
        parser = objectify.makeparser(schema=schema)
        obj = objectify.fromstring(self.f_xml.read(), parser)
        return obj
    
