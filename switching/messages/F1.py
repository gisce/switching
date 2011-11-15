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
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaDesdeFactura

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

    # Línies de potència
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


class Lectura(object):
    
    def __init__(self, lect, tarifa):
        self.lectura = lect
        self.tarifa = tarifa

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
                 'PM': 'M' }
        return tipus.get(self.lectura.Magnitud)

    @property
    def periode(self):
        # taula 42
        relacio = { '004' : {'01' : 'P1', '03' : 'P2'},
                    '006' : {'01' : 'P1', '03' : 'P2'},
                    '001' : {'10' : 'P1'},
                    '005' : {'10' : 'P1'},
                    '003' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'},
                    '011' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'},
                    '012' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'},
                    '013' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'},
                    '014' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'},
                    '015' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'},
                    '016' : {'61' : 'P1', '62' : 'P2', '63' : 'P3', 
                             '64' : 'P4', '65' : 'P5'}}
        
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
        return self.lectura.LecturaHasta.Lectura
        
    @property
    def valor_lectura_final(self):
        return self.lectura.LecturaDesde.Lectura

    @property
    def origen_lectura_inicial(self):
        return self.lectura.LecturaDesde.Procedencia
    
    @property
    def origen_lectura_final(self):
        return self.lectura.LecturaHasta.Procedencia


