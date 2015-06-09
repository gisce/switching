# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera
from sw_c1 import DatosSolicitud, Contrato, Cliente, DatosAceptacion
from sw_c1 import DatosActivacion, PuntosDeMedida
from sw_c2 import Medida, Comentarios, RegistrosDocumento, DocTecnica


class ModificacionDeATR(XmlModel):
    _sort_order = ('cambio', 'solicitud', 'contrato', 'cliente',
                   'cliente_saliente', 'medida', 'doctecnica',
                   'comentario', 'registro')

    def __init__(self):
        self.cambio= XmlField('ModificacionDeATR')
        self.solicitud = DatosSolicitud()
        self.contrato = Contrato()
        self.cliente = Cliente()
        self.cliente_saliente = Cliente()
        self.medida = Medida()
        self.doctecnica = DocTecnica()
        self.comentario = Comentarios()
        self.registro = RegistrosDocumento()
        super(ModificacionDeATR, self).\
                    __init__('ModificacionDeATR', 'cambio')


class MensajeModificacionDeATR(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'cambio')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeModificacionDeATR', 
                          attributes={
                              'xmlns': 'http://localhost/elegibilidad'
                           })
        self.cabecera = Cabecera()
        self.cambio = ModificacionDeATR()
        super(MensajeModificacionDeATR, self).\
               __init__('MensajeModificacionDeATR', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()

class AceptacionModificacionDeATR(XmlModel):
    _sort_order = ('acceptacio', 'dades', 'contracte')

    def __init__(self):
        self.acceptacio = \
                       XmlField('AceptacionModificacionDeATR')
        self.dades = DatosAceptacion()
        self.contracte = Contrato()
        super(AceptacionModificacionDeATR, self).\
         __init__('AceptacionModificacionDeATR', 'acceptacio')


class MensajeAceptacionModificacionDeATR(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'acceptacio')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeAceptacionModificacionDeATR',
                         attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.acceptacio = AceptacionModificacionDeATR() 
        super(MensajeAceptacionModificacionDeATR, self).\
                __init__('MensajeAceptacionModificacionDeATR',
                         'missatge')
        
    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class ActivacionModificacionDeATR(XmlModel):
    _sort_order = ('activacio', 'dades', 'contracte', 'punts_mesura')
    
    def __init__(self):
        self.activacio = XmlField('ActivacionModificacionDeATR')
        self.dades = DatosActivacion()
        self.contracte = Contrato()
        self.punts_mesura = PuntosDeMedida()
        super(ActivacionModificacionDeATR, self).\
                __init__('ActivacionModificacionDeATR', 'activacio')


class MensajeActivacionModificacionDeATR(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'activacio')

    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeActivacionModificacionDeATR',
                     attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.activacio = ActivacionModificacionDeATR()
        super(MensajeActivacionModificacionDeATR, self).\
                     __init__('MensajeActivacionModificacionDeATR', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
