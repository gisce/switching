# -*- coding: utf-8 -*-

import gettext

from defs import *
from message import Message, except_f1

from Q1 import Q1, Lectura, Comptador
from switching.helpers.funcions import (
    CODIS_REG_REFACT, exces_reactiva, aggr_consums
)

_ = gettext.gettext


def get_rec_attr(obj, attr, default=None):
    try:
        res = reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        if not default is None:
            res = default
        else:
            raise
    return res


class Facturas(object):

    def __init__(self, fact):
        self.factura = fact
        self.mapa_linies_factura = {
            'ConceptoIVA': [self.get_info_conceptes_iva, 'altres']
        }

    @property
    def tipus(self):
        return self.__class__.__name__

    @property
    def _dades_generals(self):
        path = 'DatosGenerales%s' % self.tipus
        return getattr(self.factura, path)

    # Dades generals
    @property
    def cups(self):
        """Retornar el CUPS"""
        return self._dades_generals.DireccionSuministro.CUPS.text

    @property
    def get_codi(self):
        return self.cups

    @property
    def numero_factura(self):
        """Retornar el número de factura"""
        return self._dades_generals.DatosGeneralesFactura.NumeroFactura.text

    @property
    def tipus_factura(self):
        """Retornar el tipus de factura"""
        return self._dades_generals.DatosGeneralesFactura.TipoFactura.text

    @property
    def tipus_rectificadora(self):
        """Retornar el tipus de rectificadora"""
        return self._dades_generals.DatosGeneralesFactura\
            .IndicativoFacturaRectificadora.text

    @property
    def factura_rectificada(self):
        """Retorna el número de factura rectificada.
        """
        return self._dades_generals.DatosGeneralesFactura\
            .NumeroFacturaRectificada.text

    @property
    def data_factura(self):
        """Retornar el tipus de factura"""
        return self._dades_generals.DatosGeneralesFactura.FechaFactura.text

    @property
    def CIF_emisora(self):
        """Retornar el CIF"""
        return self._dades_generals.DatosGeneralesFactura.CIFEmisora.text

    @property
    def observacions(self):
        """Retornar les observacions"""
        return self._dades_generals.DatosGeneralesFactura.Observaciones.text

    @property
    def import_total_factura(self):
        """Retornar l'import total"""
        return float(self._dades_generals.DatosGeneralesFactura\
            .ImporteTotalFactura.text)

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
        return float(self._dades_generals.DatosGeneralesFactura\
                        .SaldoFactura.text)

    @property
    def saldo_cobrament(self):
        """Retornar el cobrament"""
        return float(self._dades_generals\
                       .DatosGeneralesFactura.SaldoCobro.text)

    def get_linies_factura(self):
        """Retorna una llista de llistes de LiniesFactura"""
        contingut = []
        noms_funcio = self.mapa_linies_factura
        for key in noms_funcio:
            try:
                test = list(getattr(self.factura, key))
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

    def get_info_conceptes_iva(self):
        conceptes = []
        total = 0
        for concepte in list(self.factura.ConceptoIVA):
            c = ConcepteIVA(concepte)
            # Si és una regularització refacturació 40, 41 i 42 el valor
            # només pot ser negatiu.
            # Es comprova ja que hi ha empreses que envien la refacturació
            # i també el ConceptoIVA i s'importaria dues vegades.
            if c.codi in CODIS_REG_REFACT.values() and c.total >= 0:
                continue
            elif c.total:
                total += c.total
                conceptes.append(c)
        return conceptes, total


class OtrasFacturas(Facturas):

    def __init__(self, fact):
        super(OtrasFacturas, self).__init__(fact)
        self.mapa_linies_factura.update({
            'Concepto': [self.get_info_conceptes, 'altres'],
        })

    def get_info_conceptes(self):
        conceptes = []
        total = 0
        for concepte in list(self.factura.Concepto):
            c = Concepte(concepte)
            total += c.total
            conceptes.append(c)
        return conceptes, total


class FacturaATR(Facturas):

    def __init__(self, fact):
        super(FacturaATR, self).__init__(fact)
        self.mapa_linies_factura.update({
            'Potencia': [self.get_info_potencia, 'potencia'],
            'EnergiaActiva': [self.get_info_activa, 'energia'],
            'EnergiaReactiva': [self.get_info_reactiva, 'reactiva'],
            'Alquileres': [self.get_info_lloguers, 'lloguer'],
            'ExcesoPotencia': [self.get_info_exces, 'exces_potencia'],
            'Refacturaciones': [self.get_info_refacturacions,
                                'refacturacions'],
        })

    @property
    def contracte_distri(self):
        """Retornar el tipus de facturacio"""
        return self.factura.DatosGeneralesFacturaATR.Contrato.text

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

    def get_info_activa(self):
        """Retornat els periodes d'energia"""
        periode = []
        total = 0
        lectures = []
        for i in self.get_comptadors():
            lectures.extend(i.get_lectures())
        lect_activa = self.select_consum_from_lectures(lectures, 'A')
        lect_activa = aggr_consums(lect_activa)
        try:
            for ea in self.factura.EnergiaActiva.TerminoEnergiaActiva:
                d_ini = ea.FechaDesde.text
                d_fi = ea.FechaHasta.text
                p = 0
                for i in ea.Periodo:
                    if float(i.PrecioEnergia.text):
                        p += 1
                        nom_p = 'P%d' % p
                        val = float(i.ValorEnergiaActiva.text)
                        if val in lect_activa.values():
                            per = [k for k in lect_activa if
                                                        lect_activa[k] == val]
                            if len(per) == 1:
                                nom_p = per[0]
                        periode.append(PeriodeActiva(i, nom_p, d_ini, d_fi))
                        if nom_p in lect_activa:
                            del lect_activa[nom_p]
            total = float(self.factura.EnergiaActiva.
                                            ImporteTotalEnergiaActiva.text)
        except AttributeError:
            pass
        return periode, total

    def get_periodes_reactiva(self, lectures):
        """Retorna una llista de noms de periode que tenen excés de reactiva
        """
        agrupat = INFO_TARIFA[self.codi_tarifa]['agrupat']
        lect_activa = self.select_consum_from_lectures(lectures, 'A')
        lect_reactiva = self.select_consum_from_lectures(lectures, 'R')
        if len(lect_activa) < len(lect_reactiva):
            msg = _('Menor nombre de periodes en les lectures d\'activa '\
                    'que en reactiva. No és possible calcular els excessos '\
                    'de reactiva.')
            raise except_f1('Error', msg)
        if agrupat:
            lect_activa = aggr_consums(lect_activa)
            lect_reactiva = aggr_consums(lect_reactiva)
        periodes = lect_reactiva.keys()
        periodes.sort()
        calc = {}
        marge = INFO_TARIFA[self.codi_tarifa]['marge']
        try:
            for i in periodes:
                activa = lect_activa[i]
                reactiva = lect_reactiva[i]
                val = float("%.2f" % exces_reactiva(activa, reactiva, marge))
                # Comprovem que hi ha accés de reactiva i que el període en
                # el que estem es pot facturar la reactiva
                if val > 0 and i in INFO_TARIFA[self.codi_tarifa]['reactiva']:
                    calc[i] = val
            return calc
        except KeyError, e:
            msg = _('No s\'ha trobat el periode \'%s\' en les lectures '\
                    ' d\'activa') % e[0]
            raise except_f1('Error', msg)

    def find_terme_periode_reactiva(self, reactiva_dict, done_list,
                                    aprox=0):
        periodes = []
        for er in self.factura.EnergiaReactiva.TerminoEnergiaReactiva:
            d_ini = er.FechaDesde.text
            d_fi = er.FechaHasta.text
            for tp_er in er.Periodo:
                # Per ordre intentem buscar els que casen segons
                # el valor d'energia reactiva facturada
                for p_name in reactiva_dict:
                    value = reactiva_dict[p_name]
                    if p_name in done_list:
                        continue
                    # Busquem amb un llindar de +/- 1 ja que hi ha empreses
                    # que arrodoneixen cap a munt i altres agafen només
                    # la part entera.
                    if (value - aprox
                            <= float(tp_er.ValorEnergiaReactiva.pyval)
                                <= value + aprox):
                        pr = PeriodeReactiva(tp_er, p_name, d_ini, d_fi)
                        done_list.append(p_name)
                        periodes.append(pr)
        return periodes

    def find_unic_terme_periode_reactiva(self, reactiva_dict):
        periodes = []
        for er in self.factura.EnergiaReactiva.TerminoEnergiaReactiva:
            d_ini = er.FechaDesde.text
            d_fi = er.FechaHasta.text
            for tp_er in er.Periodo:
                p_name = reactiva_dict.keys()[0]
                pr = PeriodeReactiva(tp_er, p_name, d_ini, d_fi)
                if not periodes or pr.quantitat > periodes[0].quantitat:
                    periodes = [pr]
        return periodes

    def get_info_reactiva(self):
        """Retorna els periodes de reactiva"""
        comptadors = self.get_comptadors()
        total = 0
        periodes = []
        nom_periodes_uniq = []
        done = []
        consums = {}
        for i in comptadors:
            lectures = i.get_lectures()
            # Fem un diccionari pels consums ja que UNION FENOSA no posene
            # l'excés de reactiva en el valor del terme sino que hi posen
            # el consum. Per detectar quin període és primer ho fem segons
            # l'excés i si no el troba ho buscarem pel consum
            consums_no_agg = self.select_consum_from_lectures(lectures, 'R')
            for p, c in aggr_consums(consums_no_agg).items():
                consums.setdefault(p, 0)
                consums[p] += c

            nom_periodes = self.get_periodes_reactiva(lectures)
            if nom_periodes_uniq:
                nom_periodes_uniq = list(set(nom_periodes_uniq
                                             + nom_periodes.keys()))
            else:
                nom_periodes_uniq = list(nom_periodes.keys())
        nom_periodes_uniq.sort()
        if not nom_periodes_uniq:
            return None, None
        try:
            # Primer busquem per exces de reactiva
            periodes += self.find_terme_periode_reactiva(nom_periodes, done, 1)
            # Eliminem tots els períodes que ja hem identificat del diccionari
            # de consums
            for p in set(done):
                if p in consums:
                    del consums[p]
            if consums:
                for p in consums.keys():
                    if p not in INFO_TARIFA[self.codi_tarifa]['reactiva']:
                        del consums[p]
                periodes += self.find_terme_periode_reactiva(consums, done, 0)
                # treiem els periodes que no tenen excés de reactiva
                for p in consums.keys():
                    if p not in nom_periodes_uniq:
                        del consums[p]
                falten = sorted(set(consums.keys()) - set(done))
                if falten:
                    # Si només tenim un període de reactiva i no l'hem trobat,
                    # agafem el que tingui més "consum"
                    if len(INFO_TARIFA[self.codi_tarifa]['reactiva']) == 1:
                        peri = self.find_unic_terme_periode_reactiva(consums)
                        periodes += peri
                    if not periodes:
                        raise Exception(
                            _("No s'ha pogut identificar tots els períodes de "
                              "reactiva per facturar: %s") % ', '.join(falten)
                             )

            total = float(self.factura.EnergiaReactiva.\
                             ImporteTotalEnergiaReactiva.text)
        except AttributeError:
            pass
        return periodes, total

    def get_info_potencia(self):
        """Retorna els periodes de potència"""
        periode = []
        total = 0
        try:
            for pot in self.factura.Potencia.TerminoPotencia:
                d_ini = pot.FechaDesde.text
                d_fi = pot.FechaHasta.text
                p = 0
                for i in pot.Periodo:
                    if float(i.PrecioPotencia.text):
                        p += 1
                        periode.append(PeriodePotencia(i, 'P%d' % p,
                                                            d_ini, d_fi))
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
                if float(i.ValorExcesoPotencia.text):
                    p += 1
                    periode.append(PeriodeExces(i, 'P%d' % p,
                                                self.data_inici,
                                                self.data_final))
            total = float(self.factura.ExcesoPotencia.ImporteTotalExcesos.text)
        except AttributeError:
            pass
        return periode, total

    def get_info_lloguers(self):
        """Línies de lloguers"""
        try:
            obj = Lloguer(self.factura.Alquileres.
                          ImporteFacturacionAlquileres.text,
                          self.data_inici, self.data_final)
        except AttributeError:
            obj = ''
        return obj

    def get_parcials_refacturacio(self):
        """Parcials de refacturacio"""
        parcial = {}
        for val in self.factura.ConceptoIVA:
            try:
                tipus = val.Concepto.text
            except AttributeError:
                continue
            if not tipus in parcial:
                parcial.update({tipus: float(val.ImporteConceptoIVA.text)})
            else:
                msg = _(u'Existeix més d\'un valor de refacturació parcial '
                        u'(ConceptoIVA) amb tipus %s.') % tipus
                raise except_f1('Error', msg)
        return parcial

    def get_info_refacturacions(self):
        """Linies de refacturació"""
        refact = []
        total = 0
        if hasattr(self.factura, 'Refacturaciones'):
            parcial = self.get_parcials_refacturacio()
            for ref in self.factura.Refacturaciones.Refacturacion:
                try:
                    _ref = Refacturacio(ref, parcial)
                except except_f1:
                    continue
                refact.append(_ref)
                total += _ref.import_total
        return refact, total

    @property
    def pot_data_inici(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaDesde.text

    @property
    def pot_data_fi(self):
        return self.factura.Potencia.TerminoPotencia.\
               FechaHasta.text

    def get_comptadors(self):
        """Retorna totes les lectures en una llista de comptadors"""
        return Q1._get_comptadors(self, self.factura)

    def select_from_lectures(self, lectures, tipus):
        """Retorna les lectures d'energia del tipus indicat"""
        select = {}
        for lect in lectures:
            if lect.tipus in tipus:
                select.update({lect.periode: lect})
        return select

    def select_consum_from_lectures(self, lectures, tipus):
        """Retorna els consums de lectures d'energia del tipus indicat
           En el cas d'haver-hi múltiples lectures del mateix tipus i 
           periode, n'acomula els consums"""
        select = {}
        for lect in lectures:
            if lect.tipus in tipus:
                if lect.periode in select:
                    select[lect.periode] += lect.consum
                else:
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

    def __init__(self, periode, name, data_inici, data_final):
        self.periode = periode
        self._name = name
        self._data_inici = data_inici
        self._data_final = data_final

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

    @property
    def data_inici(self):
        return self._data_inici

    @property
    def data_final(self):
        return self._data_final


class PeriodeReactiva(object):

    def __init__(self, periode, name, data_inici, data_final):
        self.periode = periode
        self._name = name
        self._data_inici = data_inici
        self._data_final = data_final

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

    @property
    def data_inici(self):
        return self._data_inici

    @property
    def data_final(self):
        return self._data_final


class PeriodePotencia(object):

    def __init__(self, periode, name, data_inici, data_final):
        self.periode = periode
        self._name = name
        self._data_inici = data_inici
        self._data_final = data_final

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

    @property
    def data_inici(self):
        return self._data_inici

    @property
    def data_final(self):
        return self._data_final


class PeriodeExces(object):
    def __init__(self, periode, name, data_inici, data_final):
        self.periode = periode
        self._name = name
        self._data_inici = data_inici
        self._data_final = data_final

    @property
    def quantitat(self):
        "Retorna kw"
        return float(self.periode.ValorExcesoPotencia.text)

    @property
    def name(self):
        "Retorna el nom del periode"
        return self._name

    @property
    def data_inici(self):
        return self._data_inici

    @property
    def data_final(self):
        return self._data_final


class Lloguer(object):
    def __init__(self, cost, data_inici, data_final):
        self.cost = cost
        self._data_inici = data_inici
        self._data_final = data_final

    @property
    def quantitat(self):
        return float(self.cost)

    @property
    def data_inici(self):
        return self._data_inici

    @property
    def data_final(self):
        return self._data_final


class Refacturacio(object):
    """Classe amb la informació de refacturació"""
    def __init__(self, ref, parcial):
        self.ref = ref
        self._import_parcial = parcial.get(self.ref.Tipo.text, False)
        if not self._import_parcial:
            msg = _(u'No s\'ha trobat el valor de refacturació parcial '
                    u'(ConceptoIVA) amb tipus %s.') % self.ref.Tipo.text
            raise except_f1('Error', msg)

    @property
    def tipus(self):
        return self.ref.Tipo.text

    @property
    def data_inici(self):
        return self.ref.RFechaDesde.text

    @property
    def data_final(self):
        return self.ref.RFechaHasta.text

    @property
    def consum_total(self):
        return float(self.ref.RConsumo.text)

    @property
    def import_total(self):
        return float(self.ref.ImporteTotal.text)

    @property
    def import_parcial(self):
        return self._import_parcial


class RegRefact(object):
    """Classe amb la informació de regularització de refacturació"""
    def __init__(self, tipus, val, d_ini, d_fi):
        self._tipus = tipus
        self._import = val
        self._d_ini = d_ini
        self._d_fi = d_fi

    @property
    def tipus(self):
        return self._tipus

    @property
    def import_parcial(self):
        return self._import

    @property
    def data_inici(self):
        return self._d_fi

    @property
    def data_final(self):
        return self._d_ini


class ConcepteIVA(object):
    def __init__(self, concepte_iva):
        self.concepte_iva = concepte_iva
        self.tipus = 'altres'
        self.quantitat = 1
        self.total = self.preu

    @property
    def codi(self):
        return get_rec_attr(self.concepte_iva, 'Concepto.text')

    @property
    def preu(self):
        return float(
            get_rec_attr(self.concepte_iva, 'ImporteConceptoIVA.text', 0)
        )



class Concepte(object):
    def __init__(self, concepte):
        self.concepte = concepte
        self.tipus = 'altres'

    @property
    def codi(self):
        return get_rec_attr(self.concepte, 'TipoConcepto.text')

    @property
    def quantitat(self):
        return float(get_rec_attr(self.concepte, 'UnidadesConcepto.text', 1))

    @property
    def preu(self):
        return float(
            get_rec_attr(self.concepte, 'ImporteUnidadConcepto.text', 0)
        )

    @property
    def total(self):
        return float(
            get_rec_attr(self.concepte, 'ImporteTotalConcepto.text', 0)
        )


class F1(Message):
    """Classe que implementa F1."""

    tipus_factures = {
        'FacturaATR': FacturaATR,
        'OtrasFacturas': OtrasFacturas
    }

    @property
    def num_factures(self):
        nelem = {}
        for tipus in self.tipus_factures:
            nelem.setdefault(tipus, 0)
            try:
                factures = getattr(self.obj.Facturas, tipus)
                nelem[tipus] = len(list(factures))
            except AttributeError:
                pass
        return nelem

    def get_factures(self):
        fact = {}
        for tipus in self.tipus_factures:
            fact.setdefault(tipus, [])
            try:
                for ch in getattr(self.obj.Facturas, tipus):
                    fact[tipus].append(self.tipus_factures[tipus](ch))
            except AttributeError:
                pass
        return fact

    @property
    def data_limit_pagament(self):
        return self.obj.Facturas.RegistroFin.FechaLimitePago.text
