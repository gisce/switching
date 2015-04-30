#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.input.messages import F1, message
import unittest
import os
import decimal
import sys

import test_helpers

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, 'data', path)


class test_F1(unittest.TestCase):
    """test de switching"""
    def setUp(self):
        self.xml = open(get_data("F1_exemple.xml"), "r")
        self.xml_err = open(get_data("F1_exemple_err.xml"), "r")
        self.xml_con = open(get_data("F1_concepte_exemple.xml"), "r")

    @unittest.skip("Not implemented yet")
    def test_F1(self):
        f1 = F1(self.xml_con)
        tipus = f1.get_tipus_xml()
        f1.parse_xml()
        ch_emisor = '0316'
        emisor = f1.get_codi_emisor
        self.assertEqual(tipus, 'F1')
        self.assertEqual(emisor, ch_emisor)

if __name__ == '__main__':
    unittest.main()
