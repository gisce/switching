from . import unittest
from .test_helpers import get_data

from switching.input.messages import message, TG


class TestS04(unittest.TestCase):

    def setUp(self):
        self.xml = open(get_data('S04_0_20150504125253.xml'), "r")
        self.tg_xml = message.MessageTG(self.xml)
        self.tg_xml.parse_xml()

    def tearDown(self):
        self.xml.close()

    def test_fix_sagecom_FFFFFFFFFFFFFFFFFW(self):
        for cnc in self.tg_xml.obj.Cnc:
            concentrator = TG.Concentrator(cnc)
            values = TG.Values(None, None, None)
            for meter in concentrator.get_meters():
                if meter.name.startswith('SAG'):
                    for s4 in meter.meter.S04:
                        if s4.get('Fx') == 'FFFFFFFFFFFFFFFFFW':
                            self.assertEqual(
                                values.get_timestamp(s4, 'Fx'),
                                '1900-01-01 00:00:00'
                            )


class TestS05(unittest.TestCase):

    def setUp(self):
        self.xml = open(get_data('S05_2Ctr.xml'), "r")
        self.tg_xml = message.MessageTG(self.xml)
        self.tg_xml.parse_xml()

    def tearDown(self):
        self.xml.close()

    def test_select_contract_1(self):
        version = self.tg_xml.version
        ctrs = {}
        for cnc in self.tg_xml.obj.Cnc:
            concentrator = TG.Concentrator(cnc)
            for meter in concentrator.get_meters():
                if meter.name == 'ZIV0036301516':
                    values = TG.Values(meter, 'S05', version)
                    for value in values.get():
                        contract = str(value['contract'])
                        ctrs.setdefault(contract, 0)
                        ctrs[contract] += 1
        assert len(ctrs.keys()) == 2
        assert ctrs['1'] == 14
        assert ctrs['2'] == 14


class TestS12(unittest.TestCase):

    def setUp(self):
        self.xml = open(get_data('S12'),'r')
        self.tg_xml = message.MessageTG(self.xml)
        self.tg_xml.parse_xml()

    def tearDown(self):
        self.xml.close()

    def test_get_S12(self):
        for concentrator_xml in self.tg_xml.obj.Cnc:
            concentrator_tg = TG.Concentrator(concentrator_xml)
            values = TG.Values(concentrator_tg,'S12',self.tg_xml.version)
            values.get()
