#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.input.messages import F1, message
from switching.output.messages.base import Cabecera
from switching.output.messages import sw_p0 as p0

import unittest
import os
import decimal
import sys

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, 'data', path)


# class test_F1(unittest.TestCase):
#     """test de switching"""
#     def setUp(self):
#         self.xml = open(get_data("F1_exemple.xml"), "r")
#         self.xml_err = open(get_data("F1_exemple_err.xml"), "r")
#         #self.xml_con = open(get_data("F1_concepte_exemple.xml"), "r")
#
#     def test_F1(self):
#         f1 = F1(self.xml_con)
#         tipus = f1.get_tipus_xml()
#         f1.parse_xml()
#         ch_emisor = '0316'
#         emisor = f1.get_codi_emisor
#         self.assertEqual(tipus, 'F1')
#         self.assertEqual(emisor, ch_emisor)

class supportClass(object):
    """Funcions de suport"""
    def getHeader(self, process='C1', step='01'):
        header = Cabecera()
        vals = {'proceso': process,
                'solicitud': '20141211100908',
                'secuencia': '01',
                'codigo': 'ES1234000000000001JN0F',
                'ree_emisora': '1234',
                'ree_destino': '4321',
                'paso': step,
                'fecha': '2014-04-16'}
        header.feed(vals)
        return header

class testSw(unittest.TestCase):
    """Test genèric SW ATR"""

    def setUp(self):
        self.xml_cap = open(get_data("capcalera.xml"), "r")

    def test_header(self):
        """"generic header"""
        sup = supportClass()
        header = sup.getHeader(process='C1', step='01')
        header.build_tree()
        xml = str(header)

        self.assertEqual(self.xml_cap.read(), xml)


class testSwP0(unittest.TestCase):
    """test de P0"""
    def setUp(self):
        self.xml_p101 = open(get_data("p101.xml"), "r")
        self.xml_p102 = open(get_data("p102-rechazo.xml"), "r")

    def test_create_pas01(self):
        sup = supportClass()
        pas01 = p0.MensajeSolicitudInformacionAlRegistrodePS()
        header = sup.getHeader('P0', '01')
        pas01.set_agente('1234')
        pas01.feed({'capcalera': header})
        pas01.build_tree()

        xml = str(pas01)
        self.assertEqual(self.xml_p101.read(), xml)

    def test_create_pas02(self):
        sup = supportClass()
        pas02 = p0.MensajeRechazoSolicitudInfRegistroPS()
        header = sup.getHeader('P0', '02')
        pas02.set_agente('1234')
        datos_rechazo = p0.DatosRechazo()
        datos_rechazo.feed({'motivo': '05'})
        rechazo = p0.RechazoSolicitudInfRegistroPS()
        rechazo.feed({'datos_rechazo': datos_rechazo})
        pas02.feed({'capcalera': header,
                    'rechazo_solicitud': rechazo})
        pas02.build_tree()

        xml = str(pas02)

        self.assertEqual(self.xml_p102.read(), xml)

    def test_create_pas03(self):
        sup = supportClass()
        pas03 = p0.EnvioInformacionAlRegistroDePuntosDeSuministro()
        header = sup.getHeader('P0', '03')
        pas03.set_agente('1234')

        pas03.feed({'capcalera': header})
        pas03.build_tree()
        pas03.pretty_print = True
        xml = str(pas03)
        print xml

        #self.assertEqual(self.xml_p102.read(), xml)

if __name__ == '__main__':
    unittest.main()
