# -*- coding: utf-8 -*-

from message import Message


class F1(Message):
    """Classe que implementa F1."""

    @property
    def get_num_factures(self):
        ch = self.obj.Facturas.getchildren()
        nelem = 0
        for i in range(len(ch)):
            if 'FacturaATR' in ch[i].tag: 
                nelem += 1
        return nelem

    def get_factura(self, fact):
        return Factura(self.obj.Facturas.FacturaATR[fact])

    @property
    def data_limit_pagament(self):
        return self.obj.Facturas.RegistroFin.FechaLimitePago


class Factura(object):

    def __init__(self, fact):
        self.factura = fact

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
        return self.factura.DatosGeneralesFacturaATR.\
               DatosFacturaATR.CodigoTarifa

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

    # Línies de factura
    @property
    def pot_data_inici(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaDesde

    @property
    def pot_data_fi(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaHasta

    @property
    def nom_comptador(self):
        """Retorna el número de comptador"""
        return self.factura.Medidas.Aparato.NumeroSerie.text

    @property
    def gir_comptador(self):
        return (10 ** self.factura.Medidas.Aparato.\
               Integrador.NumeroRuedasEnteras)
