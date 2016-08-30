#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.output.messages.sw_c1 import (
    Contacto, CondicionesContractuales, PotenciasContratadas
)
from switching.output.messages.sw_c2 import CiePapel, DatosCie, DocTecnica,\
    RegistroDoc, RegistrosDocumento
from switching.output.messages.mesures import NoICP, ICP, DatosAparato

from . import unittest
import os
import decimal
import sys

from .test_helpers import get_data
from copy import copy, deepcopy

from switching.defs import *


class test_Defs(unittest.TestCase):

    def test_tables(self):
        assert TIPUS_ACTIVACIO[0][0] == 'L'
        assert TIPUS_ACTIVACIO[0][1] == 'En ciclo de lectura'
        assert ESTAT_TEL_PM[0][0] == '1'
        assert ESTAT_TEL_PM[0][1] == 'Correcto'
        assert TABLA_111[0][0] == '01'
        assert TABLA_111[0][1] == u'Telegestión Operativa con Curva de Carga Horaria'


class test_Contacto(unittest.TestCase):
    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        pass

    def test_build_tree_simple(self):
        c = Contacto()
        c.set_data(
            es_persona_juridica=False,
            nom="Perico",
            cognom_1="Palote",
            cognom_2=u"Pérez",
            telefon='',
            prefix='',
        )
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('Contacto_simple.xml'))

    def test_build_tree_juridica(self):
        c = Contacto()
        c.set_data(
            es_persona_juridica=True,
            nom="Acme",
            cognom_1="",
            cognom_2="",
            telefon='',
            prefix='',
        )
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('Contacto_juridica.xml'))

    def test_build_tree_with_phone(self):
        c = Contacto()
        c.set_data(
            es_persona_juridica=False,
            nom="Perico",
            cognom_1="Palote",
            cognom_2=u"Pérez",
            telefon='555123123',
            prefix='',
        )
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('Contacto_withphone.xml'))

    def test_build_tree_with_prefix(self):
        c = Contacto()
        c.set_data(
            es_persona_juridica=False,
            nom="Perico",
            cognom_1="Palote",
            cognom_2=u"Pérez",
            telefon='555123123',
            prefix='01',
        )
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('Contacto_withprefix.xml'))

    def test_build_tree_with_email(self):
        c = Contacto()
        c.set_data(
            es_persona_juridica=False,
            nom="Perico",
            cognom_1="Palote",
            cognom_2=u"Pérez",
            telefon='555123123',
            prefix='01',
            correu='ppalote@acme.com'
        )
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('Contacto_withemail.xml'))


class test_CiePapel(unittest.TestCase):

    basic_data = {}

    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        self.basic_data = {
            'codigo_cie': '1234567',
            'potencia_inst_bt': 3500,
            'fecha_emision': '2015-06-04',
            'nif_instalador': '12345678Z',
            'nombre_instalador': 'Acme',
            'tension_suministro': '10',
            'tipo_suministro': 'VI', }

    def test_build_tree_simple(self):
        c = CiePapel()
        c.feed(self.basic_data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('CiePapel_simple.xml'))

    def test_build_tree_codigo_instalador(self):
        c = CiePapel()
        data = copy(self.basic_data)
        data.update({'codigo_instalador': '987654321'})
        del data['nif_instalador']
        c.feed(data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('CiePapel_codinst.xml'))

    def test_build_tree_fecha_caducidad(self):
        c = CiePapel()
        data = copy(self.basic_data)
        data.update({'fecha_caducidad': '9999-01-01'})
        c.feed(data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('CiePapel_caducidad.xml'))

    def test_build_tree_diferencial(self):
        c = CiePapel()
        data = copy(self.basic_data)
        data.update({'intensidad_diferencial': 20,
                     'sensibilidad_diferencial': 300})
        c.feed(data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('CiePapel_diferencial.xml'))

    def test_build_tree_seccion(self):
        c = CiePapel()
        data = copy(self.basic_data)
        data.update({'seccion_cable': 16})
        c.feed(data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('CiePapel_seccion.xml'))


class test_DatosCie(unittest.TestCase):

    basic_data = {}

    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        cie_paper = CiePapel()
        cie_paper_data = {
            'codigo_cie': '1234567',
            'potencia_inst_bt': 3500,
            'fecha_emision': '2015-06-04',
            'nif_instalador': '12345678Z',
            'nombre_instalador': 'Acme',
            'tension_suministro': '10',
            'tipo_suministro': 'VI', }
        cie_paper.feed(cie_paper_data)
        self.basic_data = {'cie_electronico': 'N',
                           'cie_papel': cie_paper}

    def test_build_tree_simple(self):
        c = DatosCie()
        c.feed(self.basic_data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('DatosCie_simple.xml'))


class test_DocTecnica(unittest.TestCase):

    basic_data = {}

    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        cie_paper = CiePapel()
        cie_paper.feed({
            'codigo_cie': '1234567',
            'potencia_inst_bt': 3500,
            'fecha_emision': '2015-06-04',
            'nif_instalador': '12345678Z',
            'nombre_instalador': 'Acme',
            'tension_suministro': '10',
            'tipo_suministro': 'VI', })
        dades_cie = DatosCie()
        dades_cie.feed({'cie_electronico': 'N',
                        'cie_papel': cie_paper})
        self.basic_data = {'datos_cie': dades_cie}

    def test_build_tree_simple(self):
        c = DocTecnica()
        c.feed(self.basic_data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('DocTecnica_simple.xml'))


class test_registro_documento:

    basic_data = {}

    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        dades = [
            ('01', 'http://eneracme.com/docs/CIE0100001.pdf'),
            ('06', 'http://eneracme.com/docs/INV201509161234.pdf'),
            ('08', 'http://eneracme.com/docs/NIF11111111H.pdf'),
        ]

        registro_documentos = RegistrosDocumento()
        docs = []
        for i in range(len(dades)):
            doc = RegistroDoc()
            doc.feed({
                'tipo': dades[i][0],
                'url': dades[i][1],
            })
            docs.append(doc)

        self.basic_data = {'registro': docs}

    def test_build_tree_simple(self):
        documentos = RegistrosDocumento()
        documentos.feed(self.basic_data)
        documentos.build_tree()
        xml = str(documentos)
        self.assertXmlEqual(xml, self.loadFile('RegistroDocumento_simple.xml'))


class test_CondicionesContractuales(unittest.TestCase):

    basic_data = {}

    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def test_build_tree_simple(self):
        potencies = PotenciasContratadas()

        pots = {'p1': 4400}
        potencies.feed(pots)

        c = CondicionesContractuales()
        c.feed({
            'tarifaATR': '001',
            'periodicidad_facturacion': '01',
            'tipus_telegestio': '03',
            'control_potencia': '1',
            'potencies': potencies,
        })

        c.feed(self.basic_data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile('CondContractuales.xml'))


    def test_build_tree_medida_baja(self):
        potencies = PotenciasContratadas()

        pots = {'p1': 44000, 'p2': 44000, 'p3': 44000}
        potencies.feed(pots)

        c = CondicionesContractuales()
        c.feed({
            'tarifaATR': '011',
            'periodicidad_facturacion': '01',
            'tipus_telegestio': '03',
            'control_potencia': '1',
            'potencies': potencies,
            'marca_mesura_bt_perdues': 'S',
            'kvas_trafo': 50,
            'perc_perd_pactades': 5,
        })

        c.feed(self.basic_data)
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(
            xml, self.loadFile('CondContractualesMedidaBaja.xml')
        )


class test_NoICP(unittest.TestCase):
    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        pass

    def test_build_NoIntegradores(self):
        c = NoICP()
        c.feed({
            'periode_fabricacio': 2015,
            'num_serie': '753855',
            'funcio': 'M',
            'num_integradors': 0,
            'constant_energia': 1.0,
            'constant_max': 1.0,
            'enters': 1,
            'decimals': 0,
        })
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile(
            'DatosAparatoNoICPSinIntegradores.xml'
        ))

    def test_build_Integradores(self):
        c = NoICP()
        c.feed({
            'periode_fabricacio': 2015,
            'num_serie': '753855',
            'funcio': 'M',
            'num_integradors': 20,
            'constant_energia': 1.0,
            'constant_max': 1.0,
            'enters': 1,
            'decimals': 0,
        })
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile(
            'DatosAparatoNoICPConIntegradores.xml'
        ))


class test_DatosAparato(unittest.TestCase):
    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        pass

    def test_build_NoIntegradores(self):
        c = DatosAparato()
        c.feed({
            'periode_fabricacio': 2015,
            'num_serie': '753855',
            'funcio': 'M',
            'num_integradors': 0,
            'constant_energia': 1.0,
            'constant_max': 1.0,
            'enters': 1,
            'decimals': 0,
        })
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile(
            'DatosAparatoSinIntegradores.xml'
        ))

    def test_build_Integradores(self):
        c = DatosAparato()
        c.feed({
            'periode_fabricacio': 2015,
            'num_serie': '753855',
            'funcio': 'M',
            'num_integradors': 20,
            'constant_energia': 1.0,
            'constant_max': 1.0,
            'enters': 1,
            'decimals': 0,
        })
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile(
            'DatosAparatoConIntegradores.xml'
        ))


class test_ICP(unittest.TestCase):
    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return f.read()

    def setUp(self):
        pass

    def test_build_NoIntegradores(self):
        c = ICP()
        c.feed({
            'periode_fabricacio': 2015,
            'num_serie': '753855',
            'funcio': 'M',
            'num_integradors': 0,
            'constant_energia': 1.0,
            'constant_max': 1.0,
            'enters': 1,
            'decimals': 0,
        })
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile(
            'DatosAparatoICPSinIntegradores.xml'
        ))

    def test_build_Integradores(self):
        c = ICP()
        c.feed({
            'periode_fabricacio': 2015,
            'num_serie': '753855',
            'funcio': 'M',
            'num_integradors': 20,
            'constant_energia': 1.0,
            'constant_max': 1.0,
            'enters': 1,
            'decimals': 0,
        })
        c.build_tree()
        xml = str(c)
        self.assertXmlEqual(xml, self.loadFile(
            'DatosAparatoICPConIntegradores.xml'
        ))


if __name__ == '__main__':
    unittest.main()
