# -*- coding: utf-8 -*-

from message import Message, except_f1
from F1 import Lectura

class Q1(Message):
    """Classe que implementa Q1."""
    
    def get_lectures(self):
        """Retorna totes les lectures en una llista de Lectura"""
        lectures = []
        try:
            for lect in self.obj.Medidas.Aparato.Integrador:
                lectures.append(Lectura(lect))
        except AttributeError:
            pass
        return lectures

    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.obj.Medidas.Aparato.NumeroSerie.text

    @property
    def gir_comptador(self):
        return (10 ** int(self.obj.Medidas.Aparato.\
               Integrador.NumeroRuedasEnteras.text))
