# -*- coding: utf-8 -*-
"""
.. module: switching

Aquesta llibreria proveeix de les classes i mètodes necessaris pel switching

"""
import os

__version__ = '2.6.3'

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)
