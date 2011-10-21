#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.messages import F1
import unittest
import os
import decimal

from switching.types import DecimalElement

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)

class test_F1(unittest.TestCase):
    """test de switching"""
    
    def setUp(self):
        self.xml = open(get_data("F1_exemple.xml"), "r")
        self.xml_err = open(get_data("F1_exemple_err.xml"), "r")

    def test_F1(self):
        f1 = F1(self.xml)
        tipus = f1.get_tipus_xml()
        obj = f1.parse_xml()
        dec_str = str(decimal.Decimal('21.3458'))
        obj_str = str(obj.Facturas.FacturaATR.Potencia.ImporteTotalTerminoPotencia)
        self.assertEqual(tipus, 'F1')
        self.assertEqual(obj_str, dec_str)

if __name__ == '__main__':
    unittest.main()
