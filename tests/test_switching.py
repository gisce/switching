#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.helpers.funcions import aggr_consums, aggr_ajusts
from switching.input.messages import C1
from switching.input.messages import F1, message, R1, W1, A3, M1, FacturaATR, Q1
from switching.input.messages import C2
from switching.output.messages import sw_w1 as w1
from switching.output.messages import sw_c1 as c1
from switching.output.messages import sw_c2 as c2
from switching.output.messages import sw_m1 as m1
from switching.output.messages import sw_a3 as a3
from switching.output.messages import sw_r1 as r1
from switching.output.messages.base import Cabecera
from . import unittest

from .test_helpers import get_data


class Switching_Helpers_Test(unittest.TestCase):
    """test de switching"""
    def setUp(self):
        self.consums = {'P1': 1, 'P2': 2, 'P3': 4, 'P4': 8, 'P5': 16, 'P6': 32}
        self.consums_aggr = {'P1': 9, 'P2': 18, 'P3': 36}
        self.consums_3p = dict(
            [(k, v) for k, v in self.consums.items() if k in ['P1', 'P2', 'P3']]
        )

    def test_aggr_consums(self):
        self.assertDictEqual(aggr_consums(self.consums), self.consums_aggr)
        self.assertDictEqual(aggr_consums(self.consums_3p), self.consums_3p)

    def test_aggr_ajusts(self):
        self.assertDictEqual(aggr_consums(self.consums), self.consums_aggr)
        self.assertDictEqual(aggr_consums(self.consums_3p), self.consums_3p)


class test_Message_Base(unittest.TestCase):

    def setUp(self):
        self.xml_a301_cabecera = open(get_data("a301.xml"), "r")
        self.xml_r101_reclamacion = open(get_data("r101_minim.xml"), "r")
        self.xml_c201_date_timezone = open(
            get_data("c201_date_timezone.xml"), "r"
        )

    def tearDown(self):
        self.xml_a301_cabecera.close()
        self.xml_r101_reclamacion.close()
        self.xml_c201_date_timezone.close()

    def test_cabecera_model(self):
        c = A3(self.xml_a301_cabecera)
        c.set_xsd()
        c.parse_xml()
        c.set_tipus()
        self.assertEqual(c.tipus, 'A3')
        self.assertEqual(c.pas, '01')
        self.assertEqual(c.get_pas_xml(), '01')
        self.assertEqual(c.get_codi_emisor, '1234')
        self.assertEqual(c.get_codi_destinatari, '4321')
        self.assertEqual(c.get_codi, 'ES1234000000000001JN0F')
        self.assertEqual(c.cups, 'ES1234000000000001JN0F')
        self.assertEqual(c.codi_sollicitud, '201412111009')
        self.assertEqual(c.seq_sollicitud, '01')
        self.assertEqual(c.data_sollicitud, '2014-04-16 22:13:37')
        self.assertEqual(c.versio, '02')

    def test_cabecerareclamacion_model(self):
        c = R1(self.xml_r101_reclamacion)
        c.set_xsd()
        c.parse_xml()
        c.set_tipus()
        self.assertEqual(c.tipus, 'R1')
        self.assertEqual(c.pas, '01')
        self.assertEqual(c.get_pas_xml(), '01')
        self.assertEqual(c.get_codi_emisor, '1234')
        self.assertEqual(c.get_codi_destinatari, '4321')
        self.assertEqual(c.get_codi, 'ES1234000000000001JN0F')
        self.assertEqual(c.cups, 'ES1234000000000001JN0F')
        self.assertEqual(c.codi_sollicitud, '201412111009')
        self.assertEqual(c.seq_sollicitud, '01')
        self.assertEqual(c.data_sollicitud, '2014-04-16 22:13:37')
        with self.assertRaises(message.except_f1) as e:
            c.versio

    def test_cabecera_date_with_timezone(self):
        c = C2(self.xml_c201_date_timezone)
        c.set_xsd()
        c.parse_xml()
        c.set_tipus()
        self.assertEqual(c.tipus, 'C2')
        self.assertEqual(c.pas, '01')
        self.assertEqual(c.get_pas_xml(), '01')
        self.assertEqual(c.get_codi_emisor, '1234')
        self.assertEqual(c.get_codi_destinatari, '4321')
        self.assertEqual(c.get_codi, 'ES1234000000000001JN0F')
        self.assertEqual(c.cups, 'ES1234000000000001JN0F')
        self.assertEqual(c.codi_sollicitud, '201604180065')
        self.assertEqual(c.seq_sollicitud, '01')
        self.assertEqual(c.data_sollicitud, '2016-04-18 00:00:00+01:00')


#@unittest.skip('uncommited data')
class Switching_F1_Test(unittest.TestCase):
    """test de switching"""
    def setUp(self):
        self.xml = open(get_data("F1_exemple.xml"), "r")
        self.xml_err = open(get_data("F1_exemple_err.xml"), "r")
        self.xml_no_medidas = open(get_data("F1_no_medidas.xml"), "r")
        self.xml_remesa = open(get_data("F1_exemple_remesa.xml"), "r")
        self.xml_rnoicp = open(get_data("F1_recarrec_ICP.xml"), "r")
        self.xml_reactivaok = open(get_data("F1_reactiva_ok.xml"), "r")
        self.xml_reactiva1 = open(get_data("F1_reactiva_1.xml"), "r")
        self.xml_reactiva2 = open(get_data("F1_reactiva_2.xml"), "r")
        self.xml_rectificadora = open(get_data("F1_rectificadora.xml"), "r")
        self.xml_conceptoieiva = open(get_data("F1_conceptoieiva.xml"), "r")
        self.xml_conceptoieiva_iva_empty = open(get_data("F1_conceptoieiva_iva_empty.xml"), "r")
        self.xml_ajuste = open(get_data("F1_ajuste.xml"), "r")
        #self.xml_con = open(get_data("F1_concepte_exemple.xml"), "r")

    @unittest.skip("Not implemented yet")
    def test_F1(self):
        f1 = F1(self.xml_con)
        f1.set_xsd()
        tipus = f1.get_tipus_xml()
        f1.parse_xml()
        ch_emisor = '0316'
        emisor = f1.get_codi_emisor
        self.assertEqual(tipus, 'F1')
        self.assertEqual(emisor, ch_emisor)
        f1_atrs = f1.get_factures()['FacturaATR']
        for f1_atr in f1_atrs:
            self.assertEqual(f1_atr.numero_factura, '10005604')

    def test_rectificadora(self):
        f1 = F1(self.xml_rectificadora)
        f1.set_xsd()
        tipus = f1.get_tipus_xml()
        f1.parse_xml()
        ch_emisor = '0123'
        emisor = f1.get_codi_emisor
        self.assertEqual(tipus, 'F1')
        self.assertEqual(emisor, ch_emisor)
        f1_atrs = f1.get_factures()['FacturaATR']
        for f1_atr in f1_atrs:
            self.assertEqual(f1_atr.numero_factura, '20160122100000024')
            self.assertEqual(f1_atr.factura_rectificada, '20150918030012928')
            self.assertEqual(f1_atr.tipus_rectificadora, 'R')

    def test_get_info_activa(self):
        f1 = F1(self.xml)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        periodes, total = f1_atr.get_info_activa()
        periode = periodes[0]
        self.assertEqual(total, 74.1424)
        self.assertEqual(periode.name, 'P1')
        self.assertEqual(periode.data_inici, '2010-03-01')
        self.assertEqual(periode.data_final, '2010-04-30')
        comptadors = f1_atr.get_comptadors()
        assert len(comptadors) == 1
        for comptador in comptadors:
            lectures = comptador.get_lectures()
            # sense ajusts
            for lect in lectures:
                ajust = lect.get_info_ajust()
                assert ajust is None

    def test_get_info_activa_no_medidas(self):
        f1 = F1(self.xml_no_medidas)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        periodes, total = f1_atr.get_info_activa()
        periode = periodes[0]
        self.assertEqual(total, 0.0)
        self.assertEqual(periode.name, 'P1')
        self.assertEqual(periode.data_inici, '2015-08-05')
        self.assertEqual(periode.data_final, '2015-09-03')
        self.assertEqual(f1_atr.gir_comptador, 0)
        self.assertEqual(f1_atr.nom_comptador, '')
        self.assertEqual(Q1._get_comptadors(self, f1_atr), [])

    # reactive
    # nf: invoice_lines
    # nl: measures
    def test_get_info_reactive_1f_1l_ok(self):
        f1 = F1(self.xml_reactivaok)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        periodes, total = f1_atr.get_info_reactiva()
        self.assertEqual(total, 0.83)
        self.assertEqual(len(periodes), 1)
        periode = periodes[0]
        self.assertEqual(periode.name, 'P2')
        self.assertEqual(periode.data_inici, '2016-01-11')
        self.assertEqual(periode.data_final, '2016-02-03')
        self.assertEqual(float(periode.quantitat), 20.0)
        self.assertEqual(float(periode.preu_unitat), 0.041554)

    def test_get_info_reactive_1f_2l(self):
        f1 = F1(self.xml_reactiva1)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        periodes, total = f1_atr.get_info_reactiva()
        self.assertEqual(total, 0.62)
        self.assertEqual(len(periodes), 2)
        self.assertEqual(len(set([p.name for p in periodes])), 2)
        for periode in periodes:
            self.assertIn(periode.name, ['P1', 'P2'])
            self.assertEqual(periode.data_inici, '2015-12-31')
            self.assertEqual(periode.data_final, '2016-01-31')
            self.assertEqual(float(periode.quantitat), 15.0)
            self.assertEqual(float(periode.preu_unitat), 0.041554)

    def test_get_info_reactive_1f_1l_2c(self):
        # Active meter and reactive meter
        f1 = F1(self.xml_reactiva2)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        periodes, total = f1_atr.get_info_reactiva()
        self.assertEqual(total, 6.83)
        self.assertEqual(len(periodes), 1)
        self.assertEqual(len(set([p.name for p in periodes])), 1)
        for periode in periodes:
            self.assertIn(periode.name, ['P1'])
            self.assertEqual(periode.data_inici, '2015-12-02')
            self.assertEqual(periode.data_final, '2016-02-01')
            self.assertEqual(float(periode.quantitat), 164.5)
            self.assertEqual(float(periode.preu_unitat), 0.041554)

    def test_get_info_remesa(self):
        f1 = F1(self.xml_remesa)
        f1.set_xsd()
        f1.parse_xml()
        self.assertEqual(f1.id_remesa, '20151170176')
        self.assertEqual(f1.total_importe_remesa, 42649.66)
        self.assertEqual(f1.total_recibos_remesa, 1015)
        self.assertEqual(f1.fecha_valor_remesa, '2015-11-21')
        self.assertEqual(f1.data_limit_pagament, '2015-12-03')

    def test_get_remesa(self):
        f1 = F1(self.xml_remesa)
        f1.set_xsd()
        f1.parse_xml()
        rem_vals = f1.get_remesa()
        self.assertEqual(rem_vals['id_remesa'], '20151170176')
        self.assertEqual(rem_vals['total_importe_remesa'], 42649.66)
        self.assertEqual(rem_vals['total_recibos_remesa'], 1015)
        self.assertEqual(rem_vals['fecha_valor_remesa'], '2015-11-21')
        self.assertEqual(rem_vals['data_limit_pagament'], '2015-12-03')

    def test_facturacio_potencia_nomodo(self):
        f1 = F1(self.xml)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        mfp_info = f1_atr.info_facturacio_potencia()
        pnicp = f1_atr.penalitzacio_no_icp
        mcp = f1_atr.mode_control_potencia
        self.assertEqual(mcp, '1')
        self.assertEqual(pnicp, 'N')
        self.assertEqual(mfp_info, 'icp')

    def test_facturacio_potencia_modo(self):
        f1 = F1(self.xml_remesa)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        mfp_info = f1_atr.info_facturacio_potencia()
        pnicp = f1_atr.penalitzacio_no_icp
        mcp = f1_atr.mode_control_potencia
        self.assertEqual(mcp, '1')
        self.assertEqual(pnicp, 'N')
        self.assertEqual(mfp_info, 'icp')

    def test_facturacio_recarrec_no_icp(self):
        f1 = F1(self.xml_rnoicp)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        mfp_info = f1_atr.info_facturacio_potencia()
        pnicp = f1_atr.penalitzacio_no_icp
        mcp = f1_atr.mode_control_potencia
        self.assertEqual(mcp, '1')
        self.assertEqual(pnicp, 'S')
        self.assertEqual(mfp_info, 'recarrec')

    def test_facturacio_no_modo_max(self):
        f1 = F1(self.xml_no_medidas)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        mfp_info = f1_atr.info_facturacio_potencia()
        pnicp = f1_atr.penalitzacio_no_icp
        mcp = f1_atr.mode_control_potencia
        self.assertEqual(mcp, '1')
        self.assertEqual(pnicp, 'N')
        self.assertEqual(mfp_info, 'max')

    def test_facturacio_conceptoieiva(self):
        f1 = F1(self.xml_conceptoieiva)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        conceptes = f1_atr.get_info_conceptes_ieiva()
        assert conceptes[1] == -30.05
        assert len(conceptes[0]) == 1
        concepte = conceptes[0][0]
        assert concepte.tipus == 'altres'
        assert concepte.codi == '18'
        assert concepte.total == -30.05

    def test_facturacio_conceptoieiva_empty(self):
        f1 = F1(self.xml_conceptoieiva_iva_empty)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        conceptes, total = f1_atr.get_info_conceptes_ieiva()
        assert len(conceptes) == 0

    def test_facturacio_conceptoiva_empty(self):
        f1 = F1(self.xml_conceptoieiva_iva_empty)
        f1.set_xsd()
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        conceptes, total = f1_atr.get_info_conceptes_iva()
        assert len(conceptes) == 0

    def test_facturacio_ajustes_1(self):
        f1 = F1(self.xml_reactiva1)
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        comptadors = f1_atr.get_comptadors()
        assert len(comptadors) == 1
        comptador = comptadors[0]
        lectures = comptador.get_lectures()
        res_dict = {
            'PM': {'P1': 215, 'P2': 614, 'P3': 467},
            'AE': {'P1': 215, 'P2': 467, 'P3': 614},
            'R1': {'P1': 11, 'P2': 16, 'P3': 15},
        }
        for lect in lectures:
            ajust = lect.get_info_ajust()
            assert ajust['motivo'] == '08'
            assert ajust['ajuste'] == res_dict[lect.magnitud][lect.periode]
        # suport methods tests
        self.assertDictEqual(
            f1_atr.select_ajusts_from_lectures(lectures, 'A'), res_dict['AE']
        )
        self.assertDictEqual(
            f1_atr.select_ajusts_from_lectures(lectures, 'R'), res_dict['R1']
        )
        self.assertDictEqual(
            f1_atr.select_ajusts_from_lectures(lectures, 'M'), res_dict['PM']
        )

    def test_facturacio_ajustes_2(self):
        f1 = F1(self.xml_ajuste)
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        assert isinstance(f1_atr, FacturaATR)
        comptadors = f1_atr.get_comptadors()
        assert len(comptadors) == 1
        comptador = comptadors[0]
        lectures = comptador.get_lectures()
        res_dict = {
            'AE': {'P1': -678, 'P2': 678},
        }
        for lect in lectures:
            ajust = lect.get_info_ajust()
            assert ajust['motivo'] == '99'
            assert ajust['ajuste'] == res_dict[lect.magnitud][lect.periode]

class supportClass(object):
    """Funcions de suport"""
    def getHeader(self, process='C1', step='01'):
        header = Cabecera()
        vals = {
            'proceso': process,
            'paso': step,
            'solicitud': '20141211100908',
            'secuencia': '01',
            'codigo': 'ES1234000000000001JN0F',
            'ree_emisora': '1234',
            'ree_destino': '4321',
            'fecha': '2014-04-16T22:13:37',
        }
        header.feed(vals)
        return header

    def getNombre(self):
        nom = c1.Nombre()
        nom_vals = {
            'nombrepila': 'Perico',
            'apellido1': 'Palote',
            'apellido2': 'Pérez'
        }
        nom.feed(nom_vals)
        return nom

    def getTelefono(self, tipus='Telefono'):
        telefon = c1.Telefono(tipus)
        if tipus == 'Fax':
            telf_fields = {
                'numero': '555124124',
                'prefijo': 34
            }
        else:
            telf_fields = {
                'numero': '555123123',
                'prefijo': 34
            }
        telefon.feed(telf_fields)
        return telefon

    def getCliente(self, mail=False):
        #client
        idclient = c1.IdCliente()
        idclient.feed({
            'cifnif': 'DN',
            'identificador': '11111111H',
        })

        nomclient = self.getNombre()
        telefon = self.getTelefono()
        fax = self.getTelefono('Fax')

        client = c1.Cliente()
        cli_fields = {
            'idcliente': idclient,
            'nombre': nomclient,
            'indicador': 'S',
            'fax': fax,
            'telefono': telefon,
        }
        if mail:
            cli_fields.update({'correu': 'pericopalote@acme.com',})

        client.feed(cli_fields)

        return client


class Switching_W1_Test(unittest.TestCase):
    """test de W1"""

    def setUp(self):
        self.xml_w101 = open(get_data("w101.xml"), "r")
        self.xml_w101_0 = open(get_data("w101_0.xml"), "r")
        self.xml_w102_ok = open(get_data("w102-aceptacio.xml"), "r")
        self.xml_w102_ko = open(get_data("w102-rebuig.xml"), "r")

    def tearDown(self):
        self.xml_w101.close()
        self.xml_w102_ok.close()
        self.xml_w102_ko.close()

    def test_create_pas01(self):
        sup = supportClass()
        pas01 = w1.SolicitudAportacionLectura()
        header = sup.getHeader('W1', '01')
        pas01.set_agente('1234')
        lecturas = []
        for integrador, periodo, medida in [('AE', 21, '0000001162.00'),
                                            ('AE', 22, '0000003106.00'), ]:
            lectura = w1.LecturaAportada()
            lectura.feed(dict(
                integrador=integrador,
                codigo_periodedh=periodo,
                lectura_propuesta=medida,
            ))
            lecturas.append(lectura)
        pas01.feed({
            'capcalera': header,
            'fecha_lectura': '2015-02-18',
            'codigodh': 2,
            'lecturas': lecturas,
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_w101.read())

    def test_create_pas01_0_value(self):
        sup = supportClass()
        pas01 = w1.SolicitudAportacionLectura()
        header = sup.getHeader('W1', '01')
        pas01.set_agente('1234')
        lecturas = []
        for integrador, periodo, medida in [('AE', 61, float(1162.4567)),
                                            ('AE', 62, int(3106)),
                                            ('AE', 63, 0.0),
                                            ('AE', 64, '1234.00'),
                                            ('AE', 65, 1234567890.00),
                                            ('AE', 66, False), ]:
            lectura = w1.LecturaAportada()
            lectura.feed(dict(
                integrador=integrador,
                codigo_periodedh=periodo,
                lectura_propuesta=medida,
            ))
            lecturas.append(lectura)
        pas01.feed({
            'capcalera': header,
            'fecha_lectura': '2015-02-18',
            'codigodh': 6,
            'lecturas': lecturas,
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_w101_0.read())

    def test_create_pas02_accept(self):
        sup = supportClass()
        pas02 = w1.AceptacionAportacionLectura()
        header = sup.getHeader('W1', '02')
        pas02.set_agente('1234')
        dades_accept = w1.DatosAceptacionLectura()
        dades_accept.feed({'fecha_aceptacion': '2015-07-02'})
        pas02.feed({
            'capcalera': header,
            'datos_aceptacion': dades_accept})
        pas02.build_tree()
        xml = str(pas02)
        self.assertXmlEqual(xml, self.xml_w102_ok.read())

    def test_create_pas02_reject(self):
        sup = supportClass()
        pas02 = w1.RechazoAportacionLectura()
        header = sup.getHeader('W1', '02')
        pas02.set_agente('1234')
        dades_reject = w1.DatosRechazoLectura()
        dades_reject.feed(
            {'fecha_rechazo': '2015-07-02',
             'motivo': '01'})
        pas02.feed({
            'capcalera': header,
            'datos_rechazo': dades_reject})
        pas02.build_tree()
        xml = str(pas02)
        self.assertXmlEqual(xml, self.xml_w102_ko.read())

    def test_read_w101(self):
        self.w101_xml = W1(self.xml_w101)
        self.w101_xml.parse_xml()
        date = self.w101_xml.fecha_lectura
        cdh = self.w101_xml.codigo_dh
        lecturas = []
        for lect in self.w101_xml.lecturas:
            lecturas.append(
                (lect.integrador,
                 int(lect.codigo_periodo_dh),
                 '%.2f' % float(lect.lectura_propuesta))
            )
        assert len(lecturas) == 2
        assert lecturas[0] == ('AE', 21, '1162.00')
        assert lecturas[1] == ('AE', 22, '3106.00')

    def test_read_w102_ok(self):
        self.w102_xml = W1(self.xml_w102_ok)
        self.w102_xml.set_xsd()
        self.w102_xml.parse_xml()
        date = ''
        if self.w102_xml.aceptacion:
            date = self.w102_xml.aceptacion.fecha_aceptacion
        assert date == '2015-07-02'

    def test_read_w102_ko(self):
        self.w102_xml = W1(self.xml_w102_ko)
        self.w102_xml.set_xsd()
        self.w102_xml.parse_xml()
        date = ''
        reason = ''
        if not self.w102_xml.aceptacion:
            date = self.w102_xml.rechazo.fecha_rechazo
            reason = self.w102_xml.rechazo.motivo_rechazo
        assert date == '2015-07-02'
        assert reason == '01'


class SwitchingC1Test(unittest.TestCase):
    """test de C1"""

    def setUp(self):
        sup = supportClass()
        self.xml_c105_31alb = open(get_data("c105_31ALB.xml"), "r")
        self.xml_c105_31alb_mbt_kva = open(
            get_data("c105_31ALB_MarcaMedidaBT.xml"), "r"
        )
        self.xml_c105_31alb_mbt_va = open(
            get_data("c105_31ALB_MarcaMedidaBT_VA.xml"), "r"
        )
        self.xml_c101_regdoc = open(get_data("c101_RegistroDoc.xml"), "r")
        self.xml_c101 = open(get_data("c101.xml"), "r")

    def test_read_c105(self):
        self.c105_xml = C1(self.xml_c105_31alb)
        self.c105_xml.set_xsd()
        self.c105_xml.parse_xml()
        contract = self.c105_xml.contracte
        condicions = contract.condicions
        t31a_lb_info = condicions.get_31lb_info()
        assert contract.codi_contracte == '000393610950'
        assert condicions.tarifa == '011'
        assert not t31a_lb_info['marca_mesura_bt_perdues']

    def test_read_c105_31lb_kva(self):
        self.c105_xml = C1(self.xml_c105_31alb_mbt_kva)
        self.c105_xml.set_xsd()
        self.c105_xml.parse_xml()
        contract = self.c105_xml.contracte
        condicions = contract.condicions
        t31a_lb_info = condicions.get_31lb_info()
        assert contract.codi_contracte == '97120053381'
        assert condicions.tarifa == '011'
        assert t31a_lb_info['marca_mesura_bt_perdues']
        assert t31a_lb_info['kvas_trafo'] == 50.0

    def test_read_c105_31lb_va(self):
        self.c105_xml = C1(self.xml_c105_31alb_mbt_va)
        self.c105_xml.set_xsd()
        self.c105_xml.parse_xml()
        contract = self.c105_xml.contracte
        condicions = contract.condicions
        t31a_lb_info = condicions.get_31lb_info()
        assert contract.codi_contracte == '000135927341'
        assert condicions.tarifa == '011'
        assert t31a_lb_info['marca_mesura_bt_perdues']
        assert t31a_lb_info['kvas_trafo'] == 33.3

    def test_read_c101_min(self):
        c101_xml = C1(self.xml_c101)
        c101_xml.set_xsd()
        c101_xml.parse_xml()

        solicitud = c101_xml.sollicitud
        contracte = c101_xml.contracte
        client = c101_xml.client
        documents = c101_xml.documents

        assert solicitud.linia_negoci == '01'
        assert solicitud.sollicitudadm == 'S'
        assert solicitud.cicle_activacio == 'S'
        assert solicitud.data_prevista_accio == '2016-06-06'
        assert solicitud.representant == 'S'
        assert contracte.codi_contracte == '111111111'
        assert contracte.durada == 12
        assert contracte.tipus_contracte == '01'
        assert contracte.direccio_correspondencia == 'S'
        assert client.tipus_identificacio == 'CI'
        assert client.codi_identificacio == 'B36385870'
        assert client.nom == u'ACC Y COMP DE COCINA MILLAN Y MUÑOZ'
        assert client.telf_prefix == '34'
        assert client.telf_num == '666777888'
        assert documents == []

    def test_read_c101_regdoc(self):
        c101_xml = C1(self.xml_c101_regdoc)
        c101_xml.set_xsd()
        c101_xml.parse_xml()
        documents = c101_xml.documents
        assert len(documents) > 0
        doc = documents[0]
        assert doc.doc_type == '08'
        assert doc.url == 'http://eneracme.com/docs/NIF11111111H.pdf'
        c101_xml = C1(self.xml_c101)
        c101_xml.set_xsd()
        c101_xml.parse_xml()
        documents = c101_xml.documents
        assert documents == []

    def test_accept_no_sollicitud(self):
        text_to_elim = '    <DatosSolicitud>\n' \
                       '      <LineaNegocioElectrica>' \
                                '01</LineaNegocioElectrica>\n' \
                       '      <SolicitudAdmContractual>' \
                                'S</SolicitudAdmContractual>\n' \
                       '      <IndActivacionLectura>' \
                                'S</IndActivacionLectura>\n' \
                       '      <FechaPrevistaAccion>' \
                                '2016-06-06</FechaPrevistaAccion>\n' \
                       '      <IndSustitutoMandatario>' \
                                'S</IndSustitutoMandatario>\n' \
                       '    </DatosSolicitud>\n'

        c101_no_text_xml = C1(self.xml_c101.read().replace(text_to_elim, ''))
        c101_no_text_xml.set_xsd()
        c101_no_text_xml.parse_xml(validate=False)

        assert c101_no_text_xml.sollicitud is False

    def test_accept_no_contracte(self):
        text_to_elim = '    <Contrato>\n' \
                       '      <IdContrato>\n' \
                       '        <CodContrato>111111111</CodContrato>\n' \
                       '      </IdContrato>\n' \
                       '      <Duracion>12</Duracion>\n' \
                       '      <TipoContratoATR>01</TipoContratoATR>\n' \
                       '      <DireccionCorrespondencia>\n' \
                       '        <Indicador>S</Indicador>\n' \
                       '      </DireccionCorrespondencia>\n' \
                       '    </Contrato>\n'

        c101_no_text_xml = C1(self.xml_c101.read().replace(text_to_elim, ''))
        c101_no_text_xml.set_xsd()
        c101_no_text_xml.parse_xml(validate=False)

        assert c101_no_text_xml.contracte is False

    def test_accept_no_client(self):
        text_to_elim = '    <Cliente>\n' \
                       '      <IdCliente>\n' \
                       '        <TipoCIFNIF>CI</TipoCIFNIF>\n' \
                       '        <Identificador>B36385870</Identificador>\n' \
                       '      </IdCliente>\n' \
                       '      <Nombre>\n' \
                       '        <RazonSocial>' \
                                    'ACC Y COMP DE COCINA MILLAN Y MUÑOZ' \
                                '</RazonSocial>\n' \
                       '      </Nombre>\n' \
                       '      <Telefono>\n' \
                       '        <PrefijoPais>34</PrefijoPais>\n' \
                       '        <Numero>666777888</Numero>\n' \
                       '      </Telefono>\n' \
                       '    </Cliente>\n'

        c101_no_text_xml = C1(self.xml_c101.read().replace(text_to_elim, ''))
        c101_no_text_xml.set_xsd()
        c101_no_text_xml.parse_xml(validate=False)

        assert c101_no_text_xml.client is False

    def test_accept_no_id_type(self):
        text_to_elim = '        <TipoCIFNIF>CI</TipoCIFNIF>\n'

        c101_no_text_xml = C1(self.xml_c101.read().replace(text_to_elim, ''))
        c101_no_text_xml.set_xsd()
        c101_no_text_xml.parse_xml(validate=False)

        assert c101_no_text_xml.client.tipus_identificacio == ''

    def test_accept_no_cond_cont(self):
        c101_no_text_xml = C1(self.xml_c101)
        c101_no_text_xml.set_xsd()
        c101_no_text_xml.parse_xml(validate=False)

        assert c101_no_text_xml.contracte.condicions is False


class SwitchingC2Test(unittest.TestCase):
    """test de C2"""

    def setUp(self):
        sup = supportClass()
        self.xml_c201 = open(get_data("c201.xml"), "r")
        self.xml_c201_ciepapel = open(get_data("c201_CiePapel.xml"), "r")
        self.xml_c201_regdocs = open(get_data("c201_regdocs.xml"), "r")

        #sol·licitud
        self.sollicitud = c1.DatosSolicitud()
        sol_fields = {
            'linea': '01',
            'solicitudadm': 'S',
            'activacionlectura': 'S',
            'fechaprevista': '2015-05-27',
            'sustituto': 'S',
        }
        self.sollicitud.feed(sol_fields)

        # contracte
        # Id contracte
        idcontracte = c1.IdContrato()
        nom_ctr = '111111111'
        idcontracte.feed({
            'codigo': nom_ctr,
        })
        # Condicions contractuals
        potencies = c1.PotenciasContratadas()
        potencies.feed({'p1': 4400})

        condicions = c1.CondicionesContractuales()
        condicions.feed({
            'tarifa': '001',
            'potencies': potencies,
        })

        dir_corresp = c1.DireccionCorrespondencia()
        dir_corresp.feed({
            'indicador': 'S',
        })

        self.contracte = c1.Contrato()
        ctr_fields = {
            'tipo': '01',
            'duracion': 12,
            'idcontrato': idcontracte,
            'condiciones': condicions,
            'direccion': dir_corresp,
        }
        self.contracte.feed(ctr_fields)

        #client
        self.client = sup.getCliente()

        #mesura
        self.mesura = c2.Medida()
        self.mesura.feed({
            'cp_propietat': 'N',
            'cp_installacio': 'Y',
            'equip_aportat_client': 'N',
            'equip_installat_client': 'Y',
            'tipus_equip': 'L00',
        })

    def test_create_pas01(self):
        sup = supportClass()
        pas01 = c2.MensajeCambiodeComercializadoraConCambios()
        capcalera = sup.getHeader('C2', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        #sol·licitud de canvi
        canvi = c2.CambiodeComercializadoraConCambios()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
            'cnae': '9820',
            'vivenda': 'S',
            'tipuscanvititular': 'S',
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_c201.read())

    def test_create_pas01_ciepapel(self):
        sup = supportClass()
        pas01 = c2.MensajeCambiodeComercializadoraConCambios()
        capcalera = sup.getHeader('C2', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        cie_paper = c2.CiePapel()
        cie_paper.feed({
            'codigo_cie': '1234567',
            'potencia_inst_bt': 3500,
            'fecha_emision': '2015-06-04',
            'nif_instalador': '12345678Z',
            'nombre_instalador': 'Acme',
            'tension_suministro': '10',
            'tipo_suministro': 'VI',
        })

        dades_cie = c2.DatosCie()
        dades_cie.feed({'cie_electronico': 'N',
                        'cie_papel': cie_paper})

        doctecnica = c2.DocTecnica()
        doctecnica.feed({'datos_cie': dades_cie})

        #sol·licitud de canvi
        canvi = c2.CambiodeComercializadoraConCambios()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
            'doctecnica': doctecnica,
            'cnae': '9820',
            'vivenda': 'S',
            'tipuscanvititular': 'S',
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_c201_ciepapel.read())

    def test_create_pas01_documents_xml(self):
        sup = supportClass()
        pas01 = c2.MensajeCambiodeComercializadoraConCambios()
        capcalera = sup.getHeader('C2', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        dades_documents = [
            ('01', 'http://eneracme.com/docs/CIE0100001.pdf'),
            ('06', 'http://eneracme.com/docs/INV201509161234.pdf'),
            ('08', 'http://eneracme.com/docs/NIF11111111H.pdf'),
        ]

        docs = []
        for i in range(len(dades_documents)):
            doc = c2.RegistroDoc()
            doc.feed({
                'tipo': dades_documents[i][0],
                'url': dades_documents[i][1],
            })
            docs.append(doc)

        registro_documentos = c2.RegistrosDocumento()
        registro_documentos.feed({'registro': docs})

        # sol·licitud de canvi
        canvi = c2.CambiodeComercializadoraConCambios()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
            'registro': registro_documentos,
            'cnae': '9820',
            'vivenda': 'S',
            'tipuscanvititular': 'S',
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_c201_regdocs.read())

    def test_read_c201_regdoc(self):
        c201_xml = C2(self.xml_c201_regdocs)
        c201_xml.set_xsd()
        c201_xml.parse_xml()
        documents = c201_xml.documents
        assert len(documents) > 0
        assert documents[0].doc_type == '01'
        assert documents[0].url == 'http://eneracme.com/docs/CIE0100001.pdf'
        assert documents[1].doc_type == '06'
        assert documents[1].url == 'http://eneracme.com/docs/' \
                                   'INV201509161234.pdf'
        assert documents[2].doc_type == '08'
        assert documents[2].url == 'http://eneracme.com/docs/NIF11111111H.pdf'
        c201_xml = C1(self.xml_c201)
        c201_xml.set_xsd()
        c201_xml.parse_xml()
        documents = c201_xml.documents
        assert documents == []

    def test_accept_no_sollicitud(self):
        text_to_elim = '        <DatosSolicitud>\n' \
                       '            <LineaNegocioElectrica>' \
                                        '01</LineaNegocioElectrica>\n' \
                       '            <SolicitudAdmContractual>' \
                                        'S</SolicitudAdmContractual>\n' \
                       '            <IndActivacionLectura>' \
                                        'S</IndActivacionLectura>\n' \
                       '            <FechaPrevistaAccion>' \
                                        '2015-05-27</FechaPrevistaAccion>\n' \
                       '            <IndSustitutoMandatario>' \
                                        'S</IndSustitutoMandatario>\n' \
                       '        </DatosSolicitud>\n'

        c201_no_text_xml = C2(self.xml_c201.read().replace(text_to_elim, ''))
        c201_no_text_xml.set_xsd()
        c201_no_text_xml.parse_xml(validate=False)

        assert c201_no_text_xml.sollicitud is False

    def test_accept_no_contracte(self):
        text_to_elim = '        <Contrato>\n' \
                       '            <IdContrato>\n' \
                       '                <CodContrato>' \
                                            '111111111</CodContrato>\n' \
                       '            </IdContrato>\n' \
                       '            <Duracion>12</Duracion>\n' \
                       '            <TipoContratoATR>01</TipoContratoATR>\n' \
                       '            <CondicionesContractuales>\n' \
                       '                <TarifaATR>001</TarifaATR>\n' \
                       '                <PotenciasContratadas>\n' \
                       '                    <Potencia Periodo="1">' \
                                                '4400</Potencia>\n' \
                       '                </PotenciasContratadas>\n' \
                       '            </CondicionesContractuales>\n' \
                       '            <DireccionCorrespondencia>\n' \
                       '                <Indicador>S</Indicador>\n' \
                       '            </DireccionCorrespondencia>\n' \
                       '        </Contrato>\n'

        c201_no_text_xml = C2(self.xml_c201.read().replace(text_to_elim, ''))
        c201_no_text_xml.set_xsd()
        c201_no_text_xml.parse_xml(validate=False)

        assert c201_no_text_xml.contracte is False

    def test_accept_no_client(self):
        text_to_elim = '        <Cliente>\n' \
                       '            <IdCliente>\n' \
                       '                <TipoCIFNIF>DN</TipoCIFNIF>\n' \
                       '                <Identificador>' \
                                            '11111111H</Identificador>\n' \
                       '            </IdCliente>\n' \
                       '            <Nombre>\n' \
                       '                <NombreDePila>Perico</NombreDePila>\n' \
                       '                <PrimerApellido>' \
                                            'Palote</PrimerApellido>\n' \
                       '                <SegundoApellido>' \
                                            'Pérez</SegundoApellido>\n' \
                       '            </Nombre>\n' \
                       '            <Fax>\n' \
                       '                <PrefijoPais>34</PrefijoPais>\n' \
                       '                <Numero>555124124</Numero>\n' \
                       '            </Fax>\n' \
                       '            <Telefono>\n' \
                       '                <PrefijoPais>34</PrefijoPais>\n' \
                       '                <Numero>555123123</Numero>\n' \
                       '            </Telefono>\n' \
                       '            <IndicadorTipoDireccion>' \
                                        'S</IndicadorTipoDireccion>\n' \
                       '        </Cliente>\n'

        c201_no_text_xml = C2(self.xml_c201.read().replace(text_to_elim, ''))
        c201_no_text_xml.set_xsd()
        c201_no_text_xml.parse_xml(validate=False)

        assert c201_no_text_xml.client is False

    def test_accept_no_id_type(self):
        text_to_elim = '        <TipoCIFNIF>DN</TipoCIFNIF>\n'

        c201_no_text_xml = C2(self.xml_c201.read().replace(text_to_elim, ''))
        c201_no_text_xml.set_xsd()
        c201_no_text_xml.parse_xml(validate=False)

        assert c201_no_text_xml.client.tipus_identificacio == ''

    def test_accept_no_cond_cont(self):
        text_to_elim = '            <CondicionesContractuales>\n' \
                       '                <TarifaATR>001</TarifaATR>\n' \
                       '                <PotenciasContratadas>\n' \
                       '                    <Potencia Periodo="1">' \
                                                '4400</Potencia>\n' \
                       '                </PotenciasContratadas>\n' \
                       '            </CondicionesContractuales>\n'

        c201_no_text_xml = C2(self.xml_c201.read().replace(text_to_elim, ''))
        c201_no_text_xml.set_xsd()
        c201_no_text_xml.parse_xml(validate=False)

        assert c201_no_text_xml.contracte.condicions is False



class SwitchingA3Test(unittest.TestCase):
    """test de A3"""

    def setUp(self):
        sup = supportClass()
        self.xml_a301 = open(get_data("a301.xml"), "r")
        self.xml_a301_ciepapel = open(get_data("a301_CiePapel.xml"), "r")
        self.xml_a301_autoconsumo = open(get_data("a301_Autoconsumo.xml"), "r")
        self.xml_a301_regsdoc = open(get_data("a301_regsdoc.xml"), "r")

        #sol·licitud
        self.sollicitud = c1.DatosSolicitud()
        sol_fields = {
            'linea': '01',
            'solicitudadm': 'S',
            'activacionlectura': 'N',
            'fechaprevista': '2015-05-18',
            'cnae': '9820',
            'sustituto': 'S',
        }
        self.sollicitud.feed(sol_fields)

        # contracte
        # Id contracte
        idcontracte = c1.IdContrato()
        nom_ctr = '111111111'
        idcontracte.feed({
            'codigo': nom_ctr,
        })
        # Condicions contractuals
        potencies = c1.PotenciasContratadas()
        potencies.feed({'p1': 2300})

        condicions = c1.CondicionesContractuales()
        condicions.feed({
            'tarifa': '001',
            'potencies': potencies,
        })

        dir_corresp = c1.DireccionCorrespondencia()
        dir_corresp.feed({
            'indicador': 'S',
        })

        self.contracte = c1.Contrato()
        ctr_fields = {
            'tipo': '01',
            'duracion': 12,
            'idcontrato': idcontracte,
            'condiciones': condicions,
            'direccion': dir_corresp,
        }
        self.contracte.feed(ctr_fields)

        # contracte_autoconsum
        self.contracte_autoconsum = c1.Contrato()
        ctr_fields = {
            'tipo_autoconsumo': '2A',
            'tipo': '01',
            'duracion': 12,
            'idcontrato': idcontracte,
            'condiciones': condicions,
            'direccion': dir_corresp,
        }
        self.contracte_autoconsum.feed(ctr_fields)

        #client
        self.client = sup.getCliente()

        #mesura
        self.mesura = c2.Medida()
        self.mesura.feed({
            'cp_propietat': 'N',
            'cp_installacio': 'Y',
            'equip_aportat_client': 'N',
            'equip_installat_client': 'Y',
            'tipus_equip': 'L00',
        })

    def test_create_pas01(self):
        sup = supportClass()
        pas01 = a3.MensajePasoMRAMLConCambiosRestoTarifas()
        capcalera = sup.getHeader('A3', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        #sol·licitud de canvi
        canvi = a3.PasoMRAMLConCambiosRestoTarifas()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_a301.read())

    def test_create_pas01_ciepapel(self):
        sup = supportClass()
        pas01 = a3.MensajePasoMRAMLConCambiosRestoTarifas()
        capcalera = sup.getHeader('A3', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        cie_paper = c2.CiePapel()
        cie_paper.feed({
            'codigo_cie': '1234567',
            'potencia_inst_bt': 3500,
            'fecha_emision': '2015-06-04',
            'nif_instalador': '12345678Z',
            'nombre_instalador': 'Acme',
            'tension_suministro': '10',
            'tipo_suministro': 'VI',
        })

        dades_cie = c2.DatosCie()
        dades_cie.feed({'cie_electronico': 'N',
                        'cie_papel': cie_paper})

        doctecnica = c2.DocTecnica()
        doctecnica.feed({'datos_cie': dades_cie})

        #sol·licitud de canvi
        canvi = a3.PasoMRAMLConCambiosRestoTarifas()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
            'doctecnica': doctecnica,
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_a301_ciepapel.read())

    def test_create_pas01_tipoautoconsumo(self):
        sup = supportClass()
        pas01 = a3.MensajePasoMRAMLConCambiosRestoTarifas()
        capcalera = sup.getHeader('A3', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte_autoconsum
        client = self.client
        mesura = self.mesura

        #sol·licitud de canvi
        canvi = a3.PasoMRAMLConCambiosRestoTarifas()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_a301_autoconsumo.read())

    def test_read_a301(self):
        self.a301_xml = A3(self.xml_a301)
        self.a301_xml.set_xsd()
        self.a301_xml.parse_xml()
        contract = self.a301_xml.contracte
        mesures = self.a301_xml.mesura
        comentaris = self.a301_xml.comentaris
        assert contract.codi_contracte == '111111111'
        assert contract.tipus_autoconsum == '00'
        assert mesures.cp_installacio == 'Y'
        assert mesures.mesura.TipoEquipoMedida == 'L00'
        assert isinstance(comentaris, list)

    def test_read_a301_ciepapel(self):
        self.a301_xml_ciepapel = A3(self.xml_a301_ciepapel)
        self.a301_xml_ciepapel.set_xsd()
        self.a301_xml_ciepapel.parse_xml()
        contract = self.a301_xml_ciepapel.contracte

        ciepapel = self.a301_xml_ciepapel.obj.PasoMRAMLConCambiosRestoTarifa\
            .DocTecnica.DatosCie.CIEPapel
        assert contract.codi_contracte == '111111111'
        assert contract.tipus_autoconsum == '00'
        assert ciepapel.CodigoCie.text == '1234567'

    def test_read_a301_autoconsumo(self):
        self.a301_xml_autoconsumo = A3(self.xml_a301_autoconsumo)
        self.a301_xml_autoconsumo.set_xsd()
        self.a301_xml_autoconsumo.parse_xml()
        contract = self.a301_xml_autoconsumo.contracte

        assert contract.codi_contracte == '111111111'
        assert contract.tipus_autoconsum == '2A'

    def test_read_c201_regdoc(self):
        a301_xml = A3(self.xml_a301_regsdoc)
        a301_xml.set_xsd()
        a301_xml.parse_xml()
        documents = a301_xml.documents
        assert len(documents) > 0
        assert documents[0].doc_type == '08'
        assert documents[0].url == 'http://eneracme.com/docs/NIF11111111H.pdf'
        a301_xml = A3(self.xml_a301)
        a301_xml.set_xsd()
        a301_xml.parse_xml()
        documents = a301_xml.documents
        assert documents == []

    def test_accept_no_sollicitud(self):
        text_to_elim = '        <DatosSolicitud>\n' \
                       '            <LineaNegocioElectrica>' \
                                        '01</LineaNegocioElectrica>\n' \
                       '            <SolicitudAdmContractual>' \
                                        'S</SolicitudAdmContractual>\n' \
                       '            <IndActivacionLectura>' \
                                        'N</IndActivacionLectura>\n' \
                       '            <FechaPrevistaAccion>' \
                                        '2015-05-18</FechaPrevistaAccion>\n' \
                       '            <CNAE>9820</CNAE>\n' \
                       '            <IndSustitutoMandatario>' \
                                        'S</IndSustitutoMandatario>\n' \
                       '        </DatosSolicitud>\n'

        a301_no_text_xml = A3(self.xml_a301.read().replace(text_to_elim, ''))
        a301_no_text_xml.set_xsd()
        a301_no_text_xml.parse_xml(validate=False)

        assert a301_no_text_xml.sollicitud is False

    def test_accept_no_contracte(self):
        text_to_elim = '        <Contrato>\n' \
                       '            <IdContrato>\n' \
                       '                <CodContrato>111111111</CodContrato>\n' \
                       '            </IdContrato>\n' \
                       '            <Duracion>12</Duracion>\n' \
                       '            <TipoContratoATR>01</TipoContratoATR>\n' \
                       '            <CondicionesContractuales>\n' \
                       '                <TarifaATR>001</TarifaATR>\n' \
                       '                <PotenciasContratadas>\n' \
                       '                    <Potencia Periodo="1">' \
                                                '2300</Potencia>\n' \
                       '                </PotenciasContratadas>\n' \
                       '            </CondicionesContractuales>\n' \
                       '            <DireccionCorrespondencia>\n' \
                       '                <Indicador>S</Indicador>\n' \
                       '            </DireccionCorrespondencia>\n' \
                       '        </Contrato>\n'

        a301_no_text_xml = A3(self.xml_a301.read().replace(text_to_elim, ''))
        a301_no_text_xml.set_xsd()
        a301_no_text_xml.parse_xml(validate=False)

        assert a301_no_text_xml.contracte is False

    def test_accept_no_client(self):
        text_to_elim = '        <Cliente>\n' \
                       '            <IdCliente>\n' \
                       '                <TipoCIFNIF>DN</TipoCIFNIF>\n' \
                       '                <Identificador>' \
                                            '11111111H</Identificador>\n' \
                       '            </IdCliente>\n' \
                       '            <Nombre>\n' \
                       '                <NombreDePila>Perico</NombreDePila>\n' \
                       '                <PrimerApellido>' \
                                            'Palote</PrimerApellido>\n' \
                       '                <SegundoApellido>' \
                                            'Pérez</SegundoApellido>\n' \
                       '            </Nombre>\n' \
                       '            <Fax>\n' \
                       '                <PrefijoPais>34</PrefijoPais>\n' \
                       '                <Numero>555124124</Numero>\n' \
                       '            </Fax>\n' \
                       '            <Telefono>\n' \
                       '                <PrefijoPais>34</PrefijoPais>\n' \
                       '                <Numero>555123123</Numero>\n' \
                       '            </Telefono>\n' \
                       '            <IndicadorTipoDireccion>' \
                                        'S</IndicadorTipoDireccion>\n' \
                       '        </Cliente>\n'

        a301_no_text_xml = A3(self.xml_a301.read().replace(text_to_elim, ''))
        a301_no_text_xml.set_xsd()
        a301_no_text_xml.parse_xml(validate=False)

        assert a301_no_text_xml.client is False

    def test_accept_no_id_type(self):
        text_to_elim = '        <TipoCIFNIF>DN</TipoCIFNIF>\n'

        a301_no_text_xml = A3(self.xml_a301.read().replace(text_to_elim, ''))
        a301_no_text_xml.set_xsd()
        a301_no_text_xml.parse_xml(validate=False)

        assert a301_no_text_xml.client.tipus_identificacio == ''

    def test_accept_no_cond_cont(self):
        text_to_elim = '            <CondicionesContractuales>\n' \
                       '                <TarifaATR>001</TarifaATR>\n' \
                       '                <PotenciasContratadas>\n' \
                       '                    <Potencia Periodo="1">2300</Potencia>\n' \
                       '                </PotenciasContratadas>\n' \
                       '            </CondicionesContractuales>\n'

        a301_no_text_xml = A3(self.xml_a301.read().replace(text_to_elim, ''))
        a301_no_text_xml.set_xsd()
        a301_no_text_xml.parse_xml(validate=False)

        assert a301_no_text_xml.contracte.condicions is False


class SwitchingB1Test(unittest.TestCase):
    """test de B1"""

    def setUp(self):
        sup = supportClass
        self.xml_b101 = open(get_data("b101.xml"), "r")
        self.xml_b101_regdoc = open(get_data("b101_RegistroDoc.xml"), "r")

    def test_read_b101_regdoc(self):
        b101_xml = M1(self.xml_b101_regdoc)
        b101_xml.set_xsd()
        b101_xml.parse_xml()
        documents = b101_xml.documents
        assert len(documents) > 0
        doc = documents[0]
        assert doc.doc_type == '08'
        assert doc.url == 'http://eneracme.com/docs/NIF11111111H.pdf'
        b101_xml = M1(self.xml_b101)
        b101_xml.set_xsd()
        b101_xml.parse_xml()
        documents = b101_xml.documents
        assert documents == []


class SwitchingM1Test(unittest.TestCase):
    """test de M1"""

    def setUp(self):
        sup = supportClass()
        self.xml_m101 = open(get_data("m101.xml"), "r")
        self.xml_m101_regsdoc = open(get_data("m101_RegsDoc.xml"), "r")
        self.xml_m101_ciepapel = open(get_data("m101_CiePapel.xml"), "r")
        self.xml_m101_DT = open(get_data("m101_DocTecnica.xml"), "r")
        self.xml_m101_DT2 = open(get_data("m101_DocTecnica2.xml"), "r")

        #sol·licitud
        self.sollicitud = c1.DatosSolicitud()
        sol_fields = {
            'linea': '01',
            'solicitudadm': 'S',
            'activacionlectura': 'N',
            'fechaprevista': '2015-05-18',
        }
        self.sollicitud.feed(sol_fields)

        # contracte
        # Id contracte
        idcontracte = c1.IdContrato()
        nom_ctr = '111111111'
        idcontracte.feed({
            'codigo': nom_ctr,
        })
        # Condicions contractuals
        potencies = c1.PotenciasContratadas()
        potencies.feed({'p1': 4400})

        condicions = c1.CondicionesContractuales()
        condicions.feed({
            'tarifa': '001',
            'potencies': potencies,
        })

        dir_corresp = c1.DireccionCorrespondencia()
        dir_corresp.feed({
            'indicador': 'S',
        })

        self.contracte = c1.Contrato()
        ctr_fields = {
            'tipo': '01',
            'duracion': 12,
            'idcontrato': idcontracte,
            'condiciones': condicions,
            'direccion': dir_corresp,
        }
        self.contracte.feed(ctr_fields)

        #client
        self.client = sup.getCliente()

        #mesura
        self.mesura = c2.Medida()
        self.mesura.feed({
            'cp_propietat': 'N',
            'cp_installacio': 'Y',
            'equip_aportat_client': 'N',
            'equip_installat_client': 'Y',
            'tipus_equip': 'L00',
        })

    def test_create_pas01(self):
        sup = supportClass()
        pas01 = m1.MensajeModificacionDeATR()
        capcalera = sup.getHeader('M1', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        #sol·licitud de canvi
        canvi = m1.ModificacionDeATR()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
            'cnae': '9820',
            'vivenda': 'S',
            'tipuscanvititular': 'S',
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_m101.read())

    def test_create_pas01_ciepapel(self):
        sup = supportClass()
        pas01 = m1.MensajeModificacionDeATR()
        capcalera = sup.getHeader('M1', '01')
        pas01.set_agente('1234')

        sollicitud = self.sollicitud
        contracte = self.contracte
        client = self.client
        mesura = self.mesura

        cie_paper = c2.CiePapel()
        cie_paper.feed({
            'codigo_cie': '1234567',
            'potencia_inst_bt': 3500,
            'fecha_emision': '2015-06-04',
            'nif_instalador': '12345678Z',
            'nombre_instalador': 'Acme',
            'tension_suministro': '10',
            'tipo_suministro': 'VI',
        })

        dades_cie = c2.DatosCie()
        dades_cie.feed({'cie_electronico': 'N',
                        'cie_papel': cie_paper})

        doctecnica = c2.DocTecnica()
        doctecnica.feed({'datos_cie': dades_cie})

        #sol·licitud de canvi
        canvi = m1.ModificacionDeATR()
        canvi_vals = {
            'solicitud': sollicitud,
            'contrato': contracte,
            'cliente': client,
            'medida': mesura,
            'doctecnica': doctecnica,
            'cnae': '9820',
            'vivenda': 'S',
            'tipuscanvititular': 'S',
        }
        canvi.feed(canvi_vals)

        pas01.feed({
            'cabecera': capcalera,
            'cambio': canvi
        })
        pas01.build_tree()
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_m101_ciepapel.read())

    def test_read_m101_docTec(self):
        self.m101_dt_xml = M1(self.xml_m101_DT)
        self.m101_dt_xml.set_xsd()
        self.m101_dt_xml.parse_xml()
        doc_tecnica = self.m101_dt_xml.documentacio_tecnica
        assert doc_tecnica.es_Cie_electronic == 'N'
        assert doc_tecnica.codi_CIE == '1234567'
        assert doc_tecnica.potencia_instalada_BT == '3500'
        assert doc_tecnica.data_emissio_CIE == '2015-06-04'
        assert doc_tecnica.data_fi_CIE == '2015-06-05'
        assert doc_tecnica.nif_intalador == '12345678Z'
        assert doc_tecnica.nom_instalador == 'Acme'
        assert doc_tecnica.tensio_suministrada == '10'
        assert doc_tecnica.intensitat_diferencial == '8'
        assert doc_tecnica.sensibilitat_diferencial == '9'
        assert doc_tecnica.seccio_cable == '2'
        assert doc_tecnica.tipus_suministre == 'VI'
        self.m101_dt_xml = M1(self.xml_m101_DT2)
        self.m101_dt_xml.set_xsd()
        self.m101_dt_xml.parse_xml()
        doc_tecnica = self.m101_dt_xml.documentacio_tecnica
        assert doc_tecnica.codi_instalador == '12345678Z'

        self.m101_dt_xml = M1(self.xml_m101)
        self.m101_dt_xml.set_xsd()
        self.m101_dt_xml.parse_xml()
        doc_tecnica = self.m101_dt_xml.documentacio_tecnica
        assert not doc_tecnica

    def test_read_m101_regdoc(self):
        m101_xml = M1(self.xml_m101_regsdoc)
        m101_xml.set_xsd()
        m101_xml.parse_xml()
        documents = m101_xml.documents
        assert len(documents) > 0
        doc = documents[0]
        assert doc.doc_type == '08'
        assert doc.url == 'http://eneracme.com/docs/NIF11111111H.pdf'
        m101_xml = M1(self.xml_m101)
        m101_xml.set_xsd()
        m101_xml.parse_xml()
        documents = m101_xml.documents
        assert documents == []

    def test_accept_no_sollicitud(self):
        text_to_elim = '        <DatosSolicitud>\n' \
                       '            <LineaNegocioElectrica>' \
                                        '01</LineaNegocioElectrica>\n' \
                       '            <SolicitudAdmContractual>' \
                                        'S</SolicitudAdmContractual>\n' \
                       '            <IndActivacionLectura>' \
                                        'N</IndActivacionLectura>\n' \
                       '            <FechaPrevistaAccion>' \
                                        '2015-05-18</FechaPrevistaAccion>\n' \
                       '        </DatosSolicitud>\n'

        m101_no_text_xml = M1(self.xml_m101.read().replace(text_to_elim, ''))
        m101_no_text_xml.set_xsd()
        m101_no_text_xml.parse_xml(validate=False)

        assert m101_no_text_xml.sollicitud is False

    def test_accept_no_contracte(self):
        text_to_elim = '        <Contrato>\n' \
                       '            <IdContrato>\n' \
                       '                <CodContrato>' \
                                            '111111111</CodContrato>\n' \
                       '            </IdContrato>\n' \
                       '            <Duracion>12</Duracion>\n' \
                       '            <TipoContratoATR>01</TipoContratoATR>\n' \
                       '            <CondicionesContractuales>\n' \
                       '                <TarifaATR>001</TarifaATR>\n' \
                       '                <PotenciasContratadas>\n' \
                       '                    <Potencia Periodo="1">' \
                                                '4400</Potencia>\n' \
                       '                </PotenciasContratadas>\n' \
                       '            </CondicionesContractuales>\n' \
                       '            <DireccionCorrespondencia>\n' \
                       '                <Indicador>S</Indicador>\n' \
                       '            </DireccionCorrespondencia>\n' \
                       '        </Contrato>\n'

        m101_no_text_xml = M1(
            self.xml_m101.read().replace(text_to_elim, ''))
        m101_no_text_xml.set_xsd()
        m101_no_text_xml.parse_xml(validate=False)

        assert m101_no_text_xml.contracte is False

    def test_accept_no_client(self):
        text_to_elim = '        <Cliente>\n' \
                       '            <IdCliente>\n' \
                       '                <TipoCIFNIF>DN</TipoCIFNIF>\n' \
                       '                <Identificador>' \
                                            '11111111H</Identificador>\n' \
                       '            </IdCliente>\n' \
                       '            <Nombre>\n' \
                       '                <NombreDePila>Perico</NombreDePila>\n' \
                       '                <PrimerApellido>' \
                                            'Palote</PrimerApellido>\n' \
                       '                <SegundoApellido>' \
                                            'Pérez</SegundoApellido>\n' \
                       '            </Nombre>\n' \
                       '            <Fax>\n' \
                       '                <PrefijoPais>34</PrefijoPais>\n' \
                       '                <Numero>555124124</Numero>\n' \
                       '            </Fax>\n' \
                       '            <Telefono>\n' \
                       '                <PrefijoPais>34</PrefijoPais>\n' \
                       '                <Numero>555123123</Numero>\n' \
                       '            </Telefono>\n' \
                       '            <IndicadorTipoDireccion>' \
                                        'S</IndicadorTipoDireccion>\n' \
                       '        </Cliente>\n'

        m101_no_text_xml = M1(
            self.xml_m101.read().replace(text_to_elim, ''))
        m101_no_text_xml.set_xsd()
        m101_no_text_xml.parse_xml(validate=False)

        assert m101_no_text_xml.client is False

    def test_accept_no_id_type(self):
        text_to_elim = '        <TipoCIFNIF>DN</TipoCIFNIF>\n'

        m101_no_text_xml = M1(
            self.xml_m101.read().replace(text_to_elim, ''))
        m101_no_text_xml.set_xsd()
        m101_no_text_xml.parse_xml(validate=False)

        assert m101_no_text_xml.client.tipus_identificacio == ''

    def test_accept_no_cond_cont(self):
        text_to_elim = '            <CondicionesContractuales>\n' \
                       '                <TarifaATR>001</TarifaATR>\n' \
                       '                <PotenciasContratadas>\n' \
                       '                    <Potencia Periodo="1">' \
                                                '4400</Potencia>\n' \
                       '                </PotenciasContratadas>\n' \
                       '            </CondicionesContractuales>\n'

        m101_no_text_xml = M1(
            self.xml_m101.read().replace(text_to_elim, ''))
        m101_no_text_xml.set_xsd()
        m101_no_text_xml.parse_xml(validate=False)

        assert m101_no_text_xml.contracte.condicions is False


class SwitchingR1_Test(unittest.TestCase):
    """test de R1"""

    def setUp(self):
        sup = supportClass()
        # r1-01
        self.xml_r101_minim = open(get_data("r101_minim.xml"), "r")
        self.xml_r101_reclamant = open(get_data("r101_reclamante.xml"), "r")
        self.xml_r101_client = open(get_data("r101_cliente.xml"), "r")
        self.xml_r101_documents = open(get_data("r101_documentos.xml"), "r")
        self.xml_r101_lectures = open(get_data("r101_lectures.xml"), "r")
        self.xml_r101_0539 = open(get_data("r101_05_39.xml"), "r")
        self.xml_r101_0203 = open(get_data("r101_02_03.xml"), "r")
        self.xml_r101_multivar = open(get_data("r101_multivar.xml"), "r")
        # r1-02
        self.xml_r102_ok = open(get_data("r102_aceptacion.xml"), "r")
        self.xml_r102_ko = open(get_data("r102_rechazo.xml"), "r")
        # r1-03
        self.xml_r103_minim = open(get_data("r103_minim.xml"), "r")
        self.xml_r103_desc = open(get_data("r103_desc_inter.xml"), "r")
        self.xml_r103_inter = open(get_data("r103_intervenciones.xml"), "r")
        self.xml_r103_retip = open(get_data("r103_retipificacion.xml"), "r")
        self.xml_r103_solicitudes = open(get_data("r103_solicitudes.xml"), "r")
        # r1-04
        self.xml_r104_variables = open(get_data("r104_variables.xml"), "r")
        self.xml_r104_reg_doc = open(get_data("r104_reg_doc.xml"), "r")
        # r1-05
        self.xml_r105 = open(get_data("r105.xml"), "r")
        self.xml_r105_retipificacio = open(get_data("r105_retipificacio.xml"), "r")

        self.client = sup.getCliente(True)
        self.reclamant = self.getReclamante()

    def tearDown(self):
        # r1-01
        self.xml_r101_minim.close()
        self.xml_r101_reclamant.close()
        self.xml_r101_client.close()
        self.xml_r101_documents.close()
        self.xml_r101_lectures.close()
        self.xml_r101_0539.close()
        self.xml_r101_0203.close()
        # r1-02
        self.xml_r102_ok.close()
        self.xml_r102_ko.close()
        # r1-03
        self.xml_r103_minim.close()
        self.xml_r103_desc.close()
        self.xml_r103_inter.close()
        self.xml_r103_retip.close()
        self.xml_r103_solicitudes.close()
        # r1-04
        self.xml_r104_variables.close()
        self.xml_r104_reg_doc.close()
        # r1-05
        self.xml_r105.close()
        self.xml_r105_retipificacio.close()

    def getReclamante(self):
        sup = supportClass()
        id_reclamant = r1.IdReclamante()
        idrec_vals = {
            'tipus_cifnif': 'DN',
            'identificador': '11111111H',
        }
        id_reclamant.feed(idrec_vals)

        nom = sup.getNombre()
        fax = sup.getTelefono('Fax')
        telefon = sup.getTelefono()

        correu = 'pericopalote@acme.com'

        reclamant = r1.Reclamante()
        reclamant_vals = {
            'id_reclamant': id_reclamant,
            'nom': nom,
            'fax': fax,
            'telefon': telefon,
            'correu': correu,
        }
        reclamant.feed(reclamant_vals)

        return reclamant

    def getHeader(self, process='R1', step='01', codsolicitud='20141211100908'):
        header = r1.CabeceraReclamacion()
        vals = {
            'proceso': process,
            'paso': step,
            'solicitud': codsolicitud,
            'secuencia': '01',
            'cups': 'ES1234000000000001JN0F',
            'ree_emisora': '1234',
            'ree_destino': '4321',
            'fecha': '2014-04-16T22:13:37',
        }
        header.feed(vals)
        return header

    def getDatosSolicitud(self, tipo, subtipo, ref=None):
        dades = r1.DatosSolicitud()
        vals = {
            'tipus': tipo,
            'subtipus': subtipo,
        }

        if ref:
            vals.update({'ref_origen': ref})
        dades.feed(vals)
        return dades

    def getDatosInformacion(self, tipo, codigo_reclamante, numExp=None):
        dades = r1.DatosInformacion()
        vals = {
            'tipus_comunicacio': tipo,
            'codi_reclamant_distri': codigo_reclamante,
        }

        if numExp:
            vals.update({'num_expedient': numExp})
        dades.feed(vals)
        return dades

    def test_create_pas01_minim(self):
        pas01 = r1.MensajeReclamacionIncidenciaPeticion()
        header = self.getHeader('R1', '01')
        pas01.set_agente('1234')
        dades = self.getDatosSolicitud('03', '16')

        variables = r1.VariablesDetalleReclamacion()
        variable = r1.VariableDetalleReclamacion()

        variables.feed({'detalls': [variable]})

        solicitud = r1.SolicitudReclamacion()
        solicitud.feed({
            'dades': dades,
            'variables': variables,
            'tipus_reclamant': '06',
            'comentaris': u'R1-01 minimum Test',
        })
        pas01.feed({
            'capcalera': header,
            'solicitud': solicitud
        })
        pas01.build_tree()
        pas01.pretty_print = True
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_r101_minim.read())

    def test_create_pas01_reclamant(self):
        pas01 = r1.MensajeReclamacionIncidenciaPeticion()
        header = self.getHeader('R1', '01')
        pas01.set_agente('1234')
        dades = self.getDatosSolicitud('03', '16')

        variables = r1.VariablesDetalleReclamacion()
        variable = r1.VariableDetalleReclamacion()

        variables.feed({'detalls': [variable]})

        reclamant = self.reclamant

        solicitud = r1.SolicitudReclamacion()
        solicitud.feed({
            'dades': dades,
            'variables': variables,
            #'client': client,
            'tipus_reclamant': '01',
            'reclamant': reclamant,
            'comentaris': u'R1-01 with Reclamante Test',
        })
        pas01.feed({
            'capcalera': header,
            'solicitud': solicitud
        })
        pas01.build_tree()
        pas01.pretty_print = True
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_r101_reclamant.read())

    def test_create_pas01_client(self):
        pas01 = r1.MensajeReclamacionIncidenciaPeticion()
        header = self.getHeader('R1', '01')
        pas01.set_agente('1234')
        dades = self.getDatosSolicitud('03', '16')

        variables = r1.VariablesDetalleReclamacion()
        variable = r1.VariableDetalleReclamacion()

        variables.feed({'detalls': [variable]})

        client = self.client

        solicitud = r1.SolicitudReclamacion()
        solicitud.feed({
            'dades': dades,
            'variables': variables,
            'client': client,
            'tipus_reclamant': '06',
            'comentaris': u'R1-01 with Cliente Test',
        })
        pas01.feed({
            'capcalera': header,
            'solicitud': solicitud
        })
        pas01.build_tree()
        pas01.pretty_print = True
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_r101_client.read())

    def test_create_pas01_lectures(self):
        pas01 = r1.MensajeReclamacionIncidenciaPeticion()
        header = self.getHeader('R1', '01')
        pas01.set_agente('1234')
        dades = self.getDatosSolicitud('02', '36')

        variables = r1.VariablesDetalleReclamacion()

        lectures = []
        for integrador, periodo, medida in [('AE', 21, '0000001162.00'),
                                            ('AE', 22, '0000003106.00'), ]:
            lectura = w1.LecturaAportada()
            lectura.feed(dict(
                integrador=integrador,
                codigo_periodedh=periodo,
                lectura_propuesta=medida,
            ))
            lectures.append(lectura)

        lect_aportades = r1.LecturasAportadas()
        lect_aportades.feed({
            'lectures': lectures
        })
        variable = r1.VariableDetalleReclamacion()
        variable.feed({
            'num_factura_atr': '243615',
            'data_lectura': '2016-01-20',
            'codidh': '2',
            'lectures': lect_aportades
        })

        variables.feed({'detalls': [variable]})

        # Client
        idclient = c1.IdCliente()
        idclient.feed({
            'cifnif': 'NI',
            'identificador': '11111111H',
        })

        nomclient = c1.Nombre()
        nom_vals = {
            'nombrepila': 'Perico',
            'apellido1': 'Palotes',
            'apellido2': 'Largos'
        }
        nomclient.feed(nom_vals)

        telefon = c1.Telefono()
        telf_fields = {
            'numero': '66612345',
            'prefijo': 34
        }
        telefon.feed(telf_fields)

        client = c1.Cliente()
        cli_fields = {
            'idcliente': idclient,
            'nombre': nomclient,
            'indicador': 'S',
            'telefono': telefon,
        }
        cli_fields.update({'correu': 'perico@acme.com'})

        client.feed(cli_fields)

        solicitud = r1.SolicitudReclamacion()
        solicitud.feed({
            'dades': dades,
            'variables': variables,
            'client': client,
            'tipus_reclamant': '06',
            'comentaris': u'R1-01 lectures',
        })
        pas01.feed({
            'capcalera': header,
            'solicitud': solicitud
        })
        pas01.build_tree()
        pas01.pretty_print = True
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_r101_lectures.read())

    def test_create_pas01_documents(self):
        pas01 = r1.MensajeReclamacionIncidenciaPeticion()
        header = self.getHeader('R1', '01')
        pas01.set_agente('1234')
        dades = self.getDatosSolicitud('03', '16')

        variables = r1.VariablesDetalleReclamacion()
        variable = r1.VariableDetalleReclamacion()

        variables.feed({'detalls': [variable]})

        docs = [
            ('01', 'http://eneracme.com/docs/CIE0100001.pdf'),
            ('06', 'http://eneracme.com/docs/INV201509161234.pdf'),
            ('08', 'http://eneracme.com/docs/NIF11111111H.pdf'),
        ]

        documents = []
        for doc in docs:
            tmp_doc = r1.RegistroDoc()
            tmp_doc.feed({'tipus_doc': doc[0], 'url': doc[1]})
            documents.append(tmp_doc)

        reg_documents = r1.RegistrosDocumento()
        reg_doc_vals = {
            'documents': documents,
        }
        reg_documents.feed(reg_doc_vals)

        solicitud = r1.SolicitudReclamacion()
        solicitud.feed({
            'dades': dades,
            'variables': variables,
            'tipus_reclamant': '06',
            'comentaris': u'R1-01 with RegistrosDocumentos Test',
            'reg_documents': reg_documents,
        })
        pas01.feed({
            'capcalera': header,
            'solicitud': solicitud
        })
        pas01.build_tree()
        pas01.pretty_print = True
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_r101_documents.read())

    def test_create_pas01_05_39(self):
        pas01 = r1.MensajeReclamacionIncidenciaPeticion()
        header = r1.CabeceraReclamacion()
        header.feed({
            'proceso': 'R1',
            'paso': '01',
            'solicitud': '201602231255',
            'secuencia': '01',
            'cups': 'ES1234000000000001JN0F',
            'ree_emisora': '0321',
            'ree_destino': '0123',
            'fecha': '2016-02-23T12:54:00',
        })
        pas01.set_agente('0123')
        dades = self.getDatosSolicitud('05', '39', '30968')

        telcon = r1.Telefono()
        telcon.feed({
            'prefijo': '34',
            'numero': '55512345',
        })

        nomcon = r1.Nombre()
        nomcon.feed({
            'nombrepila': 'Perico',
            'apellido1': 'Palotes',
        })

        contacte = r1.Contacto()
        contacte.feed({
            'nombre': nomcon,
            'telefon': telcon,
            'correu': 'perico@acme.com'
        })

        variable = r1.VariableDetalleReclamacion()
        variable.feed({
            'data_incident': '2016-02-08',
            'codidh': '0',
            'codi_incidencia': '02',
            'codi_sollicitud': '201602231236',
            'contacto': contacte,
            'codi_sollicitud_reclamacio': '201602231236',
            'data_inici': '2016-01-01',
            'data_fins': '2016-02-09',
            'import_reclamat': 204.49,
            'ubicacio': 'Cuadro ICP',
        })

        variables = r1.VariablesDetalleReclamacion()
        variables.feed({'detalls': [variable]})

        # Client
        idclient = c1.IdCliente()
        idclient.feed({
            'cifnif': 'NI',
            'identificador': '11111111H',
        })

        nomclient = c1.Nombre()
        nom_vals = {
            'nombrepila': 'Road',
            'apellido1': 'Runner',
            'apellido2': 'Speed'
        }
        nomclient.feed(nom_vals)

        telclient = c1.Telefono()
        telclient.feed({
            'numero': '55512345',
            'prefijo': 34
        })

        client = c1.Cliente()
        cli_fields = {
            'idcliente': idclient,
            'nombre': nomclient,
            'indicador': 'S',
            'correu': 'rrunner@acme.com',
            'telefono': telclient,
        }

        client.feed(cli_fields)

        # Reclamant
        idrec = r1.IdReclamante()
        idrec.feed({
            'tipus_cifnif': 'CI',
            'identificador': '22222222H',
        })

        nomrec = c1.Nombre()
        nomrec.feed({
            'razon': 'ACME Corporation',
        })

        telrec = c1.Telefono()
        telrec.feed({
            'numero': '555987654',
            'prefijo': 34
        })

        reclamant = r1.Reclamante()
        reclamant.feed({
            'id_reclamant': idrec,
            'nom': nomrec,
            'correu': 'reclamaatr@acme.es',
            'telefon': telrec,
        })

        docs = [(
            '06',
            'https://www.dropbox.com/s/q40impgt3tn0vtj/Reclama_%20da%C3%'
            'B1os_%20Montero%20Simon%2C%20Eduardo%20Tarsicio.pdf?dl=0'
        )]

        documents = []
        for doc in docs:
            tmp_doc = r1.RegistroDoc()
            tmp_doc.feed({'tipus_doc': doc[0], 'url': doc[1]})
            documents.append(tmp_doc)

        reg_documents = r1.RegistrosDocumento()
        reg_doc_vals = {
            'documents': documents,
        }
        reg_documents.feed(reg_doc_vals)

        solicitud = r1.SolicitudReclamacion()
        solicitud.feed({
            'dades': dades,
            'variables': variables,
            'client': client,
            'tipus_reclamant': '06',
            'reclamant': reclamant,
            'comentaris': (
                u'su diferencial del cuadro de control se ha quemado, se\n'
                u'            reclama número de incidencia de red exterior para'
                u' tramitación de\n            siniestro'),
            'reg_documents': reg_documents,
        })

        pas01.feed({
            'capcalera': header,
            'solicitud': solicitud
        })
        pas01.build_tree()
        pas01.pretty_print = True
        xml = str(pas01)
        self.assertXmlEqual(xml, self.xml_r101_0539.read())

    def test_create_pas02_ok(self):
        pas02 = r1.MensajeAceptacionReclamacion()
        header = self.getHeader('R1', '02', '201602231255')
        pas02.set_agente('1234')

        dades_acceptacio = r1.DatosAceptacion()
        dades_acceptacio.feed({
            'data_acceptacio': '2016-02-23',
            'codi_reclamacio': '3265349'
        })

        acceptacio = r1.AceptacionReclamacion()
        acceptacio.feed({
            'dades_acceptacio': dades_acceptacio
        })

        pas02.feed({
            'capcalera': header,
            'acceptacio': acceptacio
        })
        pas02.build_tree()
        pas02.pretty_print = True
        xml = str(pas02)
        self.assertXmlEqual(xml, self.xml_r102_ok.read())

    def test_create_pas02_ko(self):
        pas02 = r1.MensajeRechazoReclamacion()
        header = self.getHeader('R1', '02', '201602231255')
        pas02.set_agente('1234')

        dades_acceptacio = r1.DatosAceptacion()
        dades_acceptacio.feed({
            'data_acceptacio': '2016-02-23',
            'codi_reclamacio': '3265349'
        })

        acceptacio = r1.RechazoReclamacion()
        acceptacio.feed({
            'fecha': '2016-02-23'
        })

        rebuigs_data = [
            (1.01, '01', 'Motiu de rebuig 01: No existe Punto de '
                          'Suministro asociado al CUPS'
             ),
            (2.03, '03', 'Cuando el CIF-NIF no coincide con el que figura en '
                          'la base de datos del Distribuidor'
             ),
            (3.11, '11', 'Cuando un comercializador pide cambios de '
                          'comercializador en suministros ya comercializados '
                          'por él o bajas y modificaciones en suministros ya '
                          'no comercializados por él.'
             ),
            (4.36, '36', 'Cuando el CIF-NIF no tiene un formato adecuado '
                          '(algoritmo erróneo o numeración ininteligible)'
             ),
            (5.36, '84', 'Una reclamación duplicada es una reclamación '
                          'exactamente igual a otra pero con distinto número '
                          'de solicitud'
             ),
        ]

        rebuigs = []
        for r in rebuigs_data:
            rebuig = r1.RechazoReclamacion()
            rebuig.feed({
                'secuencial': r[0],
                'motiu': r[1],
                'comentaris': r[2]
            })
            rebuigs.append(rebuig)

        rebuigsreclamacions = r1.RechazosReclamacion()
        rebuigsreclamacions.feed({
            'rebuigs': rebuigs
        })

        pas02.feed({
            'capcalera': header,
            'data': '2016-02-23',
            'rebuigs': rebuigsreclamacions
        })
        pas02.build_tree()
        pas02.pretty_print = True
        xml = str(pas02)
        self.assertXmlEqual(xml, self.xml_r102_ko.read())

    def test_create_pas03_minim(self):
        pas03 = r1.MensajePeticionInformacionAdicionalReclamacion()
        header = self.getHeader('R1', '03', '201412111009')
        header.feed({'fecha': '2016-06-10T08:50:43'})
        pas03.set_agente('1234')
        dades = self.getDatosInformacion('01', '12345678')

        info_adicional = r1.InformacionAdicional()
        info_adicional.feed({
            'dades_informacio': dades,
            'comentaris': u'R103 minimum test.',
        })
        pas03.feed({
            'capcalera': header,
            'informacio_adicional': info_adicional
        })
        pas03.build_tree()
        pas03.pretty_print = True
        xml = str(pas03)
        self.assertXmlEqual(xml, self.xml_r103_minim.read())

    def test_create_pas03_desc_inter(self):
        pas03 = r1.MensajePeticionInformacionAdicionalReclamacion()
        header = self.getHeader('R1', '03', '201412111009')
        header.feed({'fecha': '2016-06-10T08:50:43'})
        pas03.set_agente('1234')

        dades = self.getDatosInformacion('01', '12345678')

        info_intermitja = r1.InformacionIntermedia()
        info_intermitja.feed({
            'desc_info_intermitja': u'Descripcion de la informacion intermedia aportada.',
        })

        info_adicional = r1.InformacionAdicional()
        info_adicional.feed({
            'dades_informacio': dades,
            'info_intermitja': info_intermitja,
            'comentaris': u"R1 03 with 'InformacionIntermedia'.",
        })
        pas03.feed({
            'capcalera': header,
            'informacio_adicional': info_adicional
        })
        pas03.build_tree()
        pas03.pretty_print = True
        xml = str(pas03)
        self.assertXmlEqual(xml, self.xml_r103_desc.read())

    def test_create_pas03_intervenciones(self):
        pas03 = r1.MensajePeticionInformacionAdicionalReclamacion()
        header = self.getHeader('R1', '03', '201412111009')
        header.feed({'fecha': '2016-06-10T08:50:43'})
        pas03.set_agente('1234')

        dades = self.getDatosInformacion('01', '12345678')

        info_intermitja = r1.InformacionIntermedia()
        intervencions = r1.Intervenciones()
        intervencio = r1.Intervencion()
        intervencio.feed({
            'tipus_intervencio': '01',
            'data': '2016-06-10',
            'hora_desde': '08:00:00',
            'hora_fins': '09:00:00',
            'num_visita': '10',
            'resultat': '001',
            'detalls_resultat': u'Descripcion de los resultados obtenidos.',
        })
        intervencio2 = r1.Intervencion()
        intervencio2.feed({
            'tipus_intervencio': '02',
            'data': '2016-06-10',
            'hora_desde': '08:00:00',
            'hora_fins': '09:00:00',
            'num_visita': '10',
            'resultat': '001',
            'detalls_resultat': u'Descripcion de los resultados obtenidos.',
        })
        intervencions.feed({
            'detalls': [intervencio,intervencio2]
        })
        info_intermitja.feed({
            'intervencions': intervencions,
        })

        info_adicional = r1.InformacionAdicional()
        info_adicional.feed({
            'dades_informacio': dades,
            'info_intermitja': info_intermitja,
            'comentaris': u"R1 03 with 'InformacionIntermedia'.",
        })
        pas03.feed({
            'capcalera': header,
            'informacio_adicional': info_adicional
        })
        pas03.build_tree()
        pas03.pretty_print = True
        xml = str(pas03)
        self.assertXmlEqual(xml, self.xml_r103_inter.read())

    def test_create_pas03_retipificacion(self):
        pas03 = r1.MensajePeticionInformacionAdicionalReclamacion()
        header = self.getHeader('R1', '03', '201412111009')
        header.feed({'fecha': '2016-06-10T08:50:43'})
        pas03.set_agente('1234')

        dades = self.getDatosInformacion('01', '12345678')

        dades_retipificacio = r1.Retificacion()
        dades_retipificacio.feed({
            'tipus': '02',
            'subtipus': '03',
            'descripcio_retificacio': 'descripcio de la retipificacio.'
        })

        info_adicional = r1.InformacionAdicional()
        info_adicional.feed({
            'dades_informacio': dades,
            'retificacio': dades_retipificacio,
            'comentaris': u"R1 03 with 'Retipificacion'.",
        })
        pas03.feed({
            'capcalera': header,
            'informacio_adicional': info_adicional
        })
        pas03.build_tree()
        pas03.pretty_print = True
        xml = str(pas03)
        self.assertXmlEqual(xml, self.xml_r103_retip.read())

    def test_create_pas03_solicitudes(self):
        pas03 = r1.MensajePeticionInformacionAdicionalReclamacion()
        header = self.getHeader('R1', '03', '201412111009')
        header.feed({'fecha': '2016-06-10T08:50:43'})
        pas03.set_agente('1234')

        dades = self.getDatosInformacion('01', '12345678')

        solicituds = r1.SolicitudesInformacionAdicional()
        solicitud = r1.SolicitudInformacionAdicional()
        solicitud.feed({
            'tipus_info': '01',
            'desc_peticio_info': u'Descripcion de la peticion.',
            'data_limit': '2016-07-10'
        })
        solicitud2 = r1.SolicitudInformacionAdicional()
        solicitud2.feed({
            'tipus_info': '02',
            'desc_peticio_info': u'Descripcion de la peticion.',
            'data_limit': '2016-07-10'
        })
        solicituds.feed({
            'detalls': [solicitud, solicitud2]
        })

        info_adicional = r1.InformacionAdicional()
        info_adicional.feed({
            'dades_informacio': dades,
            'sollicituds_info_adicional' : solicituds,
            'comentaris': u"R1 03 with 'SolicitudesInformacionAdicional'.",
        })
        pas03.feed({
            'capcalera': header,
            'informacio_adicional': info_adicional
        })
        pas03.build_tree()
        pas03.pretty_print = True
        xml = str(pas03)
        self.assertXmlEqual(xml, self.xml_r103_solicitudes.read())

    def test_create_pas04_variables(self):
        pas04 = r1.MensajeEnvioInformacionReclamacion()
        header = self.getHeader('R1', '04', '201650008314')
        header.feed({'fecha': '2016-01-22T10:09:41'})
        pas04.set_agente('0123')

        dades = r1.DatosEnvioInformacion()
        dades.feed({
            'num_expedient': '0123456789ABCD',
            'data_informacio': '2016-01-20',
        })

        variables = r1.VariablesAportacionInformacion()
        var1 = r1.VariableAportacionInformacion()
        var1.feed({
            'tipus_info': '01',
            'desc_peticio_info': 'Informacio per fer testos.',
            'variable': '01',
            'valor': '125',
        })
        var2 = r1.VariableAportacionInformacion()
        var2.feed({
            'tipus_info': '02',
        })
        variables.feed({
            'detalls': [var1, var2],
        })

        enviament_info_reclamacio = r1.EnvioInformacionReclamacion()
        enviament_info_reclamacio.feed({
            'dades_enviament_info': dades,
            'variables_aportacio_info': variables,
            'comentaris': u'R104 test with VariablesAportacionInformacion.',
        })
        pas04.feed({
            'capcalera': header,
            'enviament_info_reclamacio': enviament_info_reclamacio
        })
        pas04.build_tree()
        pas04.pretty_print = True
        xml = str(pas04)
        self.assertXmlEqual(xml, self.xml_r104_variables.read())

    def test_create_pas04_reg_doc(self):
        pas04 = r1.MensajeEnvioInformacionReclamacion()
        header = self.getHeader('R1', '04', '201650008314')
        header.feed({'fecha': '2016-01-22T10:09:41'})
        pas04.set_agente('0123')

        dades = r1.DatosEnvioInformacion()
        dades.feed({
            'data_informacio': '2016-01-20',
        })

        docs = r1.RegistrosDocumento()
        doc1 = r1.RegistroDoc()
        doc1.feed({
            'tipus_doc': '01',
            'url': 'http://eneracme.com/docs/CIE0100001.pdf',
        })
        doc2 = r1.RegistroDoc()
        doc2.feed({
            'tipus_doc': '06',
            'url': 'http://eneracme.com/docs/INV201509161234.pdf',
        })
        doc3 = r1.RegistroDoc()
        doc3.feed({
            'tipus_doc': '08',
            'url': 'http://eneracme.com/docs/NIF11111111H.pdf',
        })

        docs.feed({
            'documents': [doc1, doc2, doc3],
        })

        enviament_info_reclamacio = r1.EnvioInformacionReclamacion()
        enviament_info_reclamacio.feed({
            'dades_enviament_info': dades,
            'comentaris': ' ',
            'reg_doc': docs,
        })
        pas04.feed({
            'capcalera': header,
            'enviament_info_reclamacio': enviament_info_reclamacio
        })
        pas04.build_tree()
        pas04.pretty_print = True
        xml = str(pas04)
        self.assertXmlEqual(xml, self.xml_r104_reg_doc.read())

    def test_create_pas05(self):
        pas05 = r1.MensajeCierreReclamacion()
        header = self.getHeader('R1', '05', '201604111738')
        pas05.set_agente('1234')

        dades_tancament = r1.DatosCierre()
        dades_tancament.feed({
            'data': '2016-04-12',
            'hora': '16:02:25',
            'tipus': '03',
            'subtipus': '13',
            'codi_reclamacio_distri': '3291970',
            'resultat_reclamacio': '02',
            'observacions': u'Les informamos, que si se recibe solicitud de '
                            u'otra comercializadora sobre el punto de '
                            u'suministro, en los formatos establecidos y la '
                            u'misma se acepta, el comercializador es custodia '
                            u'de la documentación que acredita esa '
                            u'contratación. No obstante nuestra recomendación '
                            u'es que sea el cliente quién contacte con la '
                            u'Comercializadora entrante y les requiera la '
                            u'anulación de dicha solicitud. Les comunicamos a',
            'indemnitzacio_abonada': '0.0',
            'data_moviment': '2016-04-12',
            'codi_sollicitud': '201604111738',
        })

        tancament = r1.CierreReclamacion()
        tancament.feed({
            'dades': dades_tancament,
            'cod_contracte': '383922379',
            'comentaris': u'Les informamos, que si se recibe solicitud de otra '
                          u'comercializadora sobre el punto de suministro, en '
                          u'los formatos establecidos y la misma se acepta, el '
                          u'comercializador es custodia de la documentación '
                          u'que acredita esa contratación. No obstante nuestra '
                          u'recomendación es que sea el cliente quién contacte '
                          u'con la Comercializadora entrante y les requiera '
                          u'la anulación de dicha solicitud. Les comunicamos '
                          u'a su vez, que lo que están solicitando '
                          u'consideramos, no es una reclamación, es una '
                          u'petición, debiendo gestionarla como tal en '
                          u'lo sucesivo.'
        })

        pas05.feed({
            'capcalera': header,
            'tancament': tancament,
        })

        pas05.build_tree()
        pas05.pretty_print = True
        xml = str(pas05)
        self.assertXmlEqual(xml, self.xml_r105.read())

    def test_create_pas05_retipificacio(self):
        pas05 = r1.MensajeCierreReclamacion()
        header = self.getHeader('R1', '05', '201604111738')
        pas05.set_agente('1234')

        dades_tancament = r1.DatosCierre()
        dades_tancament.feed({
            'data': '2016-04-12',
            'hora': '16:02:25',
            'tipus': '03',
            'subtipus': '13',
            'codi_reclamacio_distri': '3291970',
            'resultat_reclamacio': '02',
            'observacions': u'Les informamos, que si se recibe solicitud de '
                            u'otra comercializadora sobre el punto de '
                            u'suministro, en los formatos establecidos y la '
                            u'misma se acepta, el comercializador es custodia '
                            u'de la documentación que acredita esa '
                            u'contratación. No obstante nuestra recomendación '
                            u'es que sea el cliente quién contacte con la '
                            u'Comercializadora entrante y les requiera la '
                            u'anulación de dicha solicitud. Les comunicamos a',
            'indemnitzacio_abonada': '0.0',
            'data_moviment': '2016-04-12',
            'codi_sollicitud': '201604111738',
        })
        dades_retipificacio = r1.Retificacion()
        dades_retipificacio.feed({
            'tipus': '02',
            'subtipus': '03',
            'descripcio_retificacio': 'descripcio de la retipificacio.'
        })
        tancament = r1.CierreReclamacion()
        tancament.feed({
            'dades': dades_tancament,
            'retificacio': dades_retipificacio,
            'cod_contracte': '383922379',
            'comentaris': u'Les informamos, que si se recibe solicitud de otra '
                          u'comercializadora sobre el punto de suministro, en '
                          u'los formatos establecidos y la misma se acepta, el '
                          u'comercializador es custodia de la documentación '
                          u'que acredita esa contratación. No obstante nuestra '
                          u'recomendación es que sea el cliente quién contacte '
                          u'con la Comercializadora entrante y les requiera '
                          u'la anulación de dicha solicitud. Les comunicamos '
                          u'a su vez, que lo que están solicitando '
                          u'consideramos, no es una reclamación, es una '
                          u'petición, debiendo gestionarla como tal en '
                          u'lo sucesivo.'
        })

        pas05.feed({
            'capcalera': header,
            'tancament': tancament,
        })

        pas05.build_tree()
        pas05.pretty_print = True
        xml = str(pas05)
        self.assertXmlEqual(xml, self.xml_r105_retipificacio.read())

    def test_read_r101_minim(self):
        self.r101_xml = R1(self.xml_r101_minim)
        self.r101_xml.set_xsd()
        self.r101_xml.parse_xml()
        sollicitud = self.r101_xml.sollicitud
        tipus_reclamant = self.r101_xml.tipus_reclamant
        reclamant = self.r101_xml.reclamant
        reclamacions = self.r101_xml.reclamacions
        client = self.r101_xml.client
        comentaris = self.r101_xml.comentaris
        documents = self.r101_xml.documents

        assert sollicitud.tipus == '03'
        assert sollicitud.subtipus == '16'
        assert tipus_reclamant == '06'
        assert reclamacions == []
        assert client is None
        assert reclamant is None
        assert comentaris == 'R1-01 minimum Test'
        assert documents == []

    def test_read_lectures(self):
        self.r101_xml = R1(self.xml_r101_lectures)
        self.r101_xml.set_xsd()
        self.r101_xml.parse_xml()
        sollicitud = self.r101_xml.sollicitud
        reclamacions = self.r101_xml.reclamacions
        tipus_reclamant = self.r101_xml.tipus_reclamant
        client = self.r101_xml.client
        comentaris = self.r101_xml.comentaris
        documents = self.r101_xml.documents

        assert sollicitud.tipus == '02'
        assert sollicitud.subtipus == '36'
        assert tipus_reclamant == '06'

        assert len(reclamacions) == 1
        reclamacio = reclamacions[0]

        assert reclamacio.contacto is None
        assert reclamacio.num_factura_atr == '243615'
        assert reclamacio.data_lectura == '2016-01-20'
        assert reclamacio.codidh == 2
        lecturas = []
        for lect in reclamacio.lectures:
            lecturas.append(
                (lect.integrador,
                 int(lect.codigo_periodo_dh),
                 '%.2f' % float(lect.lectura_propuesta))
            )
        assert len(lecturas) == 2
        assert lecturas[0] == ('AE', 21, '1162.00')
        assert lecturas[1] == ('AE', 22, '3106.00')

        assert client is not None
        assert client.codi_identificacio == '11111111H'
        assert client.correu == 'perico@acme.com'
        assert client.telf_prefix == '34'
        assert client.telf_num == '66612345'
        assert client.get_nom_complet() == 'Palotes Largos, Perico'

        assert comentaris == 'R1-01 lectures'

        assert documents == []

    def test_read_r101_documents(self):
        self.r101_xml = R1(self.xml_r101_documents)
        self.r101_xml.set_xsd()
        self.r101_xml.parse_xml()
        sollicitud = self.r101_xml.sollicitud
        tipus_reclamant = self.r101_xml.tipus_reclamant
        reclamant = self.r101_xml.reclamant
        reclamacions = self.r101_xml.reclamacions
        client = self.r101_xml.client
        comentaris = self.r101_xml.comentaris
        documents = self.r101_xml.documents

        assert sollicitud.tipus == '03'
        assert sollicitud.subtipus == '16'
        assert tipus_reclamant == '06'
        assert reclamacions == []
        assert client is None
        assert reclamant is None
        assert comentaris == 'R1-01 with RegistrosDocumentos Test'

        assert len(documents) == 3
        assert documents[0].doc_type == '01'
        assert documents[0].url == 'http://eneracme.com/docs/CIE0100001.pdf'
        assert documents[1].doc_type == '06'
        assert documents[1].url == (
            'http://eneracme.com/docs/INV201509161234.pdf'
        )
        assert documents[2].doc_type == '08'
        assert documents[2].url == 'http://eneracme.com/docs/NIF11111111H.pdf'

    def test_read_r101_0539(self):
        self.r101_xml = R1(self.xml_r101_0539)
        self.r101_xml.set_xsd()
        self.r101_xml.parse_xml()
        sollicitud = self.r101_xml.sollicitud
        reclamacions = self.r101_xml.reclamacions
        tipus_reclamant = self.r101_xml.tipus_reclamant
        reclamant = self.r101_xml.reclamant
        client = self.r101_xml.client
        comentaris = self.r101_xml.comentaris
        documents = self.r101_xml.documents

        assert sollicitud.tipus == '05'
        assert sollicitud.subtipus == '39'
        assert tipus_reclamant == '06'

        assert len(reclamacions) == 1
        reclamacio = reclamacions[0]

        assert reclamacio.contacto is not None
        assert reclamacio.data_incident == '2016-02-08'
        assert reclamacio.data_lectura is None
        assert reclamacio.codidh == 0
        assert reclamacio.codi_incidencia == '02'
        assert reclamacio.codi_sollicitud == '201602231236'
        assert reclamacio.contacto.correu == 'perico@acme.com'
        assert reclamacio.contacto.get_nom_complet() == 'Palotes, Perico'
        assert reclamacio.codi_sollicitud_reclamacio == '201602231236'
        assert reclamacio.data_inici == '2016-01-01'
        assert reclamacio.data_fins == '2016-02-09'
        assert reclamacio.import_reclamat == 204.49
        assert reclamacio.ubicacio == 'Cuadro ICP'

        assert client is not None
        assert client.codi_identificacio == '11111111H'
        assert client.correu == 'rrunner@acme.com'
        assert client.get_nom_complet() == 'Runner Speed, Road'

        assert reclamant is not None
        assert reclamant.codi_identificacio == '22222222H'
        assert reclamant.correu == 'reclamaatr@acme.es'
        assert reclamant.get_nom_complet() == 'ACME Corporation'

        assert 100 < len(comentaris) < 4000

        assert len(documents) == 1
        assert documents[0].doc_type == '06'
        assert documents[0].url == (
            u'https://www.dropbox.com/s/q40impgt3tn0vtj/Reclama_%20da%C3%B1os_'
            u'%20Montero%20Simon%2C%20Eduardo%20Tarsicio.pdf?dl=0'
        )

    def test_read_r101_0203(self):
        self.r101_xml = R1(self.xml_r101_0203)
        self.r101_xml.set_xsd()
        self.r101_xml.parse_xml()
        sollicitud = self.r101_xml.sollicitud
        reclamacions = self.r101_xml.reclamacions
        tipus_reclamant = self.r101_xml.tipus_reclamant
        reclamant = self.r101_xml.reclamant
        client = self.r101_xml.client
        comentaris = self.r101_xml.comentaris
        documents = self.r101_xml.documents

        assert sollicitud.tipus == '02'
        assert sollicitud.subtipus == '03'
        assert tipus_reclamant == '01'

        assert len(reclamacions) == 1
        reclamacio = reclamacions[0]

        assert reclamacio.contacto is not None
        assert reclamacio.num_factura_atr == '243615'
        assert reclamacio.data_incident is None
        assert reclamacio.data_lectura == '2016-01-20'
        assert reclamacio.codidh == 1
        assert reclamacio.codi_incidencia == '01'
        assert reclamacio.codi_sollicitud is None
        assert reclamacio.contacto.correu == 'perico@acme.com'
        assert reclamacio.contacto.get_nom_complet() == 'Palotes Largos, Perico'
        assert reclamacio.contacto.telf_num == '55512345'
        assert reclamacio.codi_sollicitud_reclamacio is None
        assert reclamacio.data_inici is None
        assert reclamacio.data_fins is None
        assert reclamacio.import_reclamat is None
        assert reclamacio.ubicacio is None

        assert client is not None
        assert client.codi_identificacio == '11111111H'
        assert client.correu == 'perico@acme.com'
        assert client.get_nom_complet() == 'Palotes Largos, Perico'

        assert reclamant is not None
        assert reclamant.codi_identificacio == '11111111H'
        assert reclamant.correu == ''
        assert reclamant.telf_prefix == '34'
        assert reclamant.telf_num == '66612345'
        assert reclamant.get_nom_complet() == 'Palotes Largos, Perico'

        assert 100 < len(comentaris) < 4000

        assert len(documents) == 0

    def test_read_r101_multi(self):
        self.r101_xml = R1(self.xml_r101_multivar)
        self.r101_xml.set_xsd()
        self.r101_xml.parse_xml()
        sollicitud = self.r101_xml.sollicitud
        reclamacions = self.r101_xml.reclamacions
        tipus_reclamant = self.r101_xml.tipus_reclamant
        reclamant = self.r101_xml.reclamant
        client = self.r101_xml.client
        comentaris = self.r101_xml.comentaris
        documents = self.r101_xml.documents

        assert sollicitud.tipus == '02'
        assert sollicitud.subtipus == '03'
        assert tipus_reclamant == '01'

        assert len(reclamacions) == 2
        reclamacio = reclamacions[0]

        assert reclamacio.contacto is not None
        assert reclamacio.num_factura_atr == '243615'
        assert reclamacio.data_incident is None
        assert reclamacio.data_lectura == '2016-01-20'
        assert reclamacio.codidh == 1
        assert reclamacio.codi_incidencia == '01'
        assert reclamacio.codi_sollicitud is None
        assert reclamacio.contacto.correu == 'perico@acme.com'
        assert reclamacio.contacto.get_nom_complet() == 'Palotes Largos, Perico'
        assert reclamacio.contacto.telf_num == '55512345'
        assert reclamacio.codi_sollicitud_reclamacio is None
        assert reclamacio.data_inici is None
        assert reclamacio.data_fins is None
        assert reclamacio.import_reclamat is None
        assert reclamacio.ubicacio is None

        assert reclamacions[1].contacto.get_nom_complet() == 'Palotes2 Largos2, Perico2'

        assert client is not None
        assert client.codi_identificacio == '11111111H'
        assert client.correu == 'perico@acme.com'
        assert client.get_nom_complet() == 'Palotes Largos, Perico'

        assert reclamant is not None
        assert reclamant.codi_identificacio == '11111111H'
        assert reclamant.correu == ''
        assert reclamant.telf_prefix == '34'
        assert reclamant.telf_num == '66612345'
        assert reclamant.get_nom_complet() == 'Palotes Largos, Perico'

        assert 100 < len(comentaris) < 4000

        assert len(documents) == 0

    def test_read_r102_ok(self):
        self.r102_xml = R1(self.xml_r102_ok)
        self.r102_xml.set_xsd()
        self.r102_xml.parse_xml()
        acceptacio = self.r102_xml.acceptacio

        assert acceptacio.data_acceptacio == '2016-02-23'
        assert acceptacio.codi_reclamacio_distri == '3265349'

    def test_read_r102_ko(self):
        self.r102_xml = R1(self.xml_r102_ko)
        self.r102_xml.set_xsd()
        self.r102_xml.parse_xml()
        rebuig = self.r102_xml.rebuig

        assert self.r102_xml.data == '2016-02-23'
        assert len(rebuig) == 5

    def test_read_r103(self):
        self.r103_xml = R1(self.xml_r103_minim)
        self.r103_xml.set_xsd()
        self.r103_xml.parse_xml()

        self.r103_desc = R1(self.xml_r103_desc)
        self.r103_desc.set_xsd()
        self.r103_desc.parse_xml()

        self.r103_inter = R1(self.xml_r103_inter)
        self.r103_inter.set_xsd()
        self.r103_inter.parse_xml()

        self.r103_retip = R1(self.xml_r103_retip)
        self.r103_retip.set_xsd()
        self.r103_retip.parse_xml()

        self.r103_solicitudes = R1(self.xml_r103_solicitudes)
        self.r103_solicitudes.set_xsd()
        self.r103_solicitudes.parse_xml()

        dades_informacio = self.r103_xml.informacio_adicional.dades_informacio
        informacio_intermitja_desc = self.r103_desc.informacio_adicional.informacio_intermitja
        informacio_intermitja_inter = self.r103_inter.informacio_adicional.informacio_intermitja
        retipificacio = self.r103_retip.informacio_adicional.retipificacio
        sollicituds_info_addicional = self.r103_solicitudes.informacio_adicional.sollicituds_info_addicional
        comentaris = self.r103_xml.informacio_adicional.comentaris

        assert dades_informacio.tipus_comunicacio == '01'
        assert dades_informacio.codi_reclamacio_distri == '12345678'

        if informacio_intermitja_desc:
            assert not informacio_intermitja_desc.intervencions
            assert informacio_intermitja_desc.descripcio_info_intermitja == \
                'Descripcion de la informacion intermedia aportada.'

        if informacio_intermitja_inter:
            assert not informacio_intermitja_inter.descripcio_info_intermitja
            assert len(informacio_intermitja_inter.intervencions) < 10
            intervencio = informacio_intermitja_inter.intervencions[0]
            assert intervencio.tipus_intervencio == '01'
            assert intervencio.data == '2016-06-10'
            assert intervencio.hora_desde == '08:00:00'
            assert intervencio.hora_fins == '09:00:00'
            assert intervencio.numero_visita == '10'
            assert intervencio.resultat == '001'
            assert intervencio.detall_resultat == \
                'Descripcion de los resultados obtenidos.'
            intervencio2 = informacio_intermitja_inter.intervencions[1]
            assert intervencio2.tipus_intervencio == '02'
            assert intervencio2.data == '2016-06-10'
            assert intervencio2.hora_desde == '08:00:00'
            assert intervencio2.hora_fins == '09:00:00'
            assert intervencio2.numero_visita == '10'
            assert intervencio2.resultat == '001'
            assert intervencio2.detall_resultat == \
                   'Descripcion de los resultados obtenidos.'

        if retipificacio:
            assert retipificacio.tipus == '02'
            assert retipificacio.subtipus == '03'
            assert retipificacio.descripcio_retipificacio == \
                'descripcio de la retipificacio.'

        if sollicituds_info_addicional:
            solicitud = sollicituds_info_addicional[0]
            assert solicitud.tipus_info_adicional == '01'
            assert solicitud.descripcio_peticio_informacio == 'Descripcion de la peticion.'
            assert solicitud.data_limit == '2016-07-10'
            solicitud2 = sollicituds_info_addicional[1]
            assert solicitud2.tipus_info_adicional == '02'
            assert solicitud2.descripcio_peticio_informacio == 'Descripcion de la peticion.'
            assert solicitud2.data_limit == '2016-07-10'

        assert len(comentaris) > 10

    def test_read_r104(self):
        self.r104_var_xml = R1(self.xml_r104_variables)
        self.r104_var_xml.set_xsd()
        self.r104_var_xml.parse_xml()

        info_rec = self.r104_var_xml.envio_informacion_reclamacion

        assert info_rec.num_expedient_acometida == '0123456789ABCD'
        assert info_rec.data_informacio == '2016-01-20'
        assert len(info_rec.comentaris) > 10
        assert len(info_rec.documents) == 0
        assert len(info_rec.variables_aportacio_informacio) == 2

        var1 = info_rec.variables_aportacio_informacio[0]
        assert var1.tipus_informacio == '01'
        assert var1.desc_peticio_informacio == 'Informacio per fer testos.'
        assert var1.variable == '01'
        assert var1.valor == '125'

        self.r104_reg_xml = R1(self.xml_r104_reg_doc)
        self.r104_reg_xml.set_xsd()
        self.r104_reg_xml.parse_xml()

        info_rec = self.r104_reg_xml.envio_informacion_reclamacion

        assert not info_rec.num_expedient_acometida
        assert info_rec.data_informacio == '2016-01-20'
        assert len(info_rec.documents) == 3
        assert len(info_rec.variables_aportacio_informacio) == 0

        reg1 = info_rec.documents[0]
        assert reg1.doc_type == '01'
        assert reg1.url == 'http://eneracme.com/docs/CIE0100001.pdf'

    def test_read_r105(self):
        self.r105_xml = R1(self.xml_r105)
        self.r105_xml.set_xsd()
        self.r105_xml.parse_xml()

        tancament = self.r105_xml.tancament
        dades_tancament = tancament.dades_tancament

        assert tancament.codi_contracte == '383922379'
        assert len(tancament.comentaris) > 10

        assert dades_tancament.data == '2016-04-12'
        assert dades_tancament.hora == '16:02:25'
        assert dades_tancament.tipus == '03'
        assert dades_tancament.subtipus == '13'
        assert dades_tancament.codi_reclamacio_distri == '3291970'
        assert dades_tancament.resultat_reclamacio == '02'
        assert dades_tancament.detall_resultat == ''
        assert len(dades_tancament.observacions) > 10
        assert dades_tancament.indemnitzacio_abonada == 0.0
        assert dades_tancament.num_expedient_anomalia_frau == ''
        assert dades_tancament.data_moviment == '2016-04-12'
        assert dades_tancament.codi_sollicitud == '201604111738'

    def test_read_r105_retipificacio(self):
        self.r105_xml_retipificacio = R1(self.xml_r105_retipificacio)
        self.r105_xml_retipificacio.set_xsd()
        self.r105_xml_retipificacio.parse_xml()

        tancament = self.r105_xml_retipificacio.tancament
        dades_tancament = tancament.dades_tancament
        dades_retipificacio = tancament.retipificacio

        assert tancament.codi_contracte == '383922379'
        assert len(tancament.comentaris) > 10

        assert dades_tancament.data == '2016-04-12'
        assert dades_tancament.hora == '16:02:25'
        assert dades_tancament.tipus == '03'
        assert dades_tancament.subtipus == '13'
        assert dades_tancament.codi_reclamacio_distri == '3291970'
        assert dades_tancament.resultat_reclamacio == '02'
        assert dades_tancament.detall_resultat == ''
        assert len(dades_tancament.observacions) > 10
        assert dades_tancament.indemnitzacio_abonada == 0.0
        assert dades_tancament.num_expedient_anomalia_frau == ''
        assert dades_tancament.data_moviment == '2016-04-12'
        assert dades_tancament.codi_sollicitud == '201604111738'
        assert dades_retipificacio.tipus == '02'
        assert dades_retipificacio.subtipus == '03'
        assert dades_retipificacio.descripcio_retipificacio == 'descripcio de la retipificacio.'

    def test_accept_no_sollicitud(self):
        text_to_elim = '        <DatosSolicitud>\n' \
                       '            <Tipo>03</Tipo>\n' \
                       '            <Subtipo>16</Subtipo>\n' \
                       '        </DatosSolicitud>\n'

        r101_no_text_xml = R1(
            self.xml_r101_minim.read().replace(text_to_elim, '')
        )
        r101_no_text_xml.set_xsd()
        r101_no_text_xml.parse_xml(validate=False)

        assert r101_no_text_xml.sollicitud is False

    def test_accept_no_reclamacions(self):
        text_to_elim = '        <VariablesDetalleReclamacion>\n' \
                       '            <VariableDetalleReclamacion/>\n' \
                       '        </VariablesDetalleReclamacion>\n'

        r101_no_text_xml = R1(
            self.xml_r101_minim.read().replace(text_to_elim, '')
        )
        r101_no_text_xml.set_xsd()
        r101_no_text_xml.parse_xml(validate=False)

        assert r101_no_text_xml.reclamacions == []

    def test_accept_no_id_type(self):
        text_to_elim = '        <TipoReclamante>06</TipoReclamante>\n'

        r101_no_text_xml = R1(
            self.xml_r101_minim.read().replace(text_to_elim, ''))
        r101_no_text_xml.set_xsd()
        r101_no_text_xml.parse_xml(validate=False)

        assert r101_no_text_xml.tipus_reclamant == ''

    def test_accept_no_cond_cont(self):
        text_to_elim = '        <Comentarios>R1-01 minimum Test</Comentarios>\n'

        r101_no_text_xml = R1(
            self.xml_r101_minim.read().replace(text_to_elim, ''))
        r101_no_text_xml.set_xsd()
        r101_no_text_xml.parse_xml(validate=False)

        assert r101_no_text_xml.comentaris == ''

    def test_get_subtipus(self):
        from switching.input.messages.R1 import get_subtypes
        self.assertEqual(get_subtypes('01'), ['01', '02', '38'])
        r101 = R1(self.xml_r101_minim)
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(
            r101.get_subtypes(),
            ['13', '14', '15', '16', '17', '34', '35', '45', '48']
        )

    def test_get_tipus(self):
        from switching.input.messages.R1 import get_type_from_subtype
        self.assertEqual(get_type_from_subtype('01'), '01')
        self.assertEqual(get_type_from_subtype('38'), '01')
        self.assertEqual(get_type_from_subtype('20'), '05')
        r101 = R1(self.xml_r101_minim)
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(r101.get_type_from_subtype(), '03')

    def test_minimum_fields(self):
        xml_r101_text = self.xml_r101_0539.read()

        # check:
        # 'nif_cliente', 'nombre_cliente', 'telefono_contacto', 'cups',
        # 'fecha_incidente', 'comentarios', 'persona_de_contacto',
        # 'tipo_atencion_incorrecta'
        xml_r101_text_aux = xml_r101_text.replace('<Subtipo>39', '<Subtipo>01')
        info = '<TipoDeAtencionIncorrecta>01</TipoDeAtencionIncorrecta>'
        r101 = R1(xml_r101_text_aux.replace(
            '</CodigoSolicitud>', '</CodigoSolicitud>{0}'.format(info)))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'codigo_incidencia'
        r101 = R1(xml_r101_text.replace('<Subtipo>39', '<Subtipo>03'))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'num_fact', 'tipo_concepto_facturado'
        xml_r101_text_aux = xml_r101_text.replace('<Subtipo>39', '<Subtipo>08')
        info_factura = "<NumFacturaATR>11A</NumFacturaATR>" \
                       "<TipoConceptoFacturado>10</TipoConceptoFacturado>"
        r101 = R1(xml_r101_text_aux.replace(
            '</FechaIncidente>', '</FechaIncidente>{0}'.format(info_factura)))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'lectura', 'fecha_de_lectura'
        r101 = R1(self.xml_r101_lectures)
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'fecha_desde', 'fecha_hasta', 'ubicacion_incidente'
        r101 = R1(xml_r101_text.replace('<Subtipo>39', '<Subtipo>24'))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'codigo_de_solicitud', 'concepto_contratacion'
        xml_r101_text_aux = xml_r101_text.replace('<Subtipo>39', '<Subtipo>34')
        info_sol = "<ParametroContratacion>01</ParametroContratacion>"
        r101 = R1(xml_r101_text_aux.replace(
            '</CodigoSolicitud>', '</CodigoSolicitud>{0}'.format(info_sol)))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'cta_banco'
        xml_r101_text_aux = xml_r101_text.replace('<Subtipo>39', '<Subtipo>14')
        info_sol = "<IBAN>0000000000000</IBAN>"
        r101 = R1(xml_r101_text_aux.replace(
            '</CodigoSolicitud>', '</CodigoSolicitud>{0}'.format(info_sol)))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'sol_nuevos_suministros'
        xml_r101_text_aux = xml_r101_text.replace('<Subtipo>39', '<Subtipo>18')
        info = "<NumExpedienteAcometida>123A</NumExpedienteAcometida>"
        r101 = R1(xml_r101_text_aux.replace(
            '<FechaIncidente>', '{0}<FechaIncidente>'.format(info)))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'cod_reclam_anterior'
        r101 = R1(xml_r101_text.replace('<Subtipo>39', '<Subtipo>23'))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check:
        # 'importe_reclamado'
        r101 = R1(xml_r101_text.replace('<Subtipo>39', '<Subtipo>21'))
        r101.set_xsd()
        r101.parse_xml()
        self.assertEqual(len(r101.check_minimum_fields()), 0)

        # check falten camps minims
        r101 = R1(self.xml_r101_minim.read().replace(
            '<Subtipo>16', '<Subtipo>01'))
        r101.set_xsd()
        r101.parse_xml()
        self.assertGreater(len(r101.check_minimum_fields()), 0)


class SwitchingParseValidate(unittest.TestCase):

    def test_parse_with_valid_xml(self):
        valid_xml = open(get_data("a301.xml"), "r")
        valid_xml_text = valid_xml.read()
        valid_xml = A3(valid_xml_text)
        valid_xml.set_xsd()
        self.assertIsNone(valid_xml.valid)
        self.assertIsNone(valid_xml.error)
        valid_xml.parse_xml(validate=True)
        self.assertTrue(valid_xml.valid)
        self.assertFalse(valid_xml.error)

    def test_parse_with_validation(self):
        tipo_cont_atr = '            <TipoContratoATR>01</TipoContratoATR>\n'
        valid_xml = open(get_data("a301.xml"), "r")
        valid_xml_text = valid_xml.read()
        invalid_xml = A3(valid_xml_text.replace(tipo_cont_atr, ''))
        invalid_xml.set_xsd()

        callable_obj = (lambda: invalid_xml.parse_xml(validate=True))
        self.assertRaises(message.except_f1, callableObj=callable_obj)
        self.assertIsNone(invalid_xml.obj)
        self.assertFalse(invalid_xml.valid)
        self.maxDiff = None
        self.assertEqual(
            invalid_xml.error,
            u"Element '{http://localhost/elegibilidad}CondicionesContractuales'"
            u": This element is not expected. Expected is one of ( "
            u"{http://localhost/elegibilidad}TipoAutoconsumo, "
            u"{http://localhost/elegibilidad}TipoContratoATR ).")

    def test_parse_without_validation(self):
        tipo_cont_atr = '            <TipoContratoATR>01</TipoContratoATR>\n'
        valid_xml = open(get_data("a301.xml"), "r")
        valid_xml_text = valid_xml.read()
        invalid_xml = A3(valid_xml_text.replace(tipo_cont_atr, ''))

        invalid_xml.set_xsd()
        invalid_xml.parse_xml(validate=False)
        self.assertFalse(invalid_xml.valid)
        self.assertEqual(
            invalid_xml.error,
            u"Element '{http://localhost/elegibilidad}CondicionesContractuales'"
            u": This element is not expected. Expected is one of ( "
            u"{http://localhost/elegibilidad}TipoAutoconsumo, "
            u"{http://localhost/elegibilidad}TipoContratoATR ).")
        invalid_xml.set_tipus()

        # Various checks to make sure the XML is correctly imported
        self.assertEqual(invalid_xml.tipus, 'A3')
        self.assertEqual(invalid_xml.pas, '01')
        self.assertEqual(invalid_xml.get_pas_xml(), '01')
        self.assertEqual(invalid_xml.get_codi_emisor, '1234')
        self.assertEqual(invalid_xml.get_codi_destinatari, '4321')
        self.assertEqual(invalid_xml.get_codi, 'ES1234000000000001JN0F')
        self.assertEqual(invalid_xml.cups, 'ES1234000000000001JN0F')
        self.assertEqual(invalid_xml.codi_sollicitud, '201412111009')
        self.assertEqual(invalid_xml.seq_sollicitud, '01')
        self.assertEqual(invalid_xml.data_sollicitud, '2014-04-16 22:13:37')
        self.assertEqual(invalid_xml.versio, '02')

        self.assertEqual(invalid_xml.sollicitud.linia_negoci, '01')
        self.assertEqual(invalid_xml.sollicitud.cnae, '9820')
        self.assertEqual(invalid_xml.contracte.condicions.tarifa, '001')
        self.assertEqual(invalid_xml.client.nom, 'Perico')
        self.assertEqual(invalid_xml.client.cognom_1, 'Palote')
        self.assertEqual(invalid_xml.client.cognom_2, u'Pérez')
        self.assertEqual(invalid_xml.mesura.equip_aportat_client, 'N')
        self.assertEqual(invalid_xml.mesura.tipus_equip_mesura, 'L00')

        # We also check that the field we deleted is empty
        self.assertEqual(invalid_xml.contracte.tipus_contracte, '')

if __name__ == '__main__':
    unittest.main()
