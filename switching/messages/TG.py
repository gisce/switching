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
        if len(self.concentrator.getchildren()):
            return [Meter(x, self.name) for x in self.concentrator.Cnt]
        return []


class Meter(object):
    '''Implements meter'''

    def __init__(self, meter, cnc_name):
        self.meter = meter
        self.cnc_name = cnc_name
        self.errors = {}
        self.get_errors()

    def get_errors(self):
        if self.meter.get('ErrCat'):
            self.errors = {'errcat': self.meter.get('ErrCat'),
                           'errcode': self.meter.get('ErrCode')}

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
        #If the meter has no children, nothing to do
        if not len(self.meter.meter.getchildren()):
            return {}
        return getattr(self, 'get_%s' % self.report_type)()

    def get_timestamp(self, element, value):
        return datetime.strftime(datetime.\
                        strptime(element.get(value)[:-1],
                                 '%Y%m%d%H%M%S'),
                                 '%Y-%m-%d %H:%M:%S')

    def get_S02(self):
        '''get function for S02 type values'''
        meter_name = self.meter.name
        magn = self.meter.multiplier
        ret_values = []
        for value in self.meter.meter.S02:
            timestamp = self.get_timestamp(value, 'Fh')
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

    def get_S05(self):
        '''get function for S05 type values'''
        meter_name = self.meter.name
        ret_values = []
        for S05_header in self.meter.meter.S05:
            timestamp = self.get_timestamp(S05_header, 'Fh')
            value = 'a'
            tmp_vals = {'name': meter_name,
                        'type': 'day',
                        'value': value,
                        'date_begin': timestamp,
                        'date_end': timestamp,
                        'contract': int(S05_header.get('Ctr')),
                        'period': int(S05_header.get('Pt')),
                        'cnc_name': self.meter.cnc_name,
                        }
            for S05_values in S05_header.Value:
                tmp_vals.update({'ai': int(S05_values.get('AI%s' % value)),
                                 'ae': int(S05_values.get('AE%s' % value)),
                                 'r1': int(S05_values.get('R1%s' % value)),
                                 'r2': int(S05_values.get('R2%s' % value)),
                                 'r3': int(S05_values.get('R3%s' % value)),
                                 'r4': int(S05_values.get('R4%s' % value)),
                                 })
                ret_values.append(tmp_vals)

        return ret_values

    def get_S04(self):
        '''get function for S04 type values'''
        meter_name = self.meter.name
        ret_values = []
        for S04_header in self.meter.meter.S04:
            date_begin = self.get_timestamp(S04_header, 'Fhi')
            date_end = self.get_timestamp(S04_header, 'Fhf')
            date_max = self.get_timestamp(S04_header, 'Fx')
            tmp_vals = {'name': meter_name,
                        'type': 'month',
                        'date_begin': date_begin,
                        'date_end': date_end,
                        'contract': int(S04_header.get('Ctr')),
                        'period': int(S04_header.get('Pt')),
                        'max': int(S04_header.get('Mx')),
                        'date_max': date_max,
                        'cnc_name': self.meter.cnc_name,
                        }
            for S04_values in S04_header.Value:
                if S04_values.get('AIa'):
                    value = 'a'
                else:
                    value = 'i'
                tmp_vals.update({'ai': int(S04_values.get('AI%s' % value)),
                                 'ae': int(S04_values.get('AE%s' % value)),
                                 'r1': int(S04_values.get('R1%s' % value)),
                                 'r2': int(S04_values.get('R2%s' % value)),
                                 'r3': int(S04_values.get('R3%s' % value)),
                                 'r4': int(S04_values.get('R4%s' % value)),
                                 'value': value,
                                 })
                ret_values.append(tmp_vals)

        return ret_values
