
# -*- coding: utf-8 -*-

from message import Message


class W1(Message):
    """Classe que implementa W1."""

    @property
    def lecturas(self):
        """Retorna una llista de lectures"""
        data = []
        for i in self.obj.LecturaAportada:
            data.append(LecturaAportada(i))
        return data

    @property
    def fecha_lectura(self):
        fecha_lectura = ''
        try:
            fecha_lectura = self.obj.FechaLectura.text
        except AttributeError:
            pass
        return fecha_lectura

    @property
    def aceptacion(self):
        aceptacion = ''
        try:
            aceptacion = Aceptacion(self.obj.DatosAceptacionLectura)
        except AttributeError:
            pass
        return aceptacion

    @property
    def rechazo(self):
        rechazo = ''
        try:
            rechazo = Rechazo(self.obj.DatosRechazoLectura)
        except AttributeError:
            pass
        return rechazo

    @property
    def codigo_dh(self):
        codigo_dh = ''
        try:
            codigo_dh = self.obj.CodigoDH.text
        except AttributeError:
            pass
        return codigo_dh

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        return False


class LecturaAportada(object):
    """Classe que implementa la direccio"""

    def __init__(self, data):
        self.lectura = data

    @property
    def integrador(self):
        integrador = ''
        try:
            integrador = self.lectura.Integrador.text
        except AttributeError:
            pass
        return integrador

    @property
    def codigo_periodo_dh(self):
        codigo_periodo_dh = ''
        try:
            codigo_periodo_dh = self.lectura.CodigoPeriodoDH.text
        except AttributeError:
            pass
        return codigo_periodo_dh

    @property
    def lectura_propuesta(self):
        lectura_propuesta = ''
        try:
            lectura_propuesta = self.lectura.LecturaPropuesta.text
        except AttributeError:
            pass
        return lectura_propuesta


class Aceptacion(object):
    """Classe que implementa la aceptació"""

    def __init__(self, data):
        self.aceptacion = data

    @property
    def fecha_aceptacion(self):
        fecha_aceptacion = ''
        try:
            fecha_aceptacion = self.aceptacion.FechaAceptacion.text
        except AttributeError:
            pass
        return fecha_aceptacion


class Rechazo(object):
    """Classe que implementa la aceptació"""

    def __init__(self, data):
        self.rechazo = data

    @property
    def fecha_rechazo(self):
        fecha_rechazo = ''
        try:
            fecha_rechazo = self.rechazo.FechaRechazo.text
        except AttributeError:
            pass
        return fecha_rechazo

    @property
    def motivo_rechazo(self):
        motivo_rechazo = ''
        try:
            motivo_rechazo = self.rechazo.CodigoMotivo.text
        except AttributeError:
            pass
        return motivo_rechazo
