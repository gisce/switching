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

    def cups(self, elem):
        """Retornar el CUPS"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DireccionSuministro.CUPS

    def numero_factura(self, elem):
        """Retornar el número de factura"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.NumeroFactura

    def tipus_factura(self, elem):
        """Retornar el tipus de factura"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.TipoFactura

    def tipus_rectificadora(self, elem):
        """Retornar el tipus de rectificadora"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.IndicativoFacturaRectificadora

    def data_factura(self, elem):
        """Retornar el tipus de factura"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.FechaFactura

    def CIF_emisora(self, elem):
        """Retornar el CIF"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.CIFEmisora

    def observacions(self, elem):
        """Retornar les observacions"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.Observaciones

    def import_total_factura(self, elem):
        """Retornar l'import total"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.ImporteTotalFactura

    def saldo_factura(self, elem):
        """Retornar el saldo"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.SaldoFactura

    def saldo_cobrament(self, elem):
        """Retornar el cobrament"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.SaldoCobro

    def tipus_facturacio(self, elem):
        """Retornar el tipus de facturacio"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.TipoFacturacion

    def data_BOE(self, elem):
        """Retornar la data del BOE
           També serveix per saber quines tarifes de preus aplicar
        """
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.FechaBOE

    def codi_tarifa(self, elem):
        """Retornar el codi ocsum de la tarifa"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.CodigoTarifa

    def ind_mesura_baixa(self, elem):
        """Retornar l'indicador de mesura en baixa"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.IndAltamedidoenBaja

    def data_inici(self, elem):
        """Retornar la data d'inici"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaDesdeFactura

    def data_final(self, elem):
        """Retornar la data final"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaHastaFactura

    def nombre_mesos(self, elem):
        """Retornar el nombre de mesos"""
        return self.obj.Facturas.FacturaATR[elem].DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.NumeroMeses

    # Línies de factura
    def pot_data_inici(self, elem):
        return self.obj.Facturas.FacturaATR[elem].Potencia.TerminoPotencia.\
               FechaDesde

    def pot_data_fi(self, elem):
        return self.obj.Facturas.FacturaATR[elem].Potencia.TerminoPotencia.\
               FechaHasta

    def nom_comptador(self, elem):
        """Retorna el número de comptador"""
        return self.obj.Facturas.FacturaATR[elem].Medidas.Aparato.\
               NumeroSerie.text

    def gir_comptador(self, elem):
        return (10 ** self.obj.Facturas.FacturaATR[elem].Medidas.Aparato.\
               Integrador.NumeroRuedasEnteras)

    @property
    def data_limit_pagament(self):
        return self.obj.Facturas.RegistroFin.FechaLimitePago
