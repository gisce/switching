# -*- coding: utf-8 -*-

from message import Message, except_f1
from F1 import Lectura, Comptador

class Q1(Message):
    """Classe que implementa Q1."""
    
    def get_comptadors(self):
        """Retorna totes les lectures en una llista de comptadors"""
        comptadors = []
        for mesura in self.obj.Medidas:
            if mesura.CodUnificadoPuntoSuministro.text == self.get_codi:
                for aparell in mesura.Aparato:
                    comptadors.append(Comptador(aparell))
        return comptadors

