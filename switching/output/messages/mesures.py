# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
import re

from libcomxml.core import XmlModel, XmlField

class LecturaDesde(XmlModel):
    _sort_order = ('desde', 'fechahora', 'procedencia', 'lectura')

    def __init__(self):
        self.desde = XmlField('LecturaDesde')
        self.fechahora = XmlField('FechaHora', rep=lambda x: '%sT00:00:00' % x)
        self.procedencia = XmlField('Procedencia')
        self.lectura = XmlField('Lectura', rep=lambda x: '%.2f' % x)
        super(LecturaDesde, self).__init__('LecturaDesde', 'desde')


class LecturaHasta(XmlModel):
    _sort_order = ('hasta', 'fechahora', 'procedencia', 'lectura')

    def __init__(self):
        self.hasta = XmlField('LecturaHasta')
        self.fechahora = XmlField('FechaHora', rep=lambda x: '%sT00:00:00' % x)
        self.procedencia = XmlField('Procedencia')
        self.lectura = XmlField('Lectura', rep=lambda x: '%.2f' % x)
        super(LecturaHasta, self).__init__('LecturaHasta', 'hasta')


class Integrador(XmlModel):
    _sort_order = ('integrador', 'magnitud', 'codperiodo', 'multi', 'enteras',
                   'decimales', 'consumo', 'desde', 'hasta')

    def rep_ruedas(self, num):
        return '%d' % num


    def __init__(self):
        self.integrador = XmlField('Integrador')
        self.magnitud = XmlField('Magnitud')
        self.codperiodo = XmlField('CodigoPeriodo')
        self.multi = XmlField('ConstanteMultiplicadora')
        self.enteras = XmlField('NumeroRuedasEnteras', rep=self.rep_ruedas)
        self.decimales = XmlField('NumeroRuedasDecimales', rep=self.rep_ruedas)
        self.consumo = XmlField('ConsumoCalculado', rep=lambda x: '%.2f' % x)
        self.desde = LecturaDesde()
        self.hasta = LecturaHasta()
        super(Integrador, self).__init__('Integrador', 'integrador')


class NoICP(XmlModel):

    _sort_order = ('noicp', 'periode_fabricacio', 'num_serie',
                   'funcio', 'num_integradors', 'constant_energia',
                   'constant_max', 'enters', 'decimals')

    def __init__(self):
        self.noicp = XmlField('DatosAparatoNoICP')
        self.periode_fabricacio = XmlField('PeriodoFabricacion')
        self.num_serie = XmlField('NumeroSerie')
        self.funcio = XmlField('FuncionAparato')
        self.num_integradors = XmlField('NumIntegradores')
        self.constant_energia = XmlField('ConstanteEnergia', rep=lambda x: '%.3f' % x)
        self.constant_max = XmlField('ConstanteMaximetro', rep=lambda x: '%.3f' % x)
        self.enters = XmlField('RuedasEnteras', rep=lambda x: '%i' % x)
        self.decimals = XmlField('RuedasDecimales', rep=lambda x: '%i' % x)
        super(NoICP, self).__init__('DatosAparatoNoICP', 'noicp')


class ICP(XmlModel):

    _sort_order = ('icp', 'periode_fabricacio', 'num_serie',
                   'funcio', 'num_integradors', 'constant_energia',
                   'constant_max', 'enters', 'decimals')

    def __init__(self):
        self.icp = XmlField('DatosAparatoICP')
        self.periode_fabricacio = XmlField('PeriodoFabricacion')
        self.num_serie = XmlField('NumeroSerie',
                                  rep=lambda x: x[:10])
        self.funcio = XmlField('FuncionAparato')
        self.num_integradors = XmlField('NumIntegradores')
        self.constant_energia = XmlField('ConstanteEnergia', rep=lambda x: '%.3f' % x)
        self.constant_max = XmlField('ConstanteMaximetro', rep=lambda x: '%.3f' % x)
        self.enters = XmlField('RuedasEnteras')
        self.decimals = XmlField('RuedasDecimales')
        super(ICP, self).__init__('DatosAparatoICP', 'icp')


class Modelo(XmlModel):

    _sort_order = ('tipus', 'marca', 'model')

    def __init__(self):
        self.modelo = XmlField('Modelo')
        self.tipus = XmlField('Tipo')
        self.marca = XmlField('Marca')
        self.model = XmlField('ModeloMarca')
        super(Modelo, self).__init__('Modelo', 'modelo')

class Modelos(XmlModel):

    _sort_order = ('modelos', 'modelo')

    def __init__(self):
        self.modelos = XmlField('ModelosAparato')
        self.modelo = []
        super(Modelos, self).__init__('ModelosAparato', 'modelos')

class Aparato(XmlModel):
    _sort_order = ('aparato', 'tipo', 'marca', 'numserie',
                   'codigodh', 'integradores',
                   'model', 'tipus_moviment',
                   'tipus_em', 'propietat', 'precinte',
                   'datosnoicp', 'datosicp', 'medidas')
    
    def __init__(self):
        self.aparato = XmlField('Aparato')
        self.tipo = XmlField('Tipo')
        self.marca = XmlField('Marca')
        self.numserie = XmlField('NumeroSerie',
                            rep=lambda x: re.sub('[^0-9]', '', x)[:10])
        self.codigodh = XmlField('CodigoDH')
        self.integradores = []
        self.model = Modelo()
        self.tipus_moviment = XmlField('TipoMovimiento')  
        self.tipus_em = XmlField('TipoEquipoMedida') 
        self.propietat = XmlField('TipoPropiedadAparato') 
        self.precinte = XmlField('CodPrecinto')
        self.datosnoicp = NoICP()
        self.datosicp = ICP()
        self.medidas = Medidas()
        super(Aparato, self).__init__('Aparato', 'aparato')


class Aparatos(XmlModel):
    _sort_order = ('aparatos', 'aparato')

    def __init__(self):
        self.aparatos = XmlField('Aparatos')
        self.aparato = []
        super(Aparatos, self).__init__('Aparatos', 'aparatos')


class Medida(XmlModel):
    _sort_order = ('medida', 'tipus_dh', 'periode', 'magnitud',
                   'origen', 'lectura', 'anomalia', 'text_anomalia')

    def __init__(self):
        self.medida = XmlField('Medida')
        self.tipus_dh = XmlField('TipoDH')
        self.periode = XmlField('Periodo')
        self.magnitud = XmlField('MagnitudMedida')
        self.origen = XmlField('Procedencia')
        self.lectura = XmlField('LecturaAnterior', rep=lambda x: '%.2f' % x)
        self.anomalia = XmlField('Anomalia')
        self.text_anomalia = XmlField('TextoAnomalia')
        super(Medida, self).__init__('Medida', 'medida')


class Medidas(XmlModel):
    _sort_order = ('medidas', 'cups', 'aparatos', 'lista_medidas')

    def __init__(self):
        self.medidas = XmlField('Medidas')
        self.cups = XmlField('CodUnificadoPuntoSuministro',
                             rep=lambda x: x.ljust(22, ' '))
        self.aparatos = []
        self.lista_medidas = []
        super(Medidas, self).__init__('Medidas', 'medidas')
