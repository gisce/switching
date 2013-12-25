# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

class Cabecera(XmlModel):
    _sort_order = ('cabecera', 'ree_emisora', 'ree_destino', 'proceso', 'paso',
                   'solicitud', 'secuencia', 'codigo', 'fecha', 'version')

    def rep_solicitud(self, codsol):
        codsol = ''.join([x for x in codsol if x.isalnum()])
        return codsol.ljust(12, '0')[:12]

    def rep_fecha(self, fecha):
        if len(fecha.strip()) == 10:
            #We do not have time so add it
            fecha += ' 00:00:00'
        return 'T'.join(fecha.split(' '))

    def __init__(self):
        self.cabecera = XmlField('Cabecera')
        self.ree_emisora = XmlField('CodigoREEEmpresaEmisora')
        self.ree_destino = XmlField('CodigoREEEmpresaDestino')
        self.proceso = XmlField('CodigoDelProceso')
        self.paso = XmlField('CodigoDePaso')
        self.solicitud = XmlField('CodigoDeSolicitud', rep=self.rep_solicitud)
        self.secuencia = XmlField('SecuencialDeSolicitud')
        self.codigo = XmlField('Codigo', rep=lambda x: x.ljust(22, '0'))
        self.fecha = XmlField('FechaSolicitud', rep=self.rep_fecha)
        self.version = XmlField('Version', value='02')
        super(Cabecera, self).__init__('Cabecera', 'cabecera')


class Cliente(XmlModel):
    _sort_order = ('cliente', 'cifnif', 'identificador')

    def __init__(self):
        self.cliente = XmlField('Cliente')
        self.cifnif = XmlField('TipoCIFNIF')
        self.identificador = XmlField('Identificador', rep=lambda x: len(x) > 9 and x[2:] or x)
        super(Cliente, self).__init__('Cliente', 'cliente')


class IdCliente(XmlModel):
    _sort_order = ('idcliente', 'cifnif', 'identificador')

    def __init__(self):
        self.idcliente = XmlField('IdCliente')
        self.cifnif = XmlField('TipoCIFNIF')
        self.identificador = XmlField('Identificador', rep=lambda x: len(x) > 9 and x[2:] or x)
        super(IdCliente, self).__init__('IdCliente', 'idcliente')


