#!/usr/bin/env python
# -*- coding: utf-8 -*-

from switching.messages import F1

def from_xml(f_xml, f_xsd):
    f1_xml = F1(f_xml, f_xsd)
    tipus = f1_xml.get_tipus_xml()
    print tipus
    obj = f1_xml.parse_xml()
    print(obj.Facturas.FacturaATR.Potencia.ImporteTotalTerminoPotencia)

if __name__ == '__main__':
    
    f_xsd = open("Facturacion.xsd", "r")
    f_xml = open("F1_03.HIDROELECTRICA_VIRGEN_DE_CHILLA_201004_0631_10005604.xml", "r")
    
    from_xml(f_xml, f_xsd)
