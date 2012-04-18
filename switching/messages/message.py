
# -*- coding: utf-8 -*-

import gettext
from lxml import objectify, etree

import switching
from switching.types import DecimalElement, check_decimal_element

XSD_DATA = {'F1': 'Facturacion.xsd',
            'Q1': 'SaldoLecturasFacturacion.xsd'}

_ = gettext.gettext

# register the decimal type with objectify
decimal_type = objectify.PyType('decimal', check_decimal_element,
                                DecimalElement)
decimal_type.register(before='float')


class MessageBase(object):
    """Classe base"""
    def __init__(self, xml, force_tipus=''):
        """Construeix un missatge base."""
        if isinstance(xml, file):
            self.check_fpos(xml)
            xml = xml.read()
        # Fem desaparèixer el header amb l'encoding de l'xml
        # <?xml version="1.0" encoding="ISO-8859-1"?>
        try:
            root = etree.fromstring(xml)
        except etree.XMLSyntaxError:
            raise except_f1('Error', 'Fitxer XML erroni')
        uxml = etree.tostring(root).decode('iso-8859-1')
        self.str_xml = uxml
        self.tipus = ''
        self.f_xsd = ''
        self.set_tipus()
        if force_tipus and self.tipus != force_tipus:
            msg = 'L\'XML no es correspon al tipus %s' % force_tipus
            raise except_f1('Error', _(msg))
        self.set_xsd()
    
    def set_tipus(self):
        """Set type of message. To implement in child classes"""
        pass

    def set_xsd(self):
        """Set xsd. To implement in child classes"""
        pass

    def check_fpos(self, f_obj):
        """Setejar la posició actual dels fixers"""
        if (isinstance(f_obj, file) and f_obj.tell() != 0):
            f_obj.seek(0)

    def get_tipus_xml(self):
        """Obtenir el tipus de missatge"""
        return self.tipus

    def parse_xml(self):
        """Import xml content. To implement in child classes"""
        pass


class Message(MessageBase):
    """Classe base intercanvi informacio comer-distri"""
    
    def set_tipus(self):
        """Setejar el tipus de missatge"""
        try:
            obj = objectify.fromstring(self.str_xml)
            self.tipus = obj.Cabecera.CodigoDelProceso.text
        except: 
            msg = 'No s\'ha pogut identificar el tipus'
            raise except_f1('Error', _(msg))

    def set_xsd(self):
        """Setejar el fitxer xsd"""
        if self.tipus not in XSD_DATA:
            msg = ('Tipus \'%s\'  no suportat' % self.tipus)
            raise except_f1('Error', _(msg))
        try:
            xsd = switching.get_data(XSD_DATA[self.tipus])
            self.f_xsd = open(xsd, 'r') 
        except:
            msg = ('Fitxer \'%s\' corrupte' % 
                        switching.get_data(XSD_DATA[self.tipus]))
            raise except_f1('Error', _(msg))

    def parse_xml(self):
        """Importar el contingut de l'xml"""
        self.check_fpos(self.f_xsd)
        schema = etree.XMLSchema(file=self.f_xsd)
        parser = objectify.makeparser(schema=schema)
        try:
            self.obj = objectify.fromstring(self.str_xml, parser)
        except:
            raise except_f1('Error', _('Document invàlid'))

    # Funcions relacionades amb la capçalera del XML
    @property
    def get_codi_emisor(self):
        ref = int(self.obj.Cabecera.CodigoREEEmpresaEmisora.text)
        if not ref:
            raise except_f1('Error', _('Document sense emisor'))
        return '%04d' % ref

    @property
    def get_codi(self):
        ref = self.obj.Cabecera.Codigo.text
        if not ref:
            raise except_f1('Error', _('Document sense codi'))
        return ref

    @property
    def codi_sollicitud(self):
        ref = self.obj.Cabecera.CodigoDeSolicitud.text
        if not ref:
            raise except_f1('Error', _('Document sense codi de'\
                                       ' sol·licitud'))
        return ref

    @property
    def seq_sollicitud(self):
        ref = self.obj.Cabecera.SecuencialDeSolicitud.text
        if not ref:
            raise except_f1('Error', _('Document sense codi de'\
                                       ' seqüencial de sol·licitud'))
        return ref


class MessageTG(MessageBase):
    """Classe base missatges telegestio"""
    
    def set_tipus(self):
        """Setejar el tipus de missatge"""
        try:
            obj = objectify.fromstring(self.str_xml)
            self.tipus = obj.get('IdRpt')
        except: 
            msg = 'No s\'ha pogut identificar el tipus'
            raise except_f1('Error', _(msg))

    def set_xsd(self):
        """Set xsd file. TG XML files do not use xsd :("""
        pass

    def parse_xml(self):
        """Import xml content"""
        try:
            self.obj = objectify.fromstring(self.str_xml)
        except:
            raise except_f1('Error', _('Document invàlid'))

    # Funcions relacionades amb la capçalera del XML
    @property
    def version(self):
        ref = self.obj.get('Version')
        if not ref:
            raise except_f1('Error', _('Document sense versió'))
        return ref

    @property
    def petition(self):
        ref = self.obj.get('IdPet')
        if not ref:
            raise except_f1('Error', _('Document sense codi de'\
                                       ' petició'))
        return ref


class except_f1(Exception):
    def __init__(self, name, value):
        self.name = name
        self.value = value
