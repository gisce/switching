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

    @property
    def te_ajust(self):
        res = get_rec_attr(self.lectura, 'Ajuste', default={})
        return len(res) > 0

    @property
    def motiu_ajust(self):
        if self.te_ajust:
            return self.lectura.Ajuste.CodigoMotivoAjuste.text

    @property
    def ajust(self):
        if self.te_ajust:
            return int(self.lectura.Ajuste.AjustePorIntegrador.text)

    def get_info_ajust(self):
        res = None
        if self.te_ajust:
            res = {
                'motivo': self.motiu_ajust,
                'ajuste': self.ajust
            }
        return res

    def calculate_consume(self):
        res = self.valor_lectura_final - self.valor_lectura_inicial
        if self.te_ajust:
            res += self.ajust
        return res


class Comptador(object):
    """Classe que implementa el Comptador"""
    
    def __init__(self, data):
        self.obj = data

    def get_lectures(self, tipus=None):
        """Retorna totes les lectures en una llista de Lectura"""
        lectures = []
        try:
            for lect in self.obj.Integrador:
                lectura = Lectura(lect)
                # If we don't have any type requirements or the current
                # reading is in them
                if not tipus or lectura.tipus in tipus:
                    lectures.append(lectura)
        except AttributeError:
            pass
        return lectures

    def get_lectures_activa(self):
        return self.get_lectures(['A'])

    def get_lectures_reactiva(self):
        return self.get_lectures(['R'])

    def get_lectures_energia(self):
        return self.get_lectures(['A', 'R'])

    def get_lectures_maximetre(self):
        return self.get_lectures(['M'])

    def get_consumes(self, tipus=None):
        consumes = {}
        for lect in self.get_lectures(tipus):
            valor_final = lect.valor_lectura_final
            valor_inicial = lect.valor_lectura_inicial
            ajust = lect.ajust or 0
            ret_type = lect.tipus
            consumes.setdefault(
                ret_type, {}
            )[lect.periode] = valor_final - valor_inicial + ajust
        return consumes

    def get_energy_consumes(self):
        return self.get_consumes(['A', 'R'])

    def get_power_consumes(self):
        return self.get_consumes(['M'])

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
