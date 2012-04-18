# -*- coding: utf-8 -*-

from datetime import datetime

class Concentrator(object):
    """Implements concentrator"""

    def __init__(self, concentrator):
        self.concentrator = concentrator

    @property
    def name(self):
        return self.concentrator.get('Id')

    def get_meters(self):
        '''Return all Meters in the concentrator'''
        return [Meter(x) for x in self.concentrator.Cnt]


class Meter(object):
    '''Implements meter'''

    def __init__(self, meter):
        self.meter = meter

    @property
    def name(self):
        return self.meter.get('Id')

    @property
    def multiplier(self):
        return self.meter.get('Magn')


class Values(object):
    '''return values'''

    def __init__(self, meter, report_type):
        self.report_type = report_type
        self.meter = meter

    def get(self):
        '''generic get function'''
        return getattr(self, 'get_%s' % self.report_type)

    def get_S02(self):
        '''get function for S02 type values'''
        meter_name = self.meter.name
        magn = self.meter.multiplier
        ret_values = []
        for value in self.meter.S02:
            timestamp = datetime.strftime(datetime.\
                                          strptime(value.get('Fh')[:-1],
                                                            '%Y%m%d%H%M%S'),
                                          '%Y-%m-%d %H:%M:%S')
            ret_values.append({'name': meter_name,
                               'timestamp': timestamp, 
                               'season':value.get('Fh')[-1:],
                               'magn': magn,
                               'ai': value.get('AI'),
                               'ae': value.get('AE'),
                               'r1': value.get('R1'),
                               'r2': value.get('R2'),
                               'r3': value.get('R3'),
                               'r4': value.get('R4'),
                               })

        return ret_values
