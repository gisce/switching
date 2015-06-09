# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera
from sw_c1 import DatosSolicitud, Contrato, Cliente, DatosAceptacion
from sw_c1 import DatosActivacion, PuntosDeMedida
from sw_c2 import Medida, Comentarios, RegistrosDocumento, DocTecnica

class PasoMRAMLConCambiosRestoTarifas(XmlModel):
    _sort_order = ('cambio', 'solicitud', 'contrato', 'cliente',
                   'medida', 'doctecnica', 'comentario', 'registro')
    
    def __init__(self):
        self.cambio= XmlField('PasoMRAMLConCambiosRestoTarifa')
        self.solicitud = DatosSolicitud()
        self.contrato = Contrato()
        self.cliente = Cliente()
        self.cliente_saliente = Cliente()
        self.medida = Medida()
        self.doctecnica = DocTecnica()
        self.comentario = Comentarios()
        self.registro = RegistrosDocumento()
        super(PasoMRAMLConCambiosRestoTarifas, self).\
                    __init__('PasoMRAMLConCambiosRestoTarifa', 'cambio')
                    
class MensajePasoMRAMLConCambiosRestoTarifas(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'cambio')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajePasoMRAMLConCambiosRestoTarifa', 
                          attributes={
                              'xmlns': 'http://localhost/elegibilidad'
                           })
        self.cabecera = Cabecera()
        self.cambio = PasoMRAMLConCambiosRestoTarifas()
        super(MensajePasoMRAMLConCambiosRestoTarifas, self).\
               __init__('MensajePasoMRAMLConCambiosRestoTarifa', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
        
class AceptacionPasoMRAMLConCambiosRestoTarifas(XmlModel):
    _sort_order = ('acceptacio', 'dades', 'contracte')

    def __init__(self):
        self.acceptacio = \
                       XmlField('AceptacionPasoMRAMLConCambiosRestoTarifa')
        self.dades = DatosAceptacion()
        self.contracte = Contrato()
        super(AceptacionPasoMRAMLConCambiosRestoTarifas, self).\
         __init__('AceptacionPasoMRAMLConCambiosRestoTarifas', 'acceptacio')


class MensajeAceptacionPasoMRAMLConCambiosRestoTarifas(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'acceptacio')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField(
                         'MensajeAceptacionPasoMRAMLConCambiosRestoTarifa',
                         attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.acceptacio = AceptacionPasoMRAMLConCambiosRestoTarifas() 
        super(MensajeAceptacionPasoMRAMLConCambiosRestoTarifas, self).\
                __init__('MensajeAceptacionPasoMRAMLConCambiosRestoTarifa',
                         'missatge')
        
    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
        
class ActivacionPasoMRAMLConCambiosRestoTarifas(XmlModel):
    _sort_order = ('activacio', 'dades', 'contracte', 'punts_mesura')
    
    def __init__(self):
        self.activacio = XmlField('ActivacionPasoMRAMLConCambiosRestoTarifas')
        self.dades = DatosActivacion()
        self.contracte = Contrato()
        self.punts_mesura = PuntosDeMedida()
        super(ActivacionPasoMRAMLConCambiosRestoTarifas, self).\
                __init__('ActivacionPasoMRAMLConCambiosRestoTarifas',
                         'activacio')


class MensajeActivacionPasoMRAMLConCambiosRestoTarifas(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'activacio')

    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField(
                         'MensajeActivacionPasoMRAMLConCambiosRestoTarifas',
                         attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.activacio = ActivacionPasoMRAMLConCambiosRestoTarifas()
        super(MensajeActivacionPasoMRAMLConCambiosRestoTarifas, self).\
                __init__('MensajeActivacionPasoMRAMLConCambiosRestoTarifas',
                         'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
