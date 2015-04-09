#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.input.messages import F1, message
from switching.output.messages import sw_w1 as w1
from switching.output.messages.base import Cabecera
import os
import unittest


# TODO: Move this to a common module
def assertXmlEqual(self, got, want):
    from lxml.doctestcompare import LXMLOutputChecker
    from doctest import Example

    checker = LXMLOutputChecker()
    if checker.check_output(want, got, 0):
        return
    message = checker.output_difference(Example("", want), got, 0)
    raise AssertionError(message)

unittest.TestCase.assertXmlEqual = assertXmlEqual
unittest.TestCase.__str__ = unittest.TestCase.id


_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)


#@unittest.skip('uncommited data')
class Switching_F1_Test(unittest.TestCase):
    """test de switching"""
    def setUp(self):
        self.xml = open(get_data("F1_exemple.xml"), "r")
        self.xml_err = open(get_data("F1_exemple_err.xml"), "r")
        self.xml_con = open(get_data("F1_concepte_exemple.xml"), "r")

    def test_F1(self):
        f1 = F1(self.xml_con)
        tipus = f1.get_tipus_xml()
        f1.parse_xml()
        ch_emisor = '0316'
        emisor = f1.get_codi_emisor
        self.assertEqual(tipus, 'F1')
        self.assertEqual(emisor, ch_emisor)


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
            'ree_emisora': '0762',
            'ree_destino': '0021',
            'fecha': '2014-04-16T22:13:37',
            }
        header.feed(vals)
        return header


class Switching_W1_Test(unittest.TestCase):
    """test de W1"""

    def setUp(self):
        self.xml_w101 = open(get_data("w101.xml"), "r")
#        self.xml_w102_ok = open(get_data("w102-aceptacion.xml"), "r")
#        self.xml_w102_ko = open(get_data("w102-rebuig.xml"), "r")


    def test_create_pas01(self):
        sup = supportClass()
        pas01 = w1.SolicitudAportacionLectura()
        header = sup.getHeader('W1', '01')
        pas01.set_agente('1234')
        lecturas = []
        for integrador, periodo, medida in [
            ('AE', 21, '0000001162.00'),
            ('AE', 22, '0000003106.00'),
            ]:
            lectura = w1.LecturaAportada()
            lectura.feed(dict(
                integrador = integrador,
                codigo_periodedh = periodo,
                lectura_propuesta = medida,
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
        self.assertXmlEqual(self.xml_w101.read(), xml)


if __name__ == '__main__':
    unittest.main()

