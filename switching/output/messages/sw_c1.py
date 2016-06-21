# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera, IdCliente
from mesures import Aparatos


class DatosSolicitud(XmlModel):
    _sort_order = ('datos', 'linea', 'solicitudadm',
                   'periodicidad_facturacion', 'tipo_cambio',
                   'activacionlectura', 'fechaprevista', 'motivo',
                   'cnae', 'sustituto')
    
    def __init__(self):
        self.datos = XmlField('DatosSolicitud')
        self.linea = XmlField('LineaNegocioElectrica')
        self.solicitudadm = XmlField('SolicitudAdmContractual')
        self.periodicidad_facturacion = XmlField('PeriodicidadFacturacion')
        self.tipo_cambio = XmlField('TipoCambioTitular')
        self.activacionlectura = XmlField('IndActivacionLectura')
        self.fechaprevista = XmlField('FechaPrevistaAccion')
        self.motivo = XmlField('Motivo')
        self.cnae = XmlField('CNAE')
        self.sustituto = XmlField('IndSustitutoMandatario') 
        super(DatosSolicitud, self).__init__('DatosSolicitud', 'datos')


class Direccion(XmlModel):
    _sort_order = ('direccion', 'pais', 'provincia', 'municipio', 'poblacion',
                   'tipovia', 'codpostal', 'calle', 'numfinca', 'dupfinca',
                   'escalera', 'piso', 'puerta', 'tipoaclarador', 'aclarador')

    def __init__(self):
        self.direccion = XmlField('Direccion')
        self.pais = XmlField('Pais')
        self.provincia = XmlField('Provincia')
        self.municipio = XmlField('Municipio')
        self.poblacion = XmlField('Poblacion')
        self.tipovia = XmlField('TipoVia')
        self.codpostal = XmlField('CodPostal')
        self.calle = XmlField('Calle')
        self.numfinca = XmlField('NumeroFinca')
        self.dupfinca = XmlField('DuplicadorFinca')
        self.escalera = XmlField('Escalera')
        self.piso = XmlField('Piso')
        self.puerta = XmlField('Puerta')
        self.tipoaclarador = XmlField('TipoAclaradorFinca')
        self.aclarador = XmlField('AclaradorFinca')
        super(Direccion, self).__init__('Direccion', 'direccion')


class DireccionCorrespondencia(XmlModel):
    _sort_order = ('direccion', 'indicador', 'datos_direccion')

    def __init__(self):
        self.direccion = XmlField('DireccionCorrespondencia')
        self.indicador = XmlField('Indicador')
        self.datos_direccion = Direccion()
        super(DireccionCorrespondencia, self).\
                        __init__('DireccionCorrespondencia', 'direccion')


class IdContrato(XmlModel):
    _sort_order = ('idcontrato', 'codigo')

    def __init__(self):
        self.idcontrato = XmlField('IdContrato')
        self.codigo = XmlField('CodContrato')
        super(IdContrato, self).__init__('IdContrato', 'idcontrato')


class PotenciasContratadas(XmlModel):
    _sort_order = ('potencies', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8',
                   'p9', 'p10')

    def __init__(self):
        self.potencies = XmlField('PotenciasContratadas')
        self.p1 = XmlField('Potencia', attributes={'Periodo': '1'}, rep=lambda x: '%d' % x)
        self.p2 = XmlField('Potencia', attributes={'Periodo': '2'})
        self.p3 = XmlField('Potencia', attributes={'Periodo': '3'})
        self.p4 = XmlField('Potencia', attributes={'Periodo': '4'})
        self.p5 = XmlField('Potencia', attributes={'Periodo': '5'})
        self.p6 = XmlField('Potencia', attributes={'Periodo': '6'})
        self.p7 = XmlField('Potencia', attributes={'Periodo': '7'})
        self.p8 = XmlField('Potencia', attributes={'Periodo': '8'})
        self.p9 = XmlField('Potencia', attributes={'Periodo': '9'})
        self.p10 = XmlField('Potencia', attributes={'Periodo': '10'})
        super(PotenciasContratadas, self).\
                             __init__('PotenciasContratadas', 'potencies')


class CondicionesContractuales(XmlModel):
    _sort_order = ('condicions', 'tarifa', 'periodicidad_facturacion',
                   'tipus_telegestio', 'potencies', 'control_potencia')

    def __init__(self):
        self.condicions = XmlField('CondicionesContractuales')
        self.tarifa = XmlField('TarifaATR')
        self.periodicidad_facturacion = XmlField('PeriodicidadFacturacion')
        self.tipus_telegestio = XmlField('TipodeTelegestion')
        self.potencies = PotenciasContratadas()
        self.control_potencia = XmlField('ModoControlPotencia')
        self.marca_mesura_bt_perdues = XmlField('MarcaMedidaBTConPerdidas')
        self.kvas_trafo = XmlField('KVAsTrafo')
        self.perc_perd_pactades = XmlField('PorcentajePerdidasPactadas')
        super(CondicionesContractuales, self).\
                             __init__('CondicionesContractuales', 'condicions')


class Contacto(XmlModel):
    _sort_order = ('nombre', 'telefon', 'correu')

    def __init__(self):
        self.contacte = XmlField('Contacto')
        self.nombre = Nombre()
        self.telefon = Telefono()
        self.correu = XmlField('CorreoElectronico')
        super(Contacto, self).__init__('Contacto', 'contacte')

    def set_data(self, es_persona_juridica, nom, cognom_1, cognom_2, telefon,
                 prefix, correu=''):
        con_nom = Nombre()

        if es_persona_juridica:
            nom = {
                'razon': nom,
            }
        else:
            nom = {
                'nombrepila': nom,
                'apellido1': cognom_1,
                'apellido2': cognom_2,
            }

        con_nom.feed(nom)

        con_fields = {'nombre': con_nom}
        if telefon:
            con_telefon = Telefono()
            telf_fields = {
                'numero': telefon,
                'prefijo': prefix or '34',
            }
            con_telefon.feed(telf_fields)
            con_fields.update({'telefon': con_telefon})

        if correu:
            con_fields.update({'correu': correu})

        self.feed(con_fields)


class Contrato(XmlModel):
    _sort_order = ('contrato', 'idcontrato', 'fechafin', 'duracion',
                   'tipo_autoconsumo', 'tipo', 'condiciones', 'consumoanual',
                   'contacto', 'direccion', 'tipoactivacion',
                   'fechaactivacion',)

    def __init__(self, tag_tipo='TipoContratoATR'):
        self.contrato = XmlField('Contrato')
        self.idcontrato = IdContrato()
        self.duracion = XmlField('Duracion')
        self.tipo_autoconsumo = XmlField('TipoAutoconsumo')
        self.fechafin = XmlField('FechaFinalizacion')
        self.tipo = XmlField(tag_tipo)
        self.direccion = DireccionCorrespondencia()
        self.consumoanual = XmlField('ConsumoAnualEstimado')
        self.tipoactivacion = XmlField('TipoActivacionPrevista')
        self.fechaactivacion = XmlField('FechaActivacionPrevista')
        self.condiciones = CondicionesContractuales()
        self.contacto = Contacto()
        super(Contrato, self).__init__('Contrato', 'contrato')


class Nombre(XmlModel):
    _sort_order = ('nombre', 'nombrepila', 'apellido1','apellido2', 'razon')

    def __init__(self):
        self.nombre = XmlField('Nombre')
        self.nombrepila = XmlField('NombreDePila')
        self.apellido1 = XmlField('PrimerApellido')
        self.apellido2 = XmlField('SegundoApellido')
        self.razon = XmlField('RazonSocial')
        super(Nombre, self).__init__('Nombre', 'nombre')


class Telefono(XmlModel):
    _sort_order = ('telefono', 'prefijo', 'numero')
        
    def __init__(self, tagname=None):
        if not tagname:
            tagname = 'Telefono'
        self.telefono = XmlField(tagname)
        self.prefijo = XmlField('PrefijoPais')
        self.numero = XmlField('Numero')
        super(Telefono, self).__init__(tagname, 'telefono')


class Cliente(XmlModel):
    _sort_order = ('cliente', 'idcliente', 'nombre', 'titular_pagador',
                   'fax', 'telefono', 'correu', 'indicador', 'direccion', )

    def __init__(self, tagname=None):
        if not tagname:
            tagname = 'Cliente'
        self.cliente = XmlField(tagname)
        self.idcliente = IdCliente()
        self.nombre = Nombre()
        self.fax = Telefono()
        self.telefono = Telefono()
        self.correu = XmlField('CorreoElectronico')
        self.indicador = XmlField('IndicadorTipoDireccion')
        self.direccion = Direccion()
        self.titular_pagador = XmlField('TitularContratoVsTitularPago')
        super(Cliente, self).__init__(tagname, 'cliente')


class CambiodeComercializadoraSinCambios(XmlModel):
    _sort_order = ('cambio', 'solicitud', 'contrato', 'cliente', 'aparato', 
                   'comentario', 'registro')

    def __init__(self):
        self.cambio = XmlField('CambiodeComercializadoraSinCambios')
        self.solicitud = DatosSolicitud()
        self.contrato = Contrato()
        self.cliente = Cliente()
        self.aparato = XmlField('ModelosAparato')
        self.comentario = XmlField('Comentarios')
        self.registro = XmlField('RegistrosDocumento')
        super(CambiodeComercializadoraSinCambios, self).\
                    __init__('CambiodeComercializadoraSinCambios', 'cambio', 
                             drop_empty=False)


class MensajeCambiodeComercializadoraSinCambios(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'cambio')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeCambiodeComercializadoraSinCambios', 
                          attributes={
                              'xmlns': 'http://localhost/elegibilidad'
                           })
        self.cabecera = Cabecera()
        self.cambio = CambiodeComercializadoraSinCambios()
        super(MensajeCambiodeComercializadoraSinCambios, self).\
               __init__('MensajeCambiodeComercializadoraSinCambios', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class DatosAceptacion(XmlModel):
    _sort_order = ('datos', 'fecha', 'potencia', 'actuacion', 'ultlect')
    
    def __init__(self):
        self.datos = XmlField('DatosAceptacion')
        self.fecha = XmlField('FechaAceptacion')
        self.potencia = XmlField('PotenciaActual', rep=lambda x: '%d' % x)
        self.actuacion = XmlField('ActuacionCampo')
        self.ultlect = XmlField('FechaUltimaLectura')
        super(DatosAceptacion, self).__init__('DatosAceptacion', 'datos')


class AceptacionCambiodeComercializadoraSinCambios(XmlModel):
    _sort_order = ('acceptacio', 'dades', 'contracte')

    def __init__(self):
        self.acceptacio = \
                       XmlField('AceptacionCambiodeComercializadoraSinCambios')
        self.dades = DatosAceptacion()
        self.contracte = Contrato()
        super(AceptacionCambiodeComercializadoraSinCambios, self).\
         __init__('AceptacionCambiodeComercializadoraSinCambios', 'acceptacio')


class MensajeAceptacionCambiodeComercializadoraSinCambios(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'acceptacio')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeAceptacionCambiodeComercializadoraSinCambios',
                         attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.acceptacio = AceptacionCambiodeComercializadoraSinCambios() 
        super(MensajeAceptacionCambiodeComercializadoraSinCambios, self).\
                __init__('MensajeAceptacionCambiodeComercializadoraSinCambios',
                         'missatge')
        
    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class Rechazo(XmlModel):
    _sort_order = ('rechazo', 'secuencial', 'motiu', 'text', 'data', 'hora',
                   'idcontracte')
    
    def __init__(self, tagname=None):
        if not tagname:
            tagname = 'Rechazo'
        self.rechazo = XmlField(tagname)
        self.secuencial = XmlField('Secuencial')
        self.motiu = XmlField('CodigoMotivo', rep=lambda x: x.rjust(2, '0'))
        self.text = XmlField('Texto')
        self.data = XmlField('Fecha')    
        self.hora = XmlField('Hora')
        self.idcontracte = IdContrato()
        super(Rechazo, self).__init__(tagname, 'rechazo')

 
class RechazoATRDistribuidoras(XmlModel):
    _sort_order = ('rechazoatr', 'rebuig')

    def __init__(self):
        self.rechazoatr = XmlField('RechazoATRDistribuidoras')
        self.rebuig = []
        super(RechazoATRDistribuidoras, self).\
                __init__('RechazoATRDistribuidoras', 'rechazoatr')


class MensajeRechazoATRDistribuidoras(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'rebuig')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeRechazoATRDistribuidoras',
                     attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.rebuig = RechazoATRDistribuidoras()
        super(MensajeRechazoATRDistribuidoras, self).\
                     __init__('MensajeRechazoATRDistribuidoras', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class DatosActivacion(XmlModel):
    _sort_order = ('dades', 'data', 'hora', 'tipo')
    
    def __init__(self, tagname='DatosActivacion'):
        self.dades = XmlField(tagname)
        self.data = XmlField('Fecha')
        self.hora = XmlField('Hora')
        self.tipo = XmlField('TipoActivacion')
        super(DatosActivacion, self).__init__(tagname, 'dades')


class PuntoDeMedida(XmlModel):
    _sort_order = ('punt_mesura', 'CodPM', 'TipoMovimiento', 'CUPS', 'TipoPM',
                   'ModoLectura', 'EstadoPM', 'Funcion', 'direccio', 'tensio',
                   'FechaVigor', 'FechaAlta', 'aparatos')
    
    def __init__(self):
        self.punt_mesura = XmlField('PuntoDeMedida')
        self.CodPM = XmlField('CodPM')
        self.TipoMovimiento = XmlField('TipoMovimiento')
        self.CUPS = XmlField('CUPS')
        self.TipoPM = XmlField('TipoPM')
        self.ModoLectura = XmlField('ModoLectura')
        self.EstadoPM = XmlField('EstadoPM')
        self.Funcion = XmlField('Funcion')
        self.direccio = XmlField('DireccionPuntoMedida')
        self.tensio = XmlField('TensionPM')
        self.FechaVigor = XmlField('FechaVigor')
        self.FechaAlta = XmlField('FechaAlta')
        self.aparatos = Aparatos()
        super(PuntoDeMedida, self).__init__('PuntoDeMedida', 'punt_mesura')


class PuntosDeMedida(XmlModel):
    _sort_order = ('punts_mesura', 'punt')
    
    def __init__(self):
        self.punts_mesura = XmlField('PuntosDeMedida')
        self.punt = PuntoDeMedida()
        super(PuntosDeMedida, self).__init__('PuntosDeMedida', 'punts_mesura')


class ActivacionCambiodeComercializadoraSinCambios(XmlModel):
    _sort_order = ('activacio', 'dades', 'contracte', 'punts_mesura')
    
    def __init__(self):
        self.activacio = XmlField('ActivacionCambiodeComercializadoraSinCambios')
        self.dades = DatosActivacion()
        self.contracte = Contrato()
        self.punts_mesura = PuntosDeMedida()
        super(ActivacionCambiodeComercializadoraSinCambios, self).\
                __init__('ActivacionCambiodeComercializadoraSinCambios', 'activacio')


class MensajeActivacionCambiodeComercializadoraSinCambios(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'activacio')

    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeActivacionCambiodeComercializadoraSinCambios',
                     attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.activacio = ActivacionCambiodeComercializadoraSinCambios()
        super(MensajeActivacionCambiodeComercializadoraSinCambios, self).\
                     __init__('MensajeActivacionCambiodeComercializadoraSinCambios', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class DatosNotificacion(XmlModel):
    _sort_order = ('dades_notificacio', 'data')
    
    def __init__(self):
        self.dades_notificacio = XmlField('DatosNotificacion')
        self.data = XmlField('FechaActivacion')
        super(DatosNotificacion, self).__init__('DatosNotificacion', 'dades_notificacio')


class NotificacionComercializadoraSaliente(XmlModel):        
    _sort_order = ('notificacio', 'dades', 'contracte', 'punts_mesura')

    def __init__(self):
        self.notificacio = XmlField('NotificacionComercializadoraSaliente')
        self.dades = DatosNotificacion()
        self.contracte = Contrato()
        self.punts_mesura = PuntosDeMedida()
        super(NotificacionComercializadoraSaliente, self).\
                __init__('NotificacionComercializadoraSaliente', 'notificacio')


class MensajeNotificacionComercializadoraSaliente(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'notificacio')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeNotificacionComercializadoraSaliente',
                         attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.notificacio = NotificacionComercializadoraSaliente()
        super(MensajeNotificacionComercializadoraSaliente, self).\
                     __init__('MensajeNotificacionComercializadoraSaliente', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
        

class AnulacionSolicitud(XmlModel):
    _sort_order = ('anulacion', 'datos', 'cliente', 'idcontrato')

    def __init__(self):
        self.anulacion = XmlField('AnulacionSolicitud')
        self.datos = DatosSolicitud()
        self.cliente = Cliente()
        self.idcontrato = IdContrato()
        super(AnulacionSolicitud, self).__init__('AnulacionSolicitud', 'anulacion')


class MensajeAnulacionSolicitud(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'anulacion')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeAnulacionSolicitud', attributes={
                          'xmlns': 'http://localhost/elegibilidad'})
        self.cabecera = Cabecera()
        self.anulacion = AnulacionSolicitud()
        super(MensajeAnulacionSolicitud, self).__init__('MensajeAnulacionSolicitud',
                                                 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class AceptacionAnulacion(XmlModel):
    _sort_order = ('aceptacion', 'datos', 'contrato')

    def __init__(self):
        self.aceptacion = XmlField('AceptacionAnulacion')
        self.datos = DatosAceptacion()
        self.contrato = Contrato()
        super(AceptacionAnulacion, self).__init__('AceptacionAnulacion', 'aceptacion')


class MensajeAceptacionAnulacion(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'aceptacion')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeAceptacionAnulacion', attributes={
                          'xmlns': 'http://localhost/elegibilidad'})
        self.cabecera = Cabecera()
        self.aceptacion = AceptacionAnulacion()
        super(MensajeAceptacionAnulacion, self).__init__('MensajeAceptacionAnulacion',
                                                 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class RechazoAnulacion(XmlModel):
    _sort_order = ('rechazo', 'rebuig')

    def __init__(self):
        self.rechazo = XmlField('RechazoAnulacion')
        self.rebuig = Rechazo('RechazoAnulacion')
        super(RechazoAnulacion, self).__init__('RechazoAnulacion', 'rechazo')


class RechazoDeAnulacion(XmlModel):
    _sort_order = ('rechazo', 'rebuig')

    def __init__(self):
        self.rechazoanu = XmlField('RechazoDeAnulacion')
        self.rebuig = []
        super(RechazoDeAnulacion, self).__init__('RechazoDeAnulacion',
                                                 'rechazoanu')


class MensajeRechazoAnulacion(XmlModel):
    _sort_order = ('mensaje', 'capcalera', 'rebuig')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeRechazoAnulacion', attributes={
                          'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.rebuig = RechazoDeAnulacion()
        super(MensajeRechazoAnulacion,
              self).__init__('MensajeRechazoAnulacion',
                             'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
    
    
