# -*- coding: utf-8 -*-

from message import Message, except_f1
from F1 import Lectura

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


class Comptador(object):
    """Classe que implementa el Comptador"""
    
    def __init__(self, data):
        self.obj = data

    def get_lectures(self):
        """Retorna totes les lectures en una llista de Lectura"""
        lectures = []
        try:
            for lect in self.obj.Integrador:
                lectures.append(Lectura(lect))
        except AttributeError:
            pass
        return lectures

    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.obj.NumeroSerie.text

    @property
    def gir_comptador(self):
        return (10 ** int(self.obj.Integrador.NumeroRuedasEnteras.text))

