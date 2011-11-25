# -*- coding: utf-8 -*-

from message import Message


class F1(Message):
    """Classe que implementa F1."""

    @property
    def num_factures(self):
        nelem = 0
        for ch in  self.obj.Facturas.getchildren():
            if 'FacturaATR' in ch.tag:
                nelem += 1
        return nelem

    def __get_factura(self, fact):
        return Factura(self.obj.Facturas.FacturaATR[fact])

    def get_factures(self):
        fact = []
        for ch in self.obj.Facturas.getchildren():
            if 'FacturaATR' in ch.tag:
                fact.append(Factura(ch))
        return fact

    @property
    def data_limit_pagament(self):
        return self.obj.Facturas.RegistroFin.FechaLimitePago


class Factura(object):

    def __init__(self, fact):
        self.factura = fact

    # Dades generals
    @property
    def cups(self):
        """Retornar el CUPS"""
        return self.factura.DatosGeneralesFacturaATR.\
               DireccionSuministro.CUPS

    @property
    def numero_factura(self):
        """Retornar el número de factura"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.NumeroFactura

    @property
    def tipus_factura(self):
        """Retornar el tipus de factura"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.TipoFactura

    @property
    def tipus_rectificadora(self):
        """Retornar el tipus de rectificadora"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.IndicativoFacturaRectificadora

    @property
    def data_factura(self):
        """Retornar el tipus de factura"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.FechaFactura

    @property
    def CIF_emisora(self):
        """Retornar el CIF"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.CIFEmisora

    @property
    def observacions(self):
        """Retornar les observacions"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.Observaciones

    @property
    def import_total_factura(self):
        """Retornar l'import total"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.ImporteTotalFactura

    @property
    def import_iva(self):
        """Retorna l'IVA"""
        return self.factura.IVA.Importe

    @property
    def import_net(self):
        """Retorna el total sense iva"""
        return self.factura.IVA.BaseImponible

    @property
    def saldo_factura(self):
        """Retornar el saldo"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.SaldoFactura

    @property
    def saldo_cobrament(self):
        """Retornar el cobrament"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.SaldoCobro

    @property
    def tipus_facturacio(self):
        """Retornar el tipus de facturacio"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.TipoFacturacion

    @property
    def data_BOE(self):
        """Retornar la data del BOE
           També serveix per saber quines tarifes de preus aplicar
        """
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.FechaBOE

    @property
    def codi_tarifa(self):
        """Retornar el codi ocsum de la tarifa"""
        return str(self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.CodigoTarifa).zfill(3)

    @property
    def ind_mesura_baixa(self):
        """Retornar l'indicador de mesura en baixa"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.IndAltamedidoenBaja

    @property
    def data_inici(self):
        """Retornar la data d'inici"""
        return str(self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaDesdeFactura)

    @property
    def data_final(self):
        """Retornar la data final"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaHastaFactura

    @property
    def nombre_mesos(self):
        """Retornar el nombre de mesos"""
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.NumeroMeses

    def get_linies_factura(self):
        """Retorna una llista de llistes de línies de factura"""
        noms_funcio = {'Potencia': [self.get_info_potencia, 'potencia'],
                       'EnergiaActiva': [self.get_info_activa, 'energia'],
                       'EnergiaReactiva': [self.get_info_reactiva,
                                                                  'reactiva'],
                       'Alquileres': [self.get_info_lloguers, 'lloguer']}
        contingut = []
        tipus = self.factura.getchildren()
        for i in tipus:
            key = i.tag[i.tag.find('}') + 1:]
            if key in noms_funcio.keys():
                pobj = LiniesFactura(noms_funcio[key][0](), noms_funcio[key][1])
                contingut.append(pobj)
        return contingut

    # Periodes d'energia
    def get_info_activa(self):
        periode = []
        ch = self.factura.EnergiaActiva.TerminoEnergiaActiva.getchildren()
        periode = [PeriodeActiva(i) for i in ch if 'Periodo' in i.tag]
        return periode

    def get_info_reactiva(self):
        periode = []
        ch = self.factura.EnergiaReactiva.TerminoEnergiaReactiva.getchildren()
        periode = [PeriodeReactiva(i) for i in ch if 'Periodo' in i.tag]
        return periode

    # Periodes de potència
    def get_info_potencia(self):
        periode = []
        ch = self.factura.Potencia.TerminoPotencia.getchildren()
        periode = [PeriodePotencia(i) for i in ch if 'Periodo' in i.tag]
        return periode

    # Línies de lloguers
    def get_info_lloguers(self):
        pass

    @property
    def pot_data_inici(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaDesde

    @property
    def pot_data_fi(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaHasta

    # Lectures
    def get_lectures(self):
        lectures = []
        for lect in self.factura.Medidas.Aparato.getchildren():
            if 'Integrador' in lect.tag:
                lectures.append(Lectura(lect, self.codi_tarifa)) 

        tipus = ''
        for lect in lectures:
            if tipus != lect.tipus:
                cnt = 0
                tipus = lect.tipus
            else:
                cnt += 1
            lect.cnt = cnt
        return lectures

    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.factura.Medidas.Aparato.NumeroSerie.text

    @property
    def gir_comptador(self):
        return (10 ** self.factura.Medidas.Aparato.\
               Integrador.NumeroRuedasEnteras)


class LiniesFactura(object):
    def __init__(self, data, tipus):
        self.data = data
        self._tipus = tipus

    @property
    def tipus(self):
        return self._tipus

    def get_data(self):
        return self.data


class PeriodeActiva(object):

    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        "Retorna kwh"
        return float(str(self.periode.ValorEnergiaActiva))


class PeriodeReactiva(object):

    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        return float(str(self.periode.ValorEnergiaReactiva))


class PeriodePotencia(object):

    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        "Retorna kw"
        return float(str(self.periode.PotenciaAFacturar)) / 1000


class Lectura(object):

    def __init__(self, lect, tarifa):
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
                 'PM': 'M'}
        return tipus.get(self.lectura.Magnitud)

    @property
    def periode(self):
        # taula 42
        relacio = {'004': {'01': 'P1', '03': 'P2'},
                   '006': {'01': 'P1', '03': 'P2'},
                   '001': {'10': 'P1'},
                   '005': {'10': 'P1'},
                   '003': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'},
                   '011': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'},
                   '012': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'},
                   '013': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'},
                   '014': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'},
                   '015': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'},
                   '016': {'61': 'P1', '62': 'P2', '63': 'P3', 
                           '64': 'P4', '65': 'P5', '66': 'P6'}}

        periode = str(self.lectura.CodigoPeriodo)
        return relacio[self.tarifa][periode]

    @property
    def constant_multiplicadora(self):
        return self.lectura.ConstanteMultiplicadora

    @property
    def data_lectura_inicial(self):
        data = str(self.lectura.LecturaDesde.FechaHora)
        return data[0:data.find('T')]

    @property
    def data_lectura_final(self):
        data = str(self.lectura.LecturaHasta.FechaHora)
        return data[0:data.find('T')]

    @property
    def valor_lectura_inicial(self):
        return self.lectura.LecturaDesde.Lectura

    @property
    def valor_lectura_final(self):
        return self.lectura.LecturaHasta.Lectura

    @property
    def origen_lectura_inicial(self):
        return self.lectura.LecturaDesde.Procedencia

    @property
    def origen_lectura_final(self):
        return self.lectura.LecturaHasta.Procedencia
