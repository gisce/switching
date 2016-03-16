# -*- coding: utf-8 -*-
from datetime import date, datetime

from message import Message, except_f1
from switching.helpers.funcions import get_rec_attr
from defs import *


class Q1(Message):
    """Classe que implementa Q1."""

    def get_comptadors(self):
        """Retorna totes les lectures en una llista de comptadors"""
        return Q1._get_comptadors(self)

    @staticmethod
    def _get_comptadors(self, obj=None):
        """Retorna totes les lectures en una llista de comptadors"""
        if obj is None:
            obj = self.obj
        comptadors = []
        for mesura in get_rec_attr(obj, 'Medidas', []):
            if mesura.CodUnificadoPuntoSuministro.text[:20] == \
                                                    self.get_codi[:20]:
                for aparell in mesura.Aparato:
                    compt = Comptador(aparell)
                    di, df = compt.dates_inici_i_final
                    comptadors.append((di, df, compt))
        return [a[2] for a in sorted(comptadors, lambda x,y: cmp(x[0], y[0]))]

    @staticmethod
    def agrupar_lectures_per_periode(lectures):
        """Comprova si hi ha lectures per igual tipus i periode
           amb dates diferents i les agrupa.
        """
        lect = {}
        for i in lectures:
            if not i.tipus in lect:
                lect[i.tipus] = {}
            if not i.periode in lect[i.tipus]:
                lect[i.tipus][i.periode] = []
            lect[i.tipus][i.periode].append(i)
        return lect

    @staticmethod
    def agrupar_lectures_per_data(lectures):
        """Retorna un diccionari de llistes en què les
           claus són les dates inicial i final de les lectures
        """
        lect = {}
        for i in lectures:
            key = '%s-%s' % (i.data_lectura_inicial, i.data_lectura_final)
            if not key in lect:
                lect[key] = []
            lect[key].append(i)
        return lect

    @staticmethod
    def obtenir_data_inici_i_final(dic):
        """Retorna la data inicial i final del diccionari retornat 
           per la funció agrupar_lectures_per_data()
        """
        ret_ini = None
        ret_fi = None
        for i in dic.keys():
            d_ini = date(int(i.split('-')[0]), int(i.split('-')[1]),
                                                        int(i.split('-')[2]))
            if not ret_ini or ret_ini > d_ini:
                ret_ini = d_ini
            d_fi = date(int(i.split('-')[3]), int(i.split('-')[4]),
                                                        int(i.split('-')[5]))
            if not ret_fi or ret_fi < d_fi:
                ret_fi = d_fi
        return datetime.strftime(ret_ini, '%Y-%m-%d'), datetime.strftime(
                                                            ret_fi, '%Y-%m-%d')


class Lectura(object):
    """Classe que implementa la Lectura"""

    def __init__(self, lect, tarifa=None):
        self.lectura = lect
        self.tarifa = tarifa
        self._cnt = 0

    @property
    def cnt(self):
        return self._cnt

    @cnt.setter
    def cnt(self, value):
        self._cnt = value

    @property
    def tipus(self):
        return MAGNITUDS_OCSUM.get(self.lectura.Magnitud.text)

    @property
    def magnitud(self):
        return self.lectura.Magnitud.text

    @property
    def consum(self):
        return float(self.lectura.ConsumoCalculado.text)

    @property
    def periode(self):
        return PERIODE_OCSUM.get(self.lectura.CodigoPeriodo.text, None)

    @property
    def ometre(self):
        return self.lectura.CodigoPeriodo.text in SKIP_TOTALITZADORS

    @property
    def constant_multiplicadora(self):
        return float(self.lectura.ConstanteMultiplicadora.text)

    @property
    def data_lectura_inicial(self):
        data = self.lectura.LecturaDesde.FechaHora.text
        return data[0:data.find('T')]

    @property
    def data_lectura_final(self):
        data = self.lectura.LecturaHasta.FechaHora.text
        return data[0:data.find('T')]

    @property
    def valor_lectura_inicial(self):
        return float(self.lectura.LecturaDesde.Lectura.text)

    @property
    def valor_lectura_final(self):
        return float(self.lectura.LecturaHasta.Lectura.text)

    @property
    def origen_lectura_inicial(self):
        return self.lectura.LecturaDesde.Procedencia.text

    @property
    def origen_lectura_final(self):
        return self.lectura.LecturaHasta.Procedencia.text

    @property
    def gir_comptador(self):
        if self.lectura.NumeroRuedasEnteras.text == '99':
            return 10
        return (10 ** int(self.lectura.NumeroRuedasEnteras.text))


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
    def codiDH(self):
        """Retorna el codi de Discriminació Horaria"""
        return self.obj.CodigoDH.text
    
    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.obj.NumeroSerie.text

    @property
    def gir_comptador(self):
        if self.obj.Integrador.NumeroRuedasEnteras.text == '99':
            return 10
        return (10 ** int(self.obj.Integrador.NumeroRuedasEnteras.text))

    @property
    def dates_inici_i_final(self):
        di = ''
        df = ''
        for lect in self.get_lectures():
           c_di = datetime.strptime(lect.data_lectura_inicial, '%Y-%m-%d')
           c_df = datetime.strptime(lect.data_lectura_final, '%Y-%m-%d')
           di = (not di or c_di < di) and c_di or di
           df = (not df or c_df > df) and c_df or df
        return di, df
