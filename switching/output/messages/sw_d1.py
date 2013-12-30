# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera
from sw_c1 import DatosSolicitud, Contrato, Cliente, DatosAceptacion
from sw_c1 import DatosActivacion, PuntosDeMedida
from sw_c2 import Medida, Comentarios, RegistrosDocumento


class NotificacionCambiosATRDesdeDistribuidor(XmlModel):
    _sort_order = ('notificacion_cambio', 'motivo_cambio')

    def __init__(self):
        self.notificacion_cambio = XmlField(
                                     'NotificacionCambiosATRDesdeDistribuidor'
        )
        self.motivo_cambio = XmlField('MotivoCambioATRDesdeDistribuidora')
        super(NotificacionCambiosATRDesdeDistribuidor, self).\
                    __init__('NotificacionCambiosATRDesdeDistribuidor',
                             'notificacion_cambio')


class MensajeMotivo(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'notificacion_cambio',
                   'periodicidad_facturacion')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeMotivo',
                          attributes={
                              'xmlns': 'http://localhost/elegibilidad'
                          }
        )
        self.cabecera = Cabecera()
        self.notificacion_cambio = NotificacionCambiosATRDesdeDistribuidor()
        self.periodicidad_facturacion = XmlField('PeriodicidadFacturacion')
        super(MensajeMotivo, self).\
              __init__('MensajeMotivo', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
