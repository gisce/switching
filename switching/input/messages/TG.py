# -*- coding: utf-8 -*-

from datetime import datetime

class Concentrator(object):
    """Implements concentrator"""

    def __init__(self, concentrator):
        self.concentrator = concentrator

    @property
    def name(self):
        return self.concentrator.get('Id')

    @property
    def has_meters(self):
        '''return True if concentrator has meter child tags'''
        if hasattr(self.concentrator, 'Cnt'):
            return True
        else:
            return False

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

    def __init__(self, meter, report_type, version):
        self.report_type = report_type
        self.version = version
        self.meter = meter

    def get(self):
        '''generic get function'''
        #if meter is a concentrator instance
        if isinstance(self.meter, Concentrator):
            if not len(self.meter.concentrator.getchildren()):
                return {}
        #If the meter has no children, nothing to do
        if isinstance(self.meter, Meter):
            if not len(self.meter.meter.getchildren()):
                return {}
        return getattr(self, 'get_%s' % self.report_type)()

    def get_timestamp(self, element, value):
        if len(element.get(value)) > 15:
            date_value = element.get(value)[0:14] + element.get(value)[-1]
        else:
            date_value = element.get(value)
        # Ugly fix for SAGECOM which puts this timestamp when the period doesn't
        # affect the contracted tariff
        if \
                date_value.upper() == 'FFFFFFFFFFFFFFW' \
                or \
                date_value == '00000000000000W':
            date_value = '19000101000000W'
        return datetime.strftime(datetime.\
                        strptime(date_value[:-1],
                                 '%Y%m%d%H%M%S'),
                                 '%Y-%m-%d %H:%M:%S')

    def get_boolean(self, element, value):
        return element.get(value) == 'Y' and True or False

    def get_S02(self):
        '''get function for S02 type values'''
        meter_name = self.meter.name
        magn = int(self.meter.multiplier)
        ret_values = []
        for value in self.meter.meter.S02:
            timestamp = self.get_timestamp(value, 'Fh')
            ret_values.append({'name': meter_name,
                               'cnc_name': self.meter.cnc_name,
                               'timestamp': timestamp, 
                               'season':value.get('Fh')[-1:],
                               'magn': magn,
                               'ai': float(value.get('AI')),
                               'ae': float(value.get('AE')),
                               'r1': float(value.get('R1')),
                               'r2': float(value.get('R2')),
                               'r3': float(value.get('R3')),
                               'r4': float(value.get('R4')),
                               'bc': value.get('Bc')
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
            common_vals = {'name': meter_name,
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
                tmp_vals = common_vals.copy()
                if S04_values.get('AIa'):
                    value_value = 'a'
                else:
                    value_value = 'i'
                tmp_vals.update({'ai': int(S04_values.get('AI%s' % value_value)),
                                 'ae': int(S04_values.get('AE%s' % value_value)),
                                 'r1': int(S04_values.get('R1%s' % value_value)),
                                 'r2': int(S04_values.get('R2%s' % value_value)),
                                 'r3': int(S04_values.get('R3%s' % value_value)),
                                 'r4': int(S04_values.get('R4%s' % value_value)),
                                 'value': value_value,
                                 })
                ret_values.append(tmp_vals)

        return ret_values

    def get_S12(self):
        '''get function for S12 type values'''
        cnc_name = self.meter.name
        ret_values = []
        for S12_header in self.meter.concentrator.S12:
            timestamp = self.get_timestamp(S12_header, 'Fh')
            if self.version == '3.1c':
                fw_up_to_field = 'TimeOutMeterFwU'
            else:
                fw_up_to_field = 'TimeOutPrimeFwU'
            #Els concentradors current retornen el camp IPftp1
            rpt_ftp_ip_address = (S12_header.get('IPftp', False)
                                  or S12_header.get('IPftp1'))
            vals = {
                'date': timestamp,
                'model': S12_header.get('Mod'),
                'mf_year': S12_header.get('Af'),
                'type': S12_header.get('Te'),
                'w_password': S12_header.get('DCPwdAdm'),
                'r_password': S12_header.get('DCPwdRead'),
                'fw_version': S12_header.get('Vf'),
                'fw_comm_version': S12_header.get('VfComm'),
                'protocol': S12_header.get('Pro'),
                'communication': S12_header.get('Com'),
                'battery_mon': S12_header.get('Bat'),
                'ip_address': S12_header.get('ipCom'),
                'dc_ws_port': S12_header.get('PortWS'),
                'ip_mask': S12_header.get('ipMask'),
                'ip_gtw': S12_header.get('ipGtw'),
                'dhcp': self.get_boolean(S12_header, 'ipDhcp'),
                'slave1': S12_header.get('Slave1'),
                'slave2': S12_header.get('Slave2'),
                'slave3': S12_header.get('Slave3'),
                'local_ip_address': S12_header.get('ipLoc'),
                'local_ip_mask': S12_header.get('ipMaskLoc'),
                'plc_mac': S12_header.get('Macplc'),
                'serial_port_speed': S12_header.get('Pse'),
                'priority': self.get_boolean(S12_header, 'Priority'),
                'stg_ws_ip_address': S12_header.get('IPstg'),
                'stg_ws_password': S12_header.get('stgPwd'),
                'ntp_ip_address': S12_header.get('IPNTP'),
                'rpt_ftp_ip_address': rpt_ftp_ip_address,
                'rpt_ftp_user': S12_header.get('FTPUserReport'),
                'rpt_ftp_password': S12_header.get('FTPPwdReport'),
                'fwdcup_ftp_ip_address': S12_header.get('IPftpDCUpg'),
                'fwdcup_ftp_user': S12_header.get('UserftpDCUpg'),
                'fwdcup_ftp_password': S12_header.get('PwdftpDCUpg'),
                'fwmtup_ftp_ip_address': S12_header.get('IPftpMeterUpg'),
                'fwmtup_ftp_user': S12_header.get('UserftpMeterUpg'),
                'fwmtup_ftp_password': S12_header.get('UserftpMeterUpg'),
                'retries': int(S12_header.get('RetryFtp')),
                'time_btw_retries': int(S12_header.get('TimeBetwFtp')),
                'cycle_ftp_ip_address': S12_header.get('IPftpCycles'),
                'cycle_ftp_user': S12_header.get('UserftpCycles'),
                'cycle_ftp_password': S12_header.get('PwdftpCycles'),
                'cycle_ftp_dir': S12_header.get('DestDirCycles'),
                'sync_meter': self.get_boolean(S12_header, 'SyncMeter'),
                'fwmtup_timeout': int(S12_header.get(fw_up_to_field) or 0),
                'max_time_deviation': int(S12_header.get('TimeDevOver')),
                'min_time_deviation': int(S12_header.get('TimeDev')),
                'reset_msg': self.get_boolean(S12_header, 'ResetMsg'),
                'rpt_meter_limit': int(S12_header.get('NumMeters')),
                'rpt_time_limit': int(S12_header.get('TimeSendReq')),
                'disconn_time': int(S12_header.get('TimeDisconMeter')),
                'disconn_retries': int(S12_header.get('RetryDisconMeter')),
                'disconn_retry_interval': int(S12_header.get('TimeRetryInterval')),
                'meter_reg_data': S12_header.get('MeterRegData'),
                'report_format': S12_header.get('ReportFormat'),
                's26_content': S12_header.get('S26Content'),
                'values_check_delay': int(S12_header.get('ValuesCheckDelay')),
                'max_order_outdate': int(S12_header.get('MaxOrderOutdate') or 0),
                'restart_delay': int(S12_header.get('TimeDelayRestart') or 0),
                'ntp_max_deviation': (isinstance(S12_header.get('NTPMaxDeviation'), int)
                                      and int(S12_header.get('NTPMaxDeviation')) or 0),
                'session_timeout': (isinstance(S12_header.get('AccInacTimeout'), int)
                                      and int(S12_header.get('AccInacTimeout')) or 0),
                'max_sessions':  (isinstance(S12_header.get('AccSimulMax'), int)
                                      and int(S12_header.get('AccSimulMax')) or 0),
                }
            if not hasattr(S12_header, 'TP'):
                vals['tasks'] = []
                ret_values.append(vals)
                continue
            tasks = []
            for task in S12_header.TP:
                task_values = {
                    'name': task.get('TpTar'),
                    'priority': int(task.get('TpPrio')),
                    'date_from': self.get_timestamp(task, 'TpHi'),
                    'periodicity': task.get('TpPer'),
                    'complete': self.get_boolean(task, 'TpCompl'),
                    'meters': task.get('TpMet'),
                    }
                task_data_values = []
                if getattr(task, 'TpPro', None) is not None:
                    for task_data in task.TpPro:
                        task_data_value = {
                            'request': task_data.get('TpReq'),
                            'stg_send': self.get_boolean(task_data, 'TpSend'),
                            'store': self.get_boolean(task_data, 'TpStore'),
                            'attributes': task_data.get('TpAttr'),
                            }
                        task_data_values.append(task_data_value)
                task_values['task_data'] = task_data_values
                tasks.append(task_values)
            vals['tasks'] = tasks
            ret_values.append(vals)
        return ret_values

    def get_S09(self, type='S09'):
        '''get function for S09 (meter events)'''

        meter_name = self.meter.name
        ret_values = []
        for value in getattr(self.meter.meter, type):
            timestamp = self.get_timestamp(value, 'Fh')
            values = {'name': meter_name,
                      'timestamp': timestamp,
                      'season':value.get('Fh')[-1:],
                      'cnc_name': self.meter.cnc_name,
                      'event_group': int(value.get('Et')),
                      'event_code': int(value.get('C')),
                     }
            data = ''
            d1s = ['D1: {}'.format(d)
                   for d in getattr(value, 'D1', [])]
            d2s = ['D2: {}'.format(d)
                   for d in getattr(value, 'D2', [])]
            data = '\n'.join(d1s + d2s)
            if data:
                values.update({'data': data})
            ret_values.append(values)

        return ret_values

    def get_S13(self):
        '''S13 (spontaneous events) has the same format as S09'''

        return self.get_S09(type='S13')

    def get_S17(self, type='S17'):
        '''get function for S17 (concentrator events)'''

        cnc_name = self.meter.name
        ret_values = []
        for value in getattr(self.meter.concentrator, type):
            timestamp = self.get_timestamp(value, 'Fh')
            values = {'name': cnc_name,
                      'timestamp': timestamp,
                      'season':value.get('Fh')[-1:],
                      'event_group': int(value.get('Et')),
                      'event_code': int(value.get('C')),
                     }
            data = ''
            d1s = ['D1: {}'.format(d)
                   for d in getattr(value, 'D1', [])]
            d2s = ['D2: {}'.format(d)
                   for d in getattr(value, 'D2', [])]
            data = '\n'.join(d1s + d2s)
            if data:
                values.update({'data': data})
            ret_values.append(values)

        return ret_values

    def get_S15(self):
        '''S15 (spontaneous events) has the same format as S17'''

        return self.get_S17(type='S15')
