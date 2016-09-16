# coding=utf-8
import unittest

from lxml import etree

from .test_helpers import get_data


class TestBase(unittest.TestCase):

    def loadFile(self, filename):
        with open(get_data(filename), "r") as f:
            return self.read(f)

    def read(self, f):
        tree = etree.fromstring(f.read().encode('utf-8'))
        return etree.tostring(
            tree,
            xml_declaration=False,
            pretty_print=False,
            encoding='unicode'
        )
