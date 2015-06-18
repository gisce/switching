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
