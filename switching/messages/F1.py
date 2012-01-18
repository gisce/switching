# -*- coding: utf-8 -*-

from message import Message, except_f1


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
    def get_codi_emisor(self):
        ref = self.obj.Cabecera.CodigoREEEmpresaEmisora.text
        if not ref:
            raise except_f1('Error', _('Document sense emisor'))
        return '%04d' % ref

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
        return int(self.factura.DatosGeneralesFacturaATR.\
                   DatosFacturaATR.TipoFacturacion.text)

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
        return factura.DatosGeneralesFacturaATR.\
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
        return int(self.factura.DatosGeneralesFacturaATR.\
                    DatosFacturaATR.Periodo.NumeroMeses.text)

    def get_linies_factura(self):
        """Retorna una llista de llistes de línies de factura"""
        noms_funcio = {'Potencia': [self.get_info_potencia, 'potencia'],
                       'EnergiaActiva': [self.get_info_activa, 'energia'],
                       'EnergiaReactiva': [self.get_info_reactiva,
                                                                  'reactiva'],
                       'Alquileres': [self.get_info_lloguers, 'lloguer'],
                       'ExcesoPotencia': [self.get_info_exces,
                                                             'exces_potencia']}
        contingut = []
        tipus = self.factura.getchildren()
        for i in tipus:
            key = i.tag[i.tag.find('}') + 1:]
            if key in noms_funcio.keys():
                if key == 'Alquileres':
                    data = noms_funcio[key][0]()
                    pobj = LiniesFactura(data, noms_funcio[key][1])
                else:
                    data, total = noms_funcio[key][0]()
                    pobj = LiniesFactura(data, noms_funcio[key][1], total)
                contingut.append(pobj)
        return contingut

    def get_info_activa(self):
        """Retornat els periodes d'energia"""
        periode = []
        total = 0
        ch = self.factura.EnergiaActiva.TerminoEnergiaActiva.getchildren()
        for i in ch:
            if 'Periodo' in i.tag:
                periode.append(PeriodeActiva(i))
        total = float(self.factura.EnergiaActiva.ImporteTotalEnergiaActiva.text)
        return periode, total

    def get_info_reactiva(self):
        """Retorna els periodes de reactiva"""
        periode = []
        total = 0
        ch = self.factura.EnergiaReactiva.TerminoEnergiaReactiva.getchildren()
        for i in ch:
            if 'Periodo' in i.tag:
                periode.append(PeriodeReactiva(i))
        total = float(self.factura.EnergiaReactiva.\
                         ImporteTotalEnergiaReactiva.text)
        return periode, total

    def get_info_potencia(self):
        """Retorna els periodes de potència"""
        periode = []
        total = 0
        ch = self.factura.Potencia.TerminoPotencia.getchildren()
        for i in ch:
            if 'Periodo' in i.tag:
                periode.append(PeriodePotencia(i))
        total = float(self.factura.Potencia.ImporteTotalTerminoPotencia.text)
        return periode, total

    def get_info_exces(self):
        """Retorna els periodes d'excessos de potència"""
        periode = []
        total = 0
        ch = self.factura.ExcesoPotencia.getchildren()
        for i in ch:
            if 'Periodo' in i.tag:
                periode.append(PeriodeExces(i))
            elif 'ImporteTotal' in i.tag:
                total = float(str(i))
        return periode, total

    def get_info_lloguers(self):
        """Línies de lloguers"""
        obj = Lloguer(self.factura.Alquileres.ImporteFacturacionAlquileres.text)
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
        """Retorna totes les lectures"""
        lectures = []
        for lect in self.factura.Medidas.Aparato.getchildren():
            if 'Integrador' in lect.tag:
                lectures.append(Lectura(lect, self.codi_tarifa)) 

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

    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        "Retorna kwh"
        return float(self.periode.ValorEnergiaActiva.text)

    @property
    def preu_unitat(self):
        "Retorna el preu de l'energia activa"
        return float(self.periode.PrecioEnergia.text)

class PeriodeReactiva(object):

    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        return float(self.periode.ValorEnergiaReactiva.text)

    @property
    def preu_unitat(self):
        "Retorna el preu de l'energia reactiva"
        return float(self.periode.PrecioEnergiaReactiva.text)

class PeriodePotencia(object):

    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        "Retorna kw"
        return float(self.periode.PotenciaAFacturar.text) / 1000

    @property
    def maximetre(self):
        "Retorna la potència màxima demanada"
        return float(self.periode.PotenciaMaxDemandada.text) / 1000

    @property
    def preu_unitat(self):
        "Retorna el preu del kw"
        return float(self.periode.PrecioPotencia.text) * 1000

class PeriodeExces(object):
    def __init__(self, periode):
        self.periode = periode

    @property
    def quantitat(self):
        "Retorna kw"
        return float(self.periode.ValorExcesoPotencia.text) / 1000

class Lloguer(object):
    def __init__(self, cost):
        self.cost = cost
    
    @property
    def quantitat(self):
        return float(self.cost)
    
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
                 'PM': 'M',
                 'EP': 'EP'}
        return tipus.get(self.lectura.Magnitud.text)

    @property 
    def magnitud(self):
        return self.lectura.Magnitud.text

    @property
    def consum(self):
        return int(self.lectura.ConsumoCalculado.text)

    @property
    def periode(self):
        # taula 42
        relacio = {'01': 'P1',
                   '03': 'P2',
                   '10': 'P1',
                   '61': 'P1',
                   '62': 'P2',
                   '63': 'P3',
                   '64': 'P4',
                   '65': 'P5',
                   '66': 'P6'}

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
        return int(self.lectura.LecturaDesde.Lectura.text)

    @property
    def valor_lectura_final(self):
        return int(self.lectura.LecturaHasta.Lectura.text)

    @property
    def origen_lectura_inicial(self):
        return self.lectura.LecturaDesde.Procedencia.text

    @property
    def origen_lectura_final(self):
        return self.lectura.LecturaHasta.Procedencia.text
