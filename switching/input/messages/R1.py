# -*- coding: utf-8 -*-

from message import Message
import C1


class R1(Message):
    """Classe que implementa R1."""

    def set_xsd(self):
        super(R1, self).set_xsd()
        self._header = 'SolicitudReclamacion'

    @property
    def header(self):
        return self._header

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return DatosPasoSollicitud(self.obj.SolicitudReclamacion.DatosSolicitud)

    # @property
    # def reclamacions(self):
    #     """Retorna l'objecte Sollicitud"""
    #     return Reclamacions(
    #         self.obj.SolicitudReclamacion.VariablesDetalleReclamacion
    #     )

    @property
    def client(self):
        """Retorna l'objecte Client"""
        obj = getattr(self.obj, self._header)
        if len(getattr(obj, 'Cliente', [])):
            return C1.Client(obj.Cliente)

    @property
    def tipus_reclamant(self):
        """Retorna l'objecte Tipo Reclamante"""
        return self.obj.SolicitudReclamacion.TipoReclamante.text

    # @property
    # def reclamant(self):
    #     """Retorna l'objecte Client"""
    #     obj = getattr(self.obj, self._header)
    #     if getattr('Reclamante', obj.SolicitudReclamacion.Reclamante, False):
    #         return Reclamant(self.obj.SolicitudReclamacion.Reclamante)

    @property
    def comentaris(self):
        """Retorna els comentaris (si hi son)"""
        obj = getattr(self.obj, self._header)
        if len(getattr(obj, 'Comentarios', False)):
            return obj.Comentarios.text
        else:
            return ''

    # @property
    # def acceptacio(self):
    #     """Retorna l'objecte Acceptacio"""
    #     obj = getattr(self.obj, self._header, False)
    #     if obj and hasattr(obj, 'DatosAceptacion'):
    #         return C1.Acceptacio(obj.DatosAceptacion)
    #     return False
    #
    # @property
    # def activacio(self):
    #     """Retorna l'objecte Activacio"""
    #     return C1.Activacio(self.obj.NotificacionBajaEnergia)
    #
    # @property
    # def anullacio(self):
    #     """Retorna l'object Anullacio"""
    #     return C1.Anullacio(self.obj.AnulacionSolicitud)
    #
    # @property
    # def rebuig(self):
    #     """Retorna una llista de Rebuig"""
    #     data = []
    #     for i in self.obj.RechazoATRDistribuidoras.Rechazo:
    #         data.append(C1.Rebuig(i))
    #     return data
    #
    # @property
    # def rebuig_anullacio(self):
    #     """Retorna l'objecte Rebuig"""
    #     data = []
    #     for i in self.obj.RechazoDeAnulacion.RechazoAnulacion:
    #         data.append(C1.Rebuig(i))
    #     return data
    #
    # @property
    # def contracte(self):
    #     """Retorna l'objecte Contracte"""
    #     obj = getattr(self.obj, self._header)
    #     try:
    #         idcontrato = C1.Contracte(obj.IdContrato)
    #     except AttributeError:
    #         # Step 04 Acceptacio has the classic structure
    #         idcontrato = C1.Contracte(obj.Contrato)
    #     return idcontrato
    #
    # @property
    # def direccio_correspondecia(self):
    #     direccio = False
    #     try:
    #         direccio = DireccioAmbIndicador(self.obj.BajaEnergia.DireccionCorrespondencia)
    #     except AttributeError:
    #         pass
    #     return direccio

    # @property
    # def punts_mesura(self):
    #     """Retorna una llista de punts de mesura"""
    #     data = []
    #     obj = getattr(self.obj, self._header)
    #     for i in obj.PuntosDeMedida.PuntoDeMedida:
    #         data.append(C1.PuntMesura(i))
    #     return data


class DatosPasoSollicitud(object):
    """Classe que implementa la sol·licitud"""

    def __init__(self, data):
        self.sollicitud = data

    @property
    def tipus(self):
        return self.sollicitud.Tipo.text

    @property
    def subtipus(self):
        return self.sollicitud.Subtipo.text

    @property
    def sollicitudadm(self):
        """Referència orígen"""
        ref = None
        try:
            ref = self.sollicitud.RefernciaOrigen.text
        except AttributeError:
            pass
        return ref
