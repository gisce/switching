#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

def assertXmlEqual(self, got, want):
    from lxml.doctestcompare import LXMLOutputChecker
    from doctest import Example

    checker = LXMLOutputChecker()
    if checker.check_output(want, got, 0):
        return
    message = checker.output_difference(Example("", want), got, 0)
    raise AssertionError(message)

unittest.TestCase.assertXmlEqual = assertXmlEqual
unittest.TestCase.__str__ = unittest.TestCase.id

