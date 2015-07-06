# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111
import re

from libcomxml.core import XmlModel, XmlField
import switching.output.messages.mesures as m
from switching.output.messages.base import Cabecera, Cliente


class DatosGeneralesFactura(XmlModel):
    _sort_order = ('datos', 'numero', 'tipo', 'rectificadora', 'ref', 'fecha',
                   'cif', 'codigo', 'obs', 'importe', 'saldo', 'saldocobro',
                   'moneda')

    def __init__(self):
        self.datos = XmlField('DatosGeneralesFactura')
        self.numero = XmlField('NumeroFactura', rep=lambda x: x[:26])
        self.tipo = XmlField('TipoFactura')
        self.rectificadora = XmlField('IndicativoFacturaRectificadora')
        self.ref = XmlField('NumeroFacturaRectificada')
        self.fecha = XmlField('FechaFactura')
        self.cif = XmlField('CIFEmisora')
        self.codigo = XmlField('CodigoFiscalFactura', rep=lambda x: x[:17])
        self.obs = XmlField('Observaciones')
        self.importe = XmlField('ImporteTotalFactura', rep=lambda x: '%.2f' % x)
        self.saldo = XmlField('SaldoFactura', rep=lambda x: '%.2f' % x)
        self.saldocobro = XmlField('SaldoCobro', rep=lambda x: '%.2f' % x)
        self.moneda = XmlField('TipoMoneda', value='02')
        super(DatosGeneralesFactura, self).__init__('DatosGeneralesFactura',
                                                    'datos')


class PeriodoCCH(XmlModel):
    _sort_order = ('periodocch', 'fecha_desde', 'fecha_hasta')

    def __init__(self):
        self.periodocch = XmlField('PeriodoCCH')
        self.fecha_desde = XmlField('FechaDesdeCCH')
        self.fecha_hasta = XmlField('FechaHastaCCH')
        super(PeriodoCCH, self).__init__('PeriodoCCH', 'periodocch')


class Periodo(XmlModel):
    _sort_order = ('periodo', 'fecha_desde', 'fecha_hasta', 'meses')

    def __init__(self):
        self.periodo = XmlField('Periodo')
        self.fecha_desde = XmlField('FechaDesdeFactura')
        self.fecha_hasta = XmlField('FechaHastaFactura')
        self.meses = XmlField('NumeroMeses')
        super(Periodo, self).__init__('Periodo', 'periodo')


class DatosFacturaATR(XmlModel):
    _sort_order = ('datos', 'tipo', 'boe', 'tarifa', 'mcp', 'imab',
                   'indicativo_curva_carga', 'periodocch', 'periodo')

    def __init__(self):
        self.datos = XmlField('DatosFacturaATR')
        self.tipo = XmlField('TipoFacturacion')
        self.boe = XmlField('FechaBOE')
        self.tarifa = XmlField('CodigoTarifa')
        self.mcp = XmlField('ModoControlPotencia')
        self.imab = XmlField('IndAltamedidoenBaja')
        self.indicativo_curva_carga = XmlField('IndicativoCurvaCarga')
        self.periodocch = PeriodoCCH()
        self.periodo = Periodo()
        super(DatosFacturaATR, self).__init__('DatosFacturaATR', 'datos')


class DireccionSuministro(XmlModel):
    _sort_order = ('direccion', 'cups', 'municipio', 'dirsuministro')

    def __init__(self):
        self.direccion = XmlField('DireccionSuministro')
        self.cups = XmlField('CUPS', rep=lambda x: x.ljust(22, ' '))
        self.municipio = XmlField('Municipio')
        self.dirsuministro = XmlField('DirSuministro', rep=lambda x: x[:60])
        super(DireccionSuministro, self).__init__('DireccionSuministro',
                                                  'direccion')


class DatosGeneralesFacturaATR(XmlModel):
    _sort_order = ('datos', 'direccion', 'cliente', 'contrato', 'datosgrles',
                   'datosatr')

    def __init__(self):
        self.datos = XmlField('DatosGeneralesFacturaATR')
        self.direccion = DireccionSuministro()
        self.cliente = Cliente()
        self.contrato = XmlField('Contrato',
                                         rep=lambda x: re.sub('[^0-9]', '', x))
        self.datosgrles = DatosGeneralesFactura()
        self.datosatr = DatosFacturaATR()
        super(DatosGeneralesFacturaATR,
              self).__init__('DatosGeneralesFacturaATR', 'datos')


class DatosGeneralesOtrasFacturas(XmlModel):
    _sort_order = ('datosotras', 'direccion', 'cliente', 'contrato',
                   'datosgrles', 'linea')

    def __init__(self):
        self.datosotras = XmlField('DatosGeneralesOtrasFacturas')
        self.direccion = DireccionSuministro()
        self.cliente = Cliente()
        self.contrato = XmlField('Contrato',
                                 rep=lambda x: re.sub('[^0-9]', '', x))
        self.datosgrles = DatosGeneralesFactura()
        self.linea = XmlField('LineaNegocio')
        super(DatosGeneralesOtrasFacturas,
              self).__init__('DatosGeneralesOtrasFacturas', 'datosotras')


class TerminoPotencia(XmlModel):
    _sort_order = ('termino', 'fecha_desde', 'fecha_hasta', 'periodos')

    def __init__(self):
        self.termino = XmlField('TerminoPotencia')
        self.fecha_desde = XmlField('FechaDesde')
        self.fecha_hasta = XmlField('FechaHasta')
        self.periodos = []
        super(TerminoPotencia, self).__init__('TerminoPotencia', 'termino')


class Potencia(XmlModel):
    _sort_order = ('potencia', 'termino', 'icp', 'importe')

    def __init__(self):
        self.potencia = XmlField('Potencia')
        self.termino = []
        self.icp = XmlField('PenalizacionNoICP')
        self.importe = XmlField('ImporteTotalTerminoPotencia',
                                rep=lambda x: '%.2f' % x)
        super(Potencia, self).__init__('Potencia', 'potencia')


class PeriodoExcesoPotencia(XmlModel):
    _sort_order = ('periodo', 'valor')

    def __init__(self):
        self.periodo = XmlField('Periodo')
        self.valor = XmlField('ValorExcesoPotencia', rep=lambda x: '%i' % x)
        super(PeriodoExcesoPotencia, self).__init__('PeriodoExcesoPotencia', 'periodo')


class ExcesoPotencia(XmlModel):
    _sort_order = ('exceso', 'periodos', 'importe')

    def __init__(self):
        self.exceso = XmlField('ExcesoPotencia')
        self.periodos = []
        self.importe = XmlField('ImporteTotalExcesos',
                                        rep=lambda x: '%.4f' % x)
        super(ExcesoPotencia, self).__init__('ExcesoPotencia', 'exceso')


class TerminoEnergiaActiva(XmlModel):
    _sort_order = ('termino', 'fecha_desde', 'fecha_hasta', 'periodos')

    def __init__(self):
        self.termino = XmlField('TerminoEnergiaActiva')
        self.fecha_desde = XmlField('FechaDesde')
        self.fecha_hasta = XmlField('FechaHasta')
        self.periodos = []
        super(TerminoEnergiaActiva, self).__init__(
            'TerminoEnergiaActiva', 'termino')


class EnergiaActiva(XmlModel):
    _sort_order = ('activa', 'termino', 'importe')

    def __init__(self):
        self.activa = XmlField('EnergiaActiva')
        self.termino = []
        self.importe = XmlField('ImporteTotalEnergiaActiva',
                                rep=lambda x: '%.2f' % x)
        super(EnergiaActiva, self).__init__('EnergiaActiva', 'activa')


class TerminoEnergiaReactiva(XmlModel):
    _sort_order = ('termino', 'fecha_desde', 'fecha_hasta', 'periodos')

    def __init__(self):
        self.termino = XmlField('TerminoEnergiaReactiva')
        self.fecha_desde = XmlField('FechaDesde')
        self.fecha_hasta = XmlField('FechaHasta')
        self.periodos = []
        super(TerminoEnergiaReactiva, self).__init__(
            'TerminoEnergiaReactiva', 'termino')


class EnergiaReactiva(XmlModel):
    _sort_order = ('reactiva', 'termino', 'importe')

    def __init__(self):
        self.reactiva = XmlField('EnergiaReactiva')
        self.termino = []
        self.importe = XmlField('ImporteTotalEnergiaReactiva',
                                rep=lambda x: '%.2f' % (x or bool(x)))
        super(EnergiaReactiva, self).__init__('EnergiaRectiva', 'reactiva')


class PeriodoPotencia(XmlModel):
    _sort_order = ('periodo', 'contratada', 'maxdemandada', 'afacturar',
                   'precio')

    def _pot_rep(self, val):
        return ('%.0f' % val)[:11]

    def __init__(self):
        self.periodo = XmlField('Periodo')
        self.contratada = XmlField('PotenciaContratada', rep=self._pot_rep)
        self.maxdemandada = XmlField('PotenciaMaxDemandada', rep=self._pot_rep)
        self.afacturar = XmlField('PotenciaAFacturar', rep=self._pot_rep)
        self.precio = XmlField('PrecioPotencia', rep=lambda x: '%.8f' % x)
        super(PeriodoPotencia, self).__init__('PeriodoPotencia', 'periodo')


class PeriodoEnergiaActiva(XmlModel):
    _sort_order = ('periodo', 'valor', 'precio')

    def __init__(self):
        self.periodo = XmlField('Periodo')
        self.valor = XmlField('ValorEnergiaActiva', rep=lambda x: '%.2f' % x)
        self.precio = XmlField('PrecioEnergia', rep=lambda x: '%.8f' % x)
        super(PeriodoEnergiaActiva, self).__init__('PeriodoEnergiaActiva',
                                                   'periodo')


class PeriodoEnergiaReactiva(XmlModel):
    _sort_order = ('periodo', 'valor', 'precio')

    def __init__(self):
        self.periodo = XmlField('Periodo')
        self.valor = XmlField('ValorEnergiaReactiva', rep=lambda x: '%.2f' % x)
        self.precio = XmlField('PrecioEnergiaReactiva',
                               rep=lambda x: '%.8f' % x)
        super(PeriodoEnergiaReactiva, self).__init__('PeriodoEnergiaReactiva',
                                                     'periodo')


class ImpuestoElectrico(XmlModel):
    _sort_order = ('iese', 'base', 'coef', 'percent', 'importe')

    def __init__(self):
        self.iese = XmlField('ImpuestoElectrico')
        self.base = XmlField('BaseImponible', rep=lambda x: '%.4f' % x)
        self.coef = XmlField('Coeficiente', rep=lambda x: '%.6f' % x)
        self.percent = XmlField('Porcentaje', rep=lambda x: '%.8f' % x)
        self.importe = XmlField('Importe', rep=lambda x: '%.4f' % x)
        super(ImpuestoElectrico, self).__init__('ImpuestoElectrico', 'iese')


class Alquileres(XmlModel):
    _sort_order = ('alquileres', 'importe')

    def __init__(self):
        self.alquileres = XmlField('Alquileres')
        self.importe = XmlField('ImporteFacturacionAlquileres',
                                rep=lambda x: '%.2f' % x)
        super(Alquileres, self).__init__('Alquileres', 'alquileres')


class IVA(XmlModel):
    _sort_order = ('iva', 'base', 'porcentaje', 'importe')

    def __init__(self):
        self.iva = XmlField('IVA')
        self.base = XmlField('BaseImponible', rep=lambda x: '%.4f' % x)
        self.porcentaje = XmlField('Porcentaje', rep=lambda x: '%.2f' % x)
        self.importe = XmlField('Importe', rep=lambda x: '%.4f' % x)
        super(IVA, self).__init__('IVA', 'iva')


class IVAIGICReducido(XmlModel):
    _sort_order = ('ivaigic', 'base', 'porcentaje', 'importe')

    def __init__(self):
        self.ivaigic = XmlField('IVAIGICReducido')
        self.base = XmlField('BaseImponible', rep=lambda x: '%.4f' % x)
        self.porcentaje = XmlField('Porcentaje', rep=lambda x: '%.2f' % x)
        self.importe = XmlField('Importe', rep=lambda x: '%.4f' % x)
        super(IVAIGICReducido, self).__init__('IVAIGICReducido', 'ivaigic')


class ConceptoIEIVA(XmlModel):
    _sort_order = ('conceptoieiva', 'concepto', 'importe')

    def __init__(self):
        self.conceptoieiva = XmlField('ConceptoIEIVA')
        self.concepto = XmlField('Concepto')
        self.importe = XmlField('ImporteConceptoIEIVA',
                                 rep=lambda x: '%.4f' % x)
        super(ConceptoIEIVA, self).__init__('ConceptoIEIVA', 'conceptoieiva')


class ConceptoIVA(XmlModel):
    _sort_order = ('conceptoiva', 'concepto', 'importe', 'observaciones')

    def __init__(self):
        self.conceptoiva = XmlField('ConceptoIVA')
        self.concepto = XmlField('Concepto')
        self.importe = XmlField('ImporteConceptoIVA',
                                 rep=lambda x: '%.4f' % x)
        self.observaciones = XmlField('Observaciones')
        super(ConceptoIVA, self).__init__('ConceptoIVA', 'conceptoiva')


class Concepto(XmlModel):
    _sort_order = ('tipoconcepto', 'unidadesconcepto', 'importeunidadconcept',
                   'importetotalconcept')

    def __init__(self):
        self.concepto = XmlField('Concepto')
        self.tipoconcepto = XmlField('TipoConcepto')
        self.unidadesconcepto = XmlField('UnidadesConcepto')
        self.importeunidadconcept = XmlField('ImporteUnidadConcepto',
                                             rep=lambda x: '%.4f' % x)
        self.importetotalconcept = XmlField('ImporteTotalConcepto',
                                            rep=lambda x: '%.4f' % x)
        super(Concepto, self).__init__('Concepto', 'concepto')


class Refacturacion(XmlModel):
    _sort_order = ('refacturacion', 'tipo', 'fecha_desde', 'fecha_hasta',
                   'consumo', 'importe_total')
    
    def __init__(self):
        self.refacturacion = XmlField('Refacturacion')
        self.tipo = XmlField('Tipo')
        self.fecha_desde = XmlField('RFechaDesde')
        self.fecha_hasta = XmlField('RFechaHasta')
        self.consumo = XmlField('RConsumo',
                                rep=lambda x: '%.2f' % x)
        self.importe_total = XmlField('ImporteTotal',
                                      rep=lambda x: '%.4f' % x)
        super(Refacturacion, self).__init__('Refacturacion', 'refacturacion')


class FacturaATR(XmlModel):
    _sort_order = ('factura', 'datosatr', 'potencia', 'exceso',
                   'energia', 'reactiva', 'conceptoieiva', 'iese',
                   'alquileres', 'conceptoiva', 'iva',
                   'refacturaciones', 'medidas')

    def __init__(self):
        self.factura = XmlField('FacturaATR')
        self.datosatr = DatosGeneralesFacturaATR()
        self.potencia = Potencia()
        self.exceso = ExcesoPotencia()
        self.energia = EnergiaActiva()
        self.reactiva = EnergiaReactiva()
        self.conceptoieiva = []
        self.iese = ImpuestoElectrico()
        self.alquileres = Alquileres()
        self.conceptoiva = []
        self.iva = []
        self.refacturaciones =  XmlField('Refacturaciones')
        self.medidas = m.Medidas()
        super(FacturaATR, self).__init__('FacturaATR', 'factura')


class FacturaConcepto(XmlModel):
    _sort_order = ('factura', 'datosatr', 'potencia', 'exceso',
                   'energia', 'reactiva', 'conceptoieiva', 'iese',
                   'alquileres', 'conceptoiva', 'iva',
                   'refacturaciones', 'medidas')

    def __init__(self):
        self.facturaconcepto = XmlField('FacturaConcepto')
        self.otrasfacturas = OtrasFacturas()
        self.registro = RegistroFin()
        super(FacturaConcepto, self).__init__('FacturaConcepto', 'factura')


class OtrasFacturas(XmlModel):
    _sort_order = ('otrasfacturas', 'datosotras', 'concepto', 'iva',
                   'ivaigic')

    def __init__(self):
        self.otrasfacturas = XmlField('OtrasFacturas')
        self.datosotras = DatosGeneralesOtrasFacturas()
        self.concepto = Concepto()
        self.iva = IVA()
        self.ivaigic = IVAIGICReducido()
        super(OtrasFacturas, self).__init__('OtrasFacturas', 'otrasfacturas')


class CuentaBancaria(XmlModel):
    _sort_order = ('ccc', 'banco', 'sucursal', 'digcontrol', 'cuenta')

    def __init__(self):
        self.ccc = XmlField('CuentaBancaria')
        self.banco = XmlField('Banco')
        self.sucursal = XmlField('Sucursal')
        self.digcontrol = XmlField('DC')
        self.cuenta = XmlField('Cuenta')
        super(CuentaBancaria, self).__init__('CuentaBancaria', 'ccc')


class RegistroFin(XmlModel):
    _sort_order = ('registro', 'importe', 'sfacturacion', 'scobro', 'totalrec',
                   'tipomoneda', 'fvalor', 'flimite', 'ccc', 'iban',
                   'idremesa')

    def __init__(self):
        self.registro = XmlField('RegistroFin')
        self.importe = XmlField('ImporteTotal', rep=lambda x: '%.2f' % x)
        self.sfacturacion = XmlField('SaldoTotalFacturacion',
                                     rep=lambda x: '%.2f' % x)
        self.scobro = XmlField('SaldoTotalCobro', rep=lambda x: '%.2f' % x)
        self.totalrec = XmlField('TotalRecibos')
        self.tipomoneda = XmlField('TipoMoneda')
        self.fvalor = XmlField('FechaValor')
        self.flimite = XmlField('FechaLimitePago')
        self.ccc = CuentaBancaria()
        self.iban = XmlField('IBAN')
        self.idremesa = XmlField('IdRemesa')
        super(RegistroFin, self).__init__('RegistroFin', 'registro')


class MensajeFacturacion(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'facturas')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeFacturacion', attributes={
                          'xmlns': 'http://localhost/elegibilidad'})
        self.cabecera = Cabecera()
        self.facturas = XmlField('Facturas')
        super(MensajeFacturacion, self).__init__('MensajeFacturacion',
                                                 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()

