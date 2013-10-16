
# -*- coding: utf-8 -*-

from message import Message
import C1


class D1(Message):
    """Classe que implementa D1."""

    @property
    def notificacio_canvi(self):
        return NotificacioCanvi(self.obj.
                                NotificacionCambiosATRDesdeDistribuidor)

    @property
    def periodicitat_facturacio(self):
        periodicitat = ''
        try:
            periodicitat = self.obj.PeriodicidadFacturacion.text
        except AttributeError:
            pass
        return periodicitat

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        return False


class NotificacioCanvi(object):
    """Classe que implementa la direccio"""

    def __init__(self, data):
        self.notificacio = data

    @property
    def motiu_canvi(self):
        motiu = ''
        try:
            motiu = self.notificacio.MotivoCambioATRDesdeDistribuidora.text
        except AttributeError:
            pass
        return motiu
