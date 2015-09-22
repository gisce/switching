
# -*- coding: utf-8 -*-

from message import Message, except_f1
import C1, C2


class A3(Message):
    """Classe que implementa A3."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return C1.Sollicitud(self.obj.PasoMRAMLConCambiosRestoTarifa.\
                             DatosSolicitud)

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self.header)
        return C1.Contracte(obj.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return C1.Client(self.obj.PasoMRAMLConCambiosRestoTarifa.\
                         Cliente)

    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        obj = getattr(self.obj, self.header, False)
        if obj and hasattr(obj, 'DatosAceptacion'):
            return C1.Acceptacio(obj.DatosAceptacion)
        return False

    @property
    def rebuig(self):
        """Retorna una llista de Rebuig"""
        data = []
        for i in self.obj.RechazoATRDistribuidoras.Rechazo:
            data.append(C1.Rebuig(i))
        return data

    @property
    def rebuig_anullacio(self):
        """Retorna l'objecte Rebuig"""
        data = []
        for i in self.obj.RechazoDeAnulacion.RechazoAnulacion:
            data.append(C1.Rebuig(i))
        return data

    @property
    def header(self):
        header = self._header
        if self._header == 'PasoMRAMLConCambiosRestoTarifas':
            header = 'PasoMRAMLConCambiosRestoTarifa'
        return header

    @property
    def activacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Activacio(self.obj.\
                            ActivacionPasoMRAMLConCambiosRestoTarifas)

    @property
    def anullacio(self):
        """Retorna l'object Anullacio"""
        return C1.Anullacio(self.obj.AnulacionSolicitud)

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self.header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(C1.PuntMesura(i))
        return data

    @property
    def mesura(self):
        """Retorna l'objecte mesura"""
        obj = getattr(self.obj, self.header)
        return C2.Mesura(obj.Medida)

    @property
    def comentaris(self):
        """Retorna una llista de comentaris"""
        data = []
        obj = getattr(self.obj, self.header)
        if (hasattr(obj, 'Comentarios') and
            hasattr(obj.Comentarios, 'Comentario')):
            for i in obj.Comentarios.Comentario:
                data.append(C2.Comentari(i))
        return data

    @property
    def incidencies(self):
        """Retorna una llista de incidencies"""
        data = []
        for i in self.obj.IncidenciasATRDistribuidoras.Incidencia:
            data.append(C1.Rebuig(i))
        return data
