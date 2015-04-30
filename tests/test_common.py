#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.output.messages.sw_c1 import Contacto
import unittest
import os
import decimal
import sys

import test_helpers

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, 'data', path)


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
        self.assertXmlEqual(xml,self.loadFile('Contacto_simple.xml'))



if __name__ == '__main__':
    unittest.main()
