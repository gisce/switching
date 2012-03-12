# -*- coding: utf-8 -*-

import gettext

from defs import *
from message import Message, except_f1
from libfacturacioatr import tarifes

_ = gettext.gettext


class F1(Message):
    """Classe que implementa F1."""

    @property
    def num_factures(self):
        nelem = 0
        try:
            nelem = len(list(self.obj.Facturas.FacturaATR))
        except AttributeError:
            pass
        return nelem

    def __get_factura(self, fact):
        return Factura(self.obj.Facturas.FacturaATR[fact])

    def get_factures(self):
        fact = []
        try:
            for ch in self.obj.Facturas.FacturaATR:
                fact.append(Factura(ch))
        except AttributeError:
            pass
        return fact

    @property
    def data_limit_pagament(self):
        return self.obj.Facturas.RegistroFin.FechaLimitePago.text


class Factura(object):

    def __init__(self, fact):
        self.factura = fact

    # Dades generals
    @property
    def cups(self):
        """Retornar el CUPS"""
        return self.factura.DatosGeneralesFacturaATR.\
               DireccionSuministro.CUPS.text

    @property
    def numero_factura(self):
        """Retornar el número de factura"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.NumeroFactura.text

    @property
    def tipus_factura(self):
        """Retornar el tipus de factura"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.TipoFactura.text

    @property
    def tipus_rectificadora(self):
        """Retornar el tipus de rectificadora"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.IndicativoFacturaRectificadora.text

    @property
    def data_factura(self):
        """Retornar el tipus de factura"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.FechaFactura.text

    @property
    def CIF_emisora(self):
        """Retornar el CIF"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.CIFEmisora.text

    @property
    def observacions(self):
        """Retornar les observacions"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.Observaciones.text

    @property
    def import_total_factura(self):
        """Retornar l'import total"""
        return float(self.factura.DatosGeneralesFacturaATR.\
                     DatosGeneralesFactura.ImporteTotalFactura.text)

    @property
    def import_iva(self):
        """Retorna l'IVA"""
        return float(self.factura.IVA.Importe.text)

    @property
    def import_net(self):
        """Retorna el total sense iva"""
        return float(self.factura.IVA.BaseImponible.text)

    @property
    def saldo_factura(self):
        """Retornar el saldo"""
        return float(self.factura.DatosGeneralesFacturaATR.\
                     DatosGeneralesFactura.SaldoFactura.text)

    @property
    def saldo_cobrament(self):
        """Retornar el cobrament"""
        return float(self.factura.DatosGeneralesFacturaATR.\
                       DatosGeneralesFactura.SaldoCobro.text)

    @property
    def tipus_facturacio(self):
        """Retornar el tipus de facturacio"""
        return self.factura.DatosGeneralesFacturaATR.\
            DatosFacturaATR.TipoFacturacion.text

    @property
    def data_BOE(self):
        """Retornar la data del BOE
           També serveix per saber quines tarifes de preus aplicar
        """
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.FechaBOE.text

    @property
    def codi_tarifa(self):
        """Retornar el codi ocsum de la tarifa"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.CodigoTarifa.text.zfill(3)

    @property
    def ind_mesura_baixa(self):
        """Retornar l'indicador de mesura en baixa"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.IndAltamedidoenBaja.text

    @property
    def data_inici(self):
        """Retornar la data d'inici"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaDesdeFactura.text

    @property
    def data_final(self):
        """Retornar la data final"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaHastaFactura.text

    @property
    def nombre_mesos(self):
        """Retornar el nombre de mesos"""
        return float(self.factura.DatosGeneralesFacturaATR.\
                    DatosFacturaATR.Periodo.NumeroMeses.text)

    def get_linies_factura(self):
        """Retorna una llista de llistes de LiniesFactura"""
        noms_funcio = {'Potencia': [self.get_info_potencia, 'potencia'],
                       'EnergiaActiva': [self.get_info_activa, 'energia'],
                       'EnergiaReactiva': [self.get_info_reactiva,
                                                                  'reactiva'],
                       'Alquileres': [self.get_info_lloguers, 'lloguer'],
                       'ExcesoPotencia': [self.get_info_exces,
                                                             'exces_potencia']}
        contingut = []
        for key in noms_funcio:
            try:
                test = list(eval("self.factura.%s" % key))
                if key == 'Alquileres':
                    data = noms_funcio[key][0]()
                    pobj = LiniesFactura(data, noms_funcio[key][1])
                else:
                    data, total = noms_funcio[key][0]()
                    pobj = LiniesFactura(data, noms_funcio[key][1], total)
                contingut.append(pobj)
            except AttributeError:
                pass
        return contingut

    def get_info_activa(self):
        """Retornat els periodes d'energia"""
        periode = []
        total = 0
        try:
            for ea in self.factura.EnergiaActiva.TerminoEnergiaActiva:
                p = 0
                for i in ea.Periodo:
                    if float(i.PrecioEnergia.text):
                        p += 1
                        periode.append(PeriodeActiva(i, 'P%d' % p))
            total = float(self.factura.EnergiaActiva.
                                            ImporteTotalEnergiaActiva.text)
        except AttributeError:
            pass
        return periode, total

    def get_info_reactiva(self):
        """Retorna els periodes de reactiva
           Assigna el periode que correspon comprovant la quantitat
           en les lectures.
        """
        lectures = self.get_lectures()[1]
        agrupat = INFO_TARIFA[self.codi_tarifa]['agrupat']
        lect_activa = self.select_consum_from_lectures(lectures, 'A')
        lect_reactiva = self.select_consum_from_lectures(lectures, 'R')
        if agrupat:
            lect_activa = tarifes.aggr_consums(lect_activa)
            lect_reactiva = tarifes.aggr_consums(lect_reactiva)
        calc = {}
        marge = INFO_TARIFA[self.codi_tarifa]['marge']
        for i in lect_activa:
            activa = lect_activa[i]
            reactiva = lect_reactiva[i]
            val = float("%.2f" %
                            tarifes.exces_reactiva(activa, reactiva, marge))
            calc.update({i: str(round(val, 2))})

        total = 0
        periode = []
        try:
            for i in self.factura.EnergiaReactiva.TerminoEnergiaReactiva.\
                                                                    Periodo:
                pr = PeriodeReactiva(i)
                quant = str(round(pr.quantitat, 2))
                if not quant > 0:
                    continue
                if not quant in calc.values():
                    raise except_f1('Error', _('Periode de linies de reactiva'
                                               ' no trobat'))
                    continue
                for key in calc:
                    if calc[key] == quant:
                        break
                pr.update_name(key)
                periode.append(pr)
            total = float(self.factura.EnergiaReactiva.\
                             ImporteTotalEnergiaReactiva.text)
        except AttributeError:
            pass
        return periode, total

    def get_info_potencia(self):
        """Retorna els periodes de potència"""
        periode = []
        total = 0
        p = 0
        try:
            for i in self.factura.Potencia.TerminoPotencia.Periodo:
                if float(i.PrecioPotencia.text):
                    p += 1
                    periode.append(PeriodePotencia(i, 'P%d' % p))
            total = float(self.factura.Potencia.
                                        ImporteTotalTerminoPotencia.text)
        except AttributeError:
            pass
        return periode, total

    def get_info_exces(self):
        """Retorna els periodes d'excessos de potència"""
        periode = []
        total = 0
        p = 0
        try:
            for i in self.factura.ExcesoPotencia.Periodo:
                p += 1
                periode.append(PeriodeExces(i, 'P%d' % p))
            total = float(self.factura.ExcesoPotencia.ImporteTotalExcesos.text)
        except AttributeError:
            pass
        return periode, total

    def get_info_lloguers(self):
        """Línies de lloguers"""
        try:
            obj = Lloguer(self.factura.Alquileres.
                          ImporteFacturacionAlquileres.text)
        except AttributeError:
            obj = ''
        return obj

    @property
    def pot_data_inici(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaDesde.text

    @property
    def pot_data_fi(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaHasta.text

    def get_lectures(self):
        """Retorna totes les lectures en una llista de Lectura"""
        lectures = []
        try:
            for lect in self.factura.Medidas.Aparato.Integrador:
                lectures.append(Lectura(lect, self.codi_tarifa))
        except AttributeError:
            pass
        tipus = ''
        cnt_tipus = 0
        for lect in lectures:
            if tipus != lect.tipus:
                cnt = 0
                tipus = lect.tipus
                cnt_tipus += 1
            else:
                cnt += 1
            lect.cnt = cnt
        return cnt_tipus, lectures

    def select_from_lectures(self, lectures, tipus):
        """Retorna les lectures d'energia del tipus indicat"""
        select = {}
        for lect in lectures:
            if lect.tipus in tipus:
                select.update({lect.periode: lect})
        return select

    def select_consum_from_lectures(self, lectures, tipus):
        """Retorna els consums de lectures d'energia del tipus indicat"""
        select = {}
        for lect in lectures:
            if lect.tipus in tipus:
                select.update({lect.periode: lect.consum})
        return select

    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.factura.Medidas.Aparato.NumeroSerie.text

    @property
    def gir_comptador(self):
        return (10 ** int(self.factura.Medidas.Aparato.\
               Integrador.NumeroRuedasEnteras.text))


class LiniesFactura(object):
    def __init__(self, data, tipus, total=None):
        self.data = data
        self._total = total
        self._tipus = tipus

    @property
    def tipus(self):
        return self._tipus

    def get_data(self):
        return self.data

    @property
    def total(self):
        return self._total


class PeriodeActiva(object):

    def __init__(self, periode, name):
        self.periode = periode
        self._name = name

    @property
    def quantitat(self):
        "Retorna kwh"
        return float(self.periode.ValorEnergiaActiva.text)

    @property
    def preu_unitat(self):
        "Retorna el preu de l'energia activa"
        return float(self.periode.PrecioEnergia.text)

    @property
    def name(self):
        "Retorna el nom del periode"
        return self._name


class PeriodeReactiva(object):

    def __init__(self, periode):
        self.periode = periode
        self._name = ''

    @property
    def quantitat(self):
        return float(self.periode.ValorEnergiaReactiva.text)

    @property
    def preu_unitat(self):
        "Retorna el preu de l'energia reactiva"
        return float(self.periode.PrecioEnergiaReactiva.text)

    @property
    def name(self):
        "Retorna el nom del periode"
        return self._name

    def update_name(self, name):
        "Actualitza el name"
        self._name = name


class PeriodePotencia(object):

    def __init__(self, periode, name):
        self.periode = periode
        self._name = name

    @property
    def quantitat(self):
        "Retorna kw"
        return float(self.periode.PotenciaAFacturar.text)

    @property
    def maximetre(self):
        "Retorna la potència màxima demanada"
        return float(self.periode.PotenciaMaxDemandada.text)

    @property
    def preu_unitat(self):
        "Retorna el preu del kw"
        return float(self.periode.PrecioPotencia.text)
    @property
    def name(self):
        "Retorna el nom del periode"
        return self._name


class PeriodeExces(object):
    def __init__(self, periode, name):
        self.periode = periode
        self._name = name

    @property
    def quantitat(self):
        "Retorna kw"
        return float(self.periode.ValorExcesoPotencia.text)

    @property
    def name(self):
        "Retorna el nom del periode"
        return self._name


class Lloguer(object):
    def __init__(self, cost):
        self.cost = cost
    
    @property
    def quantitat(self):
        return float(self.cost)

    
class Lectura(object):

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
        tipus = {'AE': 'A',
                 'R1': 'R',
                 'PM': 'M',
                 'EP': 'EP'}
        return tipus.get(self.lectura.Magnitud.text)

    @property
    def magnitud(self):
        return self.lectura.Magnitud.text

    @property
    def consum(self):
        return float(self.lectura.ConsumoCalculado.text)

    @property
    def periode(self):
        # taula 42
        relacio = {'01': 'P1',  # Punta + Llano
                   '21': 'P1',  # Punta
                   '03': 'P2',  # Valle
                   '10': 'P1',  # Totalizador
                   '61': 'P1',  # Periodo 1
                   '62': 'P2',  # Periodo 2
                   '63': 'P3',  # Periodo 3
                   '64': 'P4',  # Periodo 4
                   '65': 'P5',  # Periodo 5
                   '66': 'P6'}  # Periodo 6

        return relacio[self.lectura.CodigoPeriodo.text]

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
