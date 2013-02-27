
# -*- coding: utf-8 -*-

from message import Message, except_f1
import C1


class C2(Message):
    """Classe que implementa C2."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return C1.Sollicitud(self.obj.CambiodeComercializadoraConCambios.\
                          DatosSolicitud)

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self._header)
        return C1.Contracte(obj.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return C1.Client(self.obj.CambiodeComercializadoraConCambios.Cliente)

    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        obj = getattr(self.obj, self._header, False)
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
        return self._header

    @property
    def activacio(self):
        """Retorna l'objecte Activacio"""
        return Activacio(self.obj.\
                            ActivacionCambiodeComercializadoraConCambios)

    @property
    def notificacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Notificacio(self.obj.NotificacionComercializadoraSaliente)
    

    @property
    def anullacio(self):
        """Retorna l'object Anullacio"""
        return C1.Anullacio(self.obj.AnulacionSolicitud)

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(C1.PuntMesura(i))
        return data



class Activacio(object):
    """Classe que implementa l'activació"""
    
    def __init__(self, data):
        self.activacio = data
    
    @property
    def data(self):
        data = ''
        try:
            data = self.activacio.DatosActivacion.Fecha.text
        except AttributeError:
            pass
        return data
    
    @property
    def hora(self):
        hora = ''
        try:
            hora = self.activacio.DatosActivacion.Hora.text
        except AttributeError:
            pass
        return hora

    @property
    def contracte(self):
        contracte = ''
        try:
            contracte = Contracte(self.activacio.Contrato)
        except AttributeError:
            pass
        return contracte

class Acceptacio(object):
    """Classe Acceptacio"""
    
    def __init__(self, data):
        self.acc = data
    
    @property
    def data_acceptacio(self):
        data = ''
        try:
            data = self.acc.FechaAceptacion.text
        except AttributeError:
            pass
        return data

    @property
    def potencia(self):
        pot = ''
        try:
            pot = int(self.acc.PotenciaActual.text)
        except AttributeError:
            pass
        return pot

    @property
    def actuacio_camp(self):
        act = ''
        try:
            act = self.acc.ActuacionCampo.text
        except AttributeError:
            pass
        return act

    @property
    def data_ult_lect(self):
        data = ''
        try:
            data = self.acc.FechaUltimaLectura.text
        except AttributeError:
            pass
        return data
