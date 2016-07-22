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
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        obj = getattr(self.obj, self._header, False)
        if obj and hasattr(obj, 'DatosAceptacion'):
            return C1.Acceptacio(obj.DatosAceptacion)
        return False

    @property
    def activacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Activacio(self.obj.NotificacionBajaEnergia)
        
    @property
    def anullacio(self):
        """Retorna l'object Anullacio"""
        return C1.Anullacio(self.obj.AnulacionSolicitud)
    
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
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self._header)
        try:
            idcontrato = C1.Contracte(obj.IdContrato)
        except AttributeError:
            # Step 04 Acceptacio has the classic structure
            idcontrato = C1.Contracte(obj.Contrato)
        return idcontrato 
         
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
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(C1.PuntMesura(i))
        return data

    @property
    def documents(self):
        """Retorna una llista de documents adjunts"""
        data = []
        obj = getattr(self.obj, self.header)
        if (hasattr(obj, 'RegistrosDocumento') and
                hasattr(obj.RegistrosDocumento, 'RegistroDoc')):
            for d in obj.RegistrosDocumento.RegistroDoc:
                data.append(C1.RegistroDoc(d))
        return data
    
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
    