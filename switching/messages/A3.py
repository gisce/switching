
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
        obj = getattr(self.obj, self._header)
        return C1.Contracte(obj.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return C1.Client(self.obj.PasoMRAMLConCambiosRestoTarifa.\
                         Cliente)
        
    @property
    def header(self):
        return self._header

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(C1.PuntMesura(i))
        return data

    @property
    def mesura(self):
        """Retorna l'objecte mesura"""
        obj = getattr(self.obj, self._header)
        return C2.Mesura(obj.Medida)

    @property
    def comentaris(self):
        """Retorna una llista de comentaris"""
        data = []
        obj = getattr(self.obj, self._header)
        if (hasattr(obj, 'Comentarios') and
            hasattr(obj.Comentarios, 'Comentario')):
            for i in obj.Comentarios.Comentario:
                data.append(C2.Comentari(i))
        return data