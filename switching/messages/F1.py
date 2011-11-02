# -*- coding: utf-8 -*-

from message import Message


class F1(Message):
    """Classe que implementa F1."""

    @property
    def cups(self):
        """Retornar el CUPS"""
        return self.obj.Cabecera.Codigo

    @property
    def numero_factura(self):
        """Retornar el número de factura"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.NumeroFactura

    @property
    def tipus_factura(self):
        """Retornar el tipus de factura"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.TipoFactura

    @property
    def tipus_rectificadora(self):
        """Retornar el tipus de rectificadora"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.IndicativoFacturaRectificadora

    @property
    def data_factura(self):
        """Retornar el tipus de factura"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.FechaFactura

    @property
    def CIF_emisora(self):
        """Retornar el CIF"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.CIFEmisora

    @property
    def codi_fiscal_factura(self):
        """Retornar el codi fiscal de la factura"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.CodigoFiscalFactura

    @property
    def observacions(self):
        """Retornar les observacions"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.Observaciones

    @property
    def import_total_factura(self):
        """Retornar l'import total"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.ImporteTotalFactura

    @property
    def saldo_factura(self):
        """Retornar el saldo"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.SaldoFactura

    @property
    def saldo_cobrament(self):
        """Retornar el cobrament"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosGeneralesFactura.SaldoCobro

    @property
    def tipus_facturacio(self):
        """Retornar el tipus de facturacio"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.TipoFacturacion

    @property
    def data_BOE(self):
        """Retornar la data del BOE
           També serveix per saber quines tarifes de preus aplicar
        """
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.FechaBOE

    @property
    def codi_tarifa(self):
        """Retornar el codi ocsum de la tarifa"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.CodigoTarifa

    @property
    def ind_mesura_baixa(self):
        """Retornar l'indicador de mesura en baixa"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.IndAltamedidoenBaja

    @property
    def data_inici(self):
        """Retornar la data d'inici"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaDesdeFactura

    @property
    def data_final(self):
        """Retornar la data final"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.FechaHastaFactura

    @property
    def nombre_mesos(self):
        """Retornar el nombre de mesos"""
        return self.obj.Facturas.FacturaATR.DatosGeneralesFacturaATR.\
               DatosFacturaATR.Periodo.NumeroMeses

    # Línies de factura

    @property
    def pot_data_inici(self):
        return self.obj.Facturas.FacturaATR.Potencia.TerminoPotencia.\
               FechaDesde

    @property
    def pot_data_fi(self):
        return self.obj.Facturas.FacturaATR.Potencia.TerminoPotencia.\
               FechaHasta
