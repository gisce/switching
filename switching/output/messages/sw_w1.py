# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera


def w1_format_measure(valor):
    return (
        valor if isinstance(valor, basestring)
        else "%.2f" % float(valor) or '0.00'
    )


class DatosAceptacionLectura(XmlModel):
    _sort_order = (
        'datos_aceptacion_lectura',
        'fecha_aceptacion',
    )

    def __init__(self):
        self.datos_aceptacion_lectura = XmlField('DatosAceptacionLectura')
        self.fecha_aceptacion = XmlField('FechaAceptacion')
        super(DatosAceptacionLectura, self).__init__(
            'DatosAceptacionLectura', 'datos_aceptacion_lectura'
        )


class DatosRechazoLectura(XmlModel):
    _sort_order = (
        'datos_rechazo_lectura',
        'fecha_rechazo',
        'motivo',
    )

    def __init__(self):
        self.datos_rechazo_lectura = XmlField('DatosRechazoLectura')
        self.fecha_rechazo = XmlField('FechaRechazo')
        self.motivo = XmlField('CodigoMotivo')
        super(DatosRechazoLectura, self).__init__(
            'DatosRechazoLectura', 'datos_rechazo_lectura'
        )


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
        self.lectura_propuesta = XmlField(
            'LecturaPropuesta', rep=w1_format_measure
        )
        super(LecturaAportada, self).__init__(
            'LecturaAportada', 'lectura_aportada', drop_empty=False)
        

#01
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


#02_ok
class AceptacionAportacionLectura(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'datos_aceptacion',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'AceptacionAportacionLectura',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = Cabecera()
        self.datos_aceptacion = DatosAceptacionLectura()
        super(AceptacionAportacionLectura, self).__init__(
            'AceptacionAportacionLectura', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


#02_ko
class RechazoAportacionLectura(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'datos_rechazo',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'RechazoAportacionLectura',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = Cabecera()
        self.datos_rechazo = DatosRechazoLectura()
        super(RechazoAportacionLectura, self).__init__(
            'RechazoAportacionLectura', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()