
# -*- coding: utf-8 -*-

from lxml import objectify, etree

import switching

XSD_DATA = {'F1': 'Facturacion.xsd'}


class Message(object):
    """Classe base"""
    def __init__(self, xml):
        """Construeix un missatge base."""
        if isinstance(xml, file):
            self.check_fpos(xml)
            self.str_xml = xml.read()
        else:
            self.str_xml = xml
        try:
            self.set_tipus()
        except:
            print 'err: No s\'ha pogut identificar el tipus'
            self.tipus = ''
            self.f_xsd = ''
        else:
            try:
                self.tipus = 'a'
                self.set_xsd()
            except:
               print 'err: Tipus \'%s\' no suportat' % self.tipus
               self.f_xsd = ''

    def set_tipus(self):
        """Setejar el tipus de missatge"""
        obj = objectify.fromstring(self.str_xml)
        self.tipus = obj.Cabecera.CodigoDelProceso

    def set_xsd(self):
        """Setejar el fitxer xsd"""
        xsd = switching.get_data(XSD_DATA[self.tipus])
        self.f_xsd = open(xsd, 'r')

    def check_fpos(self, f_obj):
        """Setejar la posició actual dels fixers"""
        if (isinstance(f_obj, file) and f_obj.tell() != 0):
            f_obj.seek(0)

    def get_tipus_xml(self):
        """Obtenir el tipus de missatge"""
        return self.tipus

    def parse_xml(self):
        """Retornar l'objectify amb el contingut de l'xml"""
        if not self.f_xsd:
            return -1
        self.check_fpos(self.f_xsd)
        schema = etree.XMLSchema(file=self.f_xsd)
        parser = objectify.makeparser(schema=schema)
        obj = objectify.fromstring(self.str_xml, parser)
        return obj
