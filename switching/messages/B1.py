# -*- coding: utf-8 -*-

from message import Message, except_f1
import C1, C2

class B1(Message):
    """Classe que implementa A3."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return C1.Sollicitud(self.obj.BajaEnergia.DatosSolicitud)