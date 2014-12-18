# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera

class MensajeSolicitudInformacionAlRegistrodePS(XmlModel):                             
    _sort_order = ('missatge', 'capcalera')                       
                                                                                
    def __init__(self):                                                         
        self.doc_root = None                                                    
        self.missatge = XmlField('MensajeSolicitudInformacionAlRegistrodePS',          
                         attributes={'xmlns': 'http://localhost/elegibilidad'}) 
        self.capcalera = Cabecera()
        super(MensajeSolicitudInformacionAlRegistrodePS, self).\
                    __init__('MensajeSolicitudInformacionAlRegistrodePS','missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
    

class DatosRechazo(XmlModel):
    _sort_order = ('rechazo', 'motivo')

    def __init__(self):
        self.rechazo = XmlField('DatosRechazo')
        self.motivo = XmlField('Motivo')
        super(DatosRechazo, self).\
                    __init__('DatosRechazo',
                             'rechazo')


class RechazoSolicitudInfRegistroPS(XmlModel):
    _sort_order = ('rechazo_solicitud', 'datos_rechazo')

    def __init__(self):
        self.rechazo_solicitud = XmlField('RechazoSolicitudInfRegistroPS')
        self.datos_rechazo = DatosRechazo()
        super(RechazoSolicitudInfRegistroPS, self).\
                    __init__('RechazoSolicitudInfRegistroPS',
                             'rechazo_solicitud')


class MensajeRechazoSolicitudInfRegistroPS(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'rechazo_solicitud')                       
                                                                                
    def __init__(self):                                                         
        self.doc_root = None                                                    
        self.missatge = XmlField('MensajeRechazoSolicitudInfRegistroPS',
                         attributes={'xmlns': 'http://localhost/elegibilidad'}) 
        self.capcalera = Cabecera()
        self.rechazo_solicitud = RechazoSolicitudInfRegistroPS()
        super(MensajeRechazoSolicitudInfRegistroPS, self).\
                    __init__('MensajeRechazoSolicitudInfRegistroPS', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
    

