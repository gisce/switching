from collections import namedtuple
from datetime import datetime, timedelta
from workdays import workday


class DeadLine(namedtuple('Deadline', "step, days, next_step")):
    def limit(self, date=datetime.today()):
        if isinstance(self.days, Naturaldays):
            return date + timedelta(self.days)
        else:
            return workday(date, self.days)


class Workdays(int):
    def __new__(cls, *args, **kwargs):
        return super(Workdays, cls).__new__(cls, *args, **kwargs)


class Naturaldays(int):
    def __new__(cls, *args, **kwargs):
        return super(Naturaldays, cls).__new__(cls, *args, **kwargs)


class ProcessDeadline(object):
    @classmethod
    def get_deadline(cls, step, activation=False):
        if not activation and step == '02':
            step = '{0}_no_activation'.format(step)
        for s in cls.steps:
            if s.step == step:
                return s
