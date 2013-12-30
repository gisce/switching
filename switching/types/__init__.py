# -*- coding: utf-8 -*- 

import decimal
from lxml import objectify 


class DecimalElement(objectify.ObjectifiedDataElement):
    @property
    def pyval(self):
        return decimal.Decimal(self.text)


def check_decimal_element(decimal_string):
    """Catch decimal's exception and raise the one objectify expects"""
    try:
        decimal.Decimal(decimal_string)
    except decimal.InvalidOperation:
        raise ValueError
