
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
    def codigo_dh(self):
        codigo_dh = ''
        try:
            codigo_dh = self.obj.CodigoDH.text
        except AttributeError:
            pass
        return codigo_dh


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
