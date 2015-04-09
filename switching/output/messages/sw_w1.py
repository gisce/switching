# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera
from sw_c1 import DatosSolicitud, Contrato, Cliente, DatosAceptacion
from sw_c1 import DatosActivacion, PuntosDeMedida
from sw_c2 import Medida, Comentarios, RegistrosDocumento

class LecturaAportada(XmlModel):
    _sort_order = (
        'lectura_aportada',
        'integrador',
        'codigo_periodedh',
        'lectura_propuesta',
        )

    def __init__(self):
        self.lectura_aportada = XmlField('LecturaAportada')
        self.integrador = XmlField('Integrador')
        self.codigo_periodedh = XmlField('CodigoPeriodoDH')
        self.lectura_propuesta = XmlField('LecturaPropuesta')
        super(LecturaAportada, self).__init__(
            'LecturaAportada', 'lectura_aportada')
        

class SolicitudAportacionLectura(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'fecha_lectura',
        'codigodh',
        'lecturas',
        )
        
    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'SolicitudAportacionLectura',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = Cabecera()
        self.fecha_lectura = XmlField('FechaLectura')
        self.codigodh = XmlField('CodigoDH')
        self.lecturas = LecturaAportada()
        super(SolicitudAportacionLectura, self).__init__(
            'SolicitudAportacionLectura', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()

