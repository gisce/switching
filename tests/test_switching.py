#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.input.messages import F1, message, W1
from switching.output.messages import sw_w1 as w1
from switching.output.messages import sw_c1 as c1
from switching.output.messages import sw_c2 as c2
from switching.output.messages import sw_m1 as m1
from switching.output.messages import sw_a3 as a3
from switching.output.messages import sw_r1 as r1
from switching.output.messages.base import Cabecera
from . import unittest

from .test_helpers import get_data


#@unittest.skip('uncommited data')
class Switching_F1_Test(unittest.TestCase):
    """test de switching"""
    def setUp(self):
        self.xml = open(get_data("F1_exemple.xml"), "r")
        self.xml_err = open(get_data("F1_exemple_err.xml"), "r")
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
        sup = supportClass()
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


class SwitchingA3Test(unittest.TestCase):
    """test de A3"""

    def setUp(self):
        sup = supportClass()
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


class SwitchingM1Test(unittest.TestCase):
    """test de M1"""

    def setUp(self):
        sup = supportClass()
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


class Switching_R1_Test(unittest.TestCase):
    """test de R1"""

    def setUp(self):
        sup = supportClass()
        self.xml_r101_minim = open(get_data("r101_minim.xml"), "r")
        self.xml_r101_reclamant = open(get_data("r101_reclamante.xml"), "r")
        self.xml_r101_client = open(get_data("r101_cliente.xml"), "r")
        self.xml_r101_documents = open(get_data("r101_documentos.xml"), "r")
        # r1-02
        self.xml_r102_ok = open(get_data("r102_aceptacion.xml"), "r")
        self.xml_r102_ko = open(get_data("r102_rechazo.xml"), "r")

        self.client = sup.getCliente(True)
        self.reclamant = self.getReclamante()

    def tearDown(self):
        self.xml_r101_minim.close()
        self.xml_r101_reclamant.close()
        self.xml_r101_client.close()
        self.xml_r101_documents.close()

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


if __name__ == '__main__':
    unittest.main()
