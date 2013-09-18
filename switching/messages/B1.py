# -*- coding: utf-8 -*-

from message import Message, except_f1
import C1, C2

class B1(Message):
    """Classe que implementa B1."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return C1.Sollicitud(self.obj.BajaEnergia.DatosSolicitud)
    
    @property
    def client(self):
        """Retorna l'objecte Client"""
        return C1.Client(self.obj.BajaEnergia.Cliente)
   
    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self._header)
        return C1.Contracte(obj.IdContrato)
         
    @property
    def direccio_correspondecia(self):
        direccio = False
        try:
            direccio = DireccioAmbIndicador(self.obj.BajaEnergia.DireccionCorrespondencia)
        except AttributeError:
            pass
        return direccio
    
    @property
    def header(self):
        return self._header
    
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

class DireccioAmbIndicador(object):
    """Classe que implementa la direccio"""

    def __init__(self, data):
        self.direccio = data
        
    @property
    def indicador(self):
        """Retorna F/S/O"""
        value = ''
        try:
            value = self.direccio.Indicador.text
        except AttributeError:
            pass
        return value
    
    @property
    def direccio_correspondecia(self):
        value = False
        try:
            value = C1.Direccio(self.direccio.Direccion)
        except AttributeError:
            pass
        return value
    