#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.input.messages import F1, message, W1, A3, FacturaATR, Q1
from switching.output.messages import sw_w1 as w1
from switching.output.messages import sw_c1 as c1
from switching.output.messages import sw_c2 as c2
from switching.output.messages import sw_m1 as m1
from switching.output.messages import sw_a3 as a3
from switching.output.messages.base import Cabecera
from . import unittest

from .test_helpers import get_data


#@unittest.skip('uncommited data')
class Switching_F1_Test(unittest.TestCase):
    """test de switching"""
    def setUp(self):
        self.xml = open(get_data("F1_exemple.xml"), "r")
        self.xml_err = open(get_data("F1_exemple_err.xml"), "r")
        self.xml_no_medidas = open(get_data("F1_no_medidas.xml"), "r")
        #self.xml_con = open(get_data("F1_concepte_exemple.xml"), "r")

    @unittest.skip("Not implemented yet")
    def test_F1(self):
        f1 = F1(self.xml_con)
        tipus = f1.get_tipus_xml()
        f1.parse_xml()
        ch_emisor = '0316'
        emisor = f1.get_codi_emisor
        self.assertEqual(tipus, 'F1')
        self.assertEqual(emisor, ch_emisor)

    def test_get_info_activa(self):
        f1 = F1(self.xml)
        f1.parse_xml()
        f1_atr = f1.get_factures()['FacturaATR'][0]
        periodes, total = f1_atr.get_info_activa()
        periode = periodes[0]
        self.assertEqual(total, 74.1424)
        self.assertEqual(periode.name, 'P1')
        self.assertEqual(periode.data_inici, '2010-03-01')
        self.assertEqual(periode.data_final, '2010-04-30')

    def test_get_info_activa_no_medidas(self):
        f1 = F1(self.xml_no_medidas)
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
        self.w102_xml.parse_xml()
        date = ''
        if self.w102_xml.aceptacion:
            date = self.w102_xml.aceptacion.fecha_aceptacion
        assert date == '2015-07-02'

    def test_read_w102_ko(self):
        self.w102_xml = W1(self.xml_w102_ko)
        self.w102_xml.parse_xml()
        date = ''
        reason = ''
        if not self.w102_xml.aceptacion:
            date = self.w102_xml.rechazo.fecha_rechazo
            reason = self.w102_xml.rechazo.motivo_rechazo
        assert date == '2015-07-02'
        assert reason == '01'


class SwitchingC2Test(unittest.TestCase):
    """test de C2"""

    def setUp(self):
        self.xml_c201 = open(get_data("c201.xml"), "r")
        self.xml_c201_ciepapel = open(get_data("c201_CiePapel.xml"), "r")

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
        idclient = c1.IdCliente()
        idclient.feed({
            'cifnif': 'DN',
            'identificador': '11111111H',
        })

        nomclient = c1.Nombre()
        nom = {'nombrepila': 'Carla',
               'apellido1': 'Aramberri',
               'apellido2': 'Cadenas'}
        nomclient.feed(nom)

        telefon = c1.Telefono()
        telf_fields = {
            'numero': '71407365',
            'prefijo': 34
        }
        telefon.feed(telf_fields)

        self.client = c1.Cliente()
        cli_fields = {
            'idcliente': idclient,
            'nombre': nomclient,
            'indicador': 'S',
            'telefono': telefon,
        }
        self.client.feed(cli_fields)

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


class SwitchingA3Test(unittest.TestCase):
    """test de A3"""

    def setUp(self):
        self.xml_a301 = open(get_data("a301.xml"), "r")
        self.xml_a301_ciepapel = open(get_data("a301_CiePapel.xml"), "r")

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

        #client
        idclient = c1.IdCliente()
        idclient.feed({
            'cifnif': 'DN',
            'identificador': '11111111H',
        })

        nomclient = c1.Nombre()
        nom = {'nombrepila': 'Carla',
               'apellido1': 'Aramberri',
               'apellido2': 'Cadenas'}
        nomclient.feed(nom)

        telefon = c1.Telefono()
        telf_fields = {
            'numero': '71407365',
            'prefijo': 34
        }
        telefon.feed(telf_fields)

        self.client = c1.Cliente()
        cli_fields = {
            'idcliente': idclient,
            'nombre': nomclient,
            'indicador': 'S',
            'telefono': telefon,
        }
        self.client.feed(cli_fields)

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

    def test_read_a301(self):
        self.a301_xml = A3(self.xml_a301)
        self.a301_xml.parse_xml()
        contract = self.a301_xml.contracte
        mesures = self.a301_xml.mesura
        comentaris = self.a301_xml.comentaris
        assert contract.codi_contracte == '111111111'
        assert mesures.cp_installacio == 'Y'
        assert mesures.mesura.TipoEquipoMedida == 'L00'
        assert isinstance(comentaris, list)

    def test_read_a301_ciepapel(self):
        self.a301_xml_ciepapel = A3(self.xml_a301_ciepapel)
        self.a301_xml_ciepapel.parse_xml()
        contract = self.a301_xml_ciepapel.contracte

        ciepapel = self.a301_xml_ciepapel.obj.PasoMRAMLConCambiosRestoTarifa\
            .DocTecnica.DatosCie.CIEPapel
        assert contract.codi_contracte == '111111111'
        assert ciepapel.CodigoCie.text == '1234567'


class SwitchingM1Test(unittest.TestCase):
    """test de M1"""

    def setUp(self):
        self.xml_m101 = open(get_data("m101.xml"), "r")
        self.xml_m101_ciepapel = open(get_data("m101_CiePapel.xml"), "r")

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
        idclient = c1.IdCliente()
        idclient.feed({
            'cifnif': 'DN',
            'identificador': '11111111H',
        })

        nomclient = c1.Nombre()
        nom = {'nombrepila': 'Carla',
               'apellido1': 'Aramberri',
               'apellido2': 'Cadenas'}
        nomclient.feed(nom)

        telefon = c1.Telefono()
        telf_fields = {
            'numero': '71407365',
            'prefijo': 34
        }
        telefon.feed(telf_fields)

        self.client = c1.Cliente()
        cli_fields = {
            'idcliente': idclient,
            'nombre': nomclient,
            'indicador': 'S',
            'telefono': telefon,
        }
        self.client.feed(cli_fields)

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

if __name__ == '__main__':
    unittest.main()
