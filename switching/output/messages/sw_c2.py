# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera, IdCliente
from mesures import Aparatos, Modelos
from sw_c1 import DatosSolicitud, Contrato, Cliente, DatosAceptacion
from sw_c1 import DatosActivacion, PuntosDeMedida


class CiePapel(XmlModel):

    _sort_order = ('cie_papel', 'codigo_cie', 'potencia_inst_bt',
                   'fecha_emision', 'fecha_caducidad', 'nif_instalador',
                   'codigo_instalador', 'nombre_instalador',
                   'tension_suministro', 'intensidad_diferencial',
                   'sensibilidad_diferencial', 'seccion_cable',
                   'tipo_suministro',)

    def __init__(self):
        self.cie_papel = XmlField('CIEPapel')
        self.codigo_cie = XmlField('CodigoCie')
        self.potencia_inst_bt = XmlField('PotenciaInstBT')
        self.fecha_emision = XmlField('FechaEmisionCie')
        self.fecha_caducidad = XmlField('FechaCaducidadCie')
        self.nif_instalador = XmlField('NifInstalador')
        self.codigo_instalador = XmlField('CodigoInstalador')
        self.nombre_instalador = XmlField('NombreInstalador')
        self.tension_suministro = XmlField('TensionSuministroCIE')
        self.intensidad_diferencial = XmlField('IntensidadDif')
        self.sensibilidad_diferencial = XmlField('SensibilidadDif')
        self.seccion_cable = XmlField('SeccionCable')
        self.tipo_suministro = XmlField('TipoSuministro')
        super(CiePapel, self).__init__('CIEPapel', 'cie_papel')


class DatosCie(XmlModel):

    _sort_order = ('datos_cie', 'cie_electronico', 'cie_papel', 'validez_cie',
                   'CIE_electronico')

    def __init__(self):
        self.datos_cie = XmlField('DatosCie')
        self.cie_electronico = XmlField('CieElectronico')
        self.cie_papel = CiePapel()

        # Not implemented
        self.validez_cie = XmlField('ValidezCie')
        self.CIE_electronico = XmlField('CIEElectronico')

        super(DatosCie, self).__init__('DatosCie', 'datos_cie')


class DocTecnica(XmlModel):

    _sort_order = ('doctecnica', 'datos_cie', 'datos_apm', )

    def __init__(self):
        self.doctecnica = XmlField('DocTecnica')
        self.datos_cie = DatosCie()

        #Not implemented
        self.datos_apm = XmlField('DatosApm')

        super(DocTecnica, self).__init__('DocTecnica', 'doctecnica')


class Medida(XmlModel):

    _sort_order = ('medida', 'cp_propietat', 'cp_installacio',
                   'equip_aportat_client', 'equip_installat_client',
                   'tipus_equip', 'modelos')

    def __init__(self):
        self.medida = XmlField('Medida')
        self.cp_propietat = XmlField('ControlPotenciaPropiedad')
        self.cp_installacio = XmlField('ControlPotenciaInstalacion')
        self.equip_aportat_client = XmlField('EquipoAportadoCliente')
        self.equip_installat_client = XmlField('EquipoInstaladoCliente')
        self.tipus_equip = XmlField('TipoEquipoMedida')
        self.modelos = Modelos()
        super(Medida, self).__init__('Medida', 'medida',
                                     drop_empty=False)


class RegistroDoc(XmlModel):

    _sort_order = ('registro', 'tipo', 'url')

    def __init__(self):
        self.registro = XmlField('RegistroDoc')
        self.tipo = XmlField('TipoDocAportado')
        self.url = XmlField('DireccionUrl')
        super(RegistroDoc, self).__init__('RegistroDoc',
                                                'registro')

class RegistrosDocumento(XmlModel):

    _sort_order = ('registros', 'registro')

    def __init__(self):
        self.registros = XmlField('RegistrosDocumento')
        self.registro = []
        super(RegistrosDocumento, self).__init__('RegistrosDocumento',
                                                 'registros')

class Comentario(XmlModel):

    _sort_order = ('comentario', 'texto', 'fecha', 'hora')

    def __init__(self):
        self.comentario = XmlField('Comentario')
        self.texto = XmlField('Texto')
        self.fecha = XmlField('Fecha')
        self.hora = XmlField('Hora')
        super(Comentario, self).__init__('Comentario',
                                         'comentario')

class Comentarios(XmlModel):

    _sort_order = ('comentarios', 'comentario')

    def __init__(self):
        self.comentarios = XmlField('Comentarios')
        self.comentario = []
        super(Comentarios, self).__init__('Comentarios',
                                          'comentarios',
                                          drop_empty=False)

class CambiodeComercializadoraConCambios(XmlModel):
    _sort_order = ('cambio', 'solicitud', 'contrato', 'cliente',
                   'medida', 'doctecnica', 'comentario', 'registro',
                   'cnae', 'vivenda', 'tipuscanvititular')

    def __init__(self):
        self.cambio = XmlField('CambiodeComercializadoraConCambios')
        self.solicitud = DatosSolicitud()
        self.contrato = Contrato()
        self.cliente = Cliente()
        self.medida = Medida()
        self.doctecnica = DocTecnica()
        self.comentario = Comentarios()
        self.registro = RegistrosDocumento()
        self.cnae = XmlField('CNAE')
        self.vivenda = XmlField('ViviendaHabitual')
        self.tipuscanvititular = XmlField('TipoCambioTitular')
        super(CambiodeComercializadoraConCambios, self).\
                    __init__('CambiodeComercializadoraSinCambios', 'cambio')


class MensajeCambiodeComercializadoraConCambios(XmlModel):
    _sort_order = ('mensaje', 'cabecera', 'cambio')

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField('MensajeCambiodeComercializadoraConCambios', 
                          attributes={
                              'xmlns': 'http://localhost/elegibilidad'
                           })
        self.cabecera = Cabecera()
        self.cambio = CambiodeComercializadoraConCambios()
        super(MensajeCambiodeComercializadoraConCambios, self).\
               __init__('MensajeCambiodeComercializadoraConCambios', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class AceptacionCambiodeComercializadoraConCambios(XmlModel):
    _sort_order = ('acceptacio', 'dades', 'contracte')

    def __init__(self):
        self.acceptacio = \
                       XmlField('AceptacionCambiodeComercializadoraConCambios')
        self.dades = DatosAceptacion()
        self.contracte = Contrato()
        super(AceptacionCambiodeComercializadoraConCambios, self).\
         __init__('AceptacionCambiodeComercializadoraConCambios', 'acceptacio')


class MensajeAceptacionCambiodeComercializadoraConCambios(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'acceptacio')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeAceptacionCambiodeComercializadoraConCambios',
                         attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.acceptacio = AceptacionCambiodeComercializadoraConCambios() 
        super(MensajeAceptacionCambiodeComercializadoraConCambios, self).\
                __init__('MensajeAceptacionCambiodeComercializadoraConCambios',
                         'missatge')
        
    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class IncidenciasATRDistribuidoras(XmlModel):
    _sort_order = ('incidenciaatr', 'incidencies')

    def __init__(self):
        self.incidenciaatr = XmlField('IncidenciasATRDistribuidoras')
        self.incidencies = [] #Mateixos camps que el rechazo, pero amb tag Incidencia
        super(IncidenciasATRDistribuidoras, self).\
                __init__('IncidenciasATRDistribuidoras', 'incidenciaatr')


class MensajeIncidenciasATRDistribuidoras(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'incidencia')
    
    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeIncidenciasATRDistribuidoras',
                     attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.incidencia = IncidenciasATRDistribuidoras()
        super(MensajeIncidenciasATRDistribuidoras, self).\
                     __init__('MensajeIncidenciasATRDistribuidoras', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
        

class ActivacionCambiodeComercializadoraConCambios(XmlModel):
    _sort_order = ('activacio', 'dades', 'contracte', 'punts_mesura')
    
    def __init__(self):
        self.activacio = XmlField('ActivacionCambiodeComercializadoraConCambios')
        self.dades = DatosActivacion()
        self.contracte = Contrato()
        self.punts_mesura = PuntosDeMedida()
        super(ActivacionCambiodeComercializadoraConCambios, self).\
                __init__('ActivacionCambiodeComercializadoraConCambios', 'activacio')


class MensajeActivacionCambiodeComercializadoraConCambios(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'activacio')

    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField('MensajeActivacionCambiodeComercializadoraConCambios',
                     attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.activacio = ActivacionCambiodeComercializadoraConCambios()
        super(MensajeActivacionCambiodeComercializadoraConCambios, self).\
                     __init__('MensajeActivacionCambiodeComercializadoraConCambios', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
