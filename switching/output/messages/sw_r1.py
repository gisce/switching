# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField

from sw_c1 import Cliente, Nombre, Telefono, Contacto
from sw_w1 import LecturaAportada


class CabeceraReclamacion(XmlModel):
    _sort_order = ('cabecera', 'ree_emisora', 'ree_destino', 'proceso', 'paso',
                   'solicitud', 'secuencia', 'fecha', 'cups')

    def rep_solicitud(self, codsol):
        codsol = ''.join([x for x in codsol if x.isalnum()])
        return codsol.ljust(12, '0')[:12]

    def rep_fecha(self, fecha):
        if len(fecha.strip()) == 10:
            #We do not have time so add it
            fecha += ' 00:00:00'
        return 'T'.join(fecha.split(' '))

    def __init__(self):
        self.cabecera = XmlField('CabeceraReclamacion')
        self.ree_emisora = XmlField('CodigoREEEmpresaEmisora')
        self.ree_destino = XmlField('CodigoREEEmpresaDestino')
        self.proceso = XmlField('CodigoDelProceso')
        self.paso = XmlField('CodigoDePaso')
        self.solicitud = XmlField('CodigoDeSolicitud', rep=self.rep_solicitud)
        self.secuencia = XmlField('SecuencialDeSolicitud')
        self.fecha = XmlField('FechaSolicitud', rep=self.rep_fecha)
        self.cups = XmlField('CUPS')
        super(CabeceraReclamacion, self).__init__('CabeceraReclamacion',
                                                  'cabecera')


class DatosSolicitud(XmlModel):
    _sort_order = ('dades', 'tipus', 'subtipus', 'ref_origen')

    def __init__(self):
        self.dades = XmlField('DatosSolicitud')
        self.tipus = XmlField('Tipo')
        self.subtipus = XmlField('Subtipo')
        self.ref_origen = XmlField('ReferenciaOrigen')
        super(DatosSolicitud, self).__init__('DatosSolicitud',
                                             'dades')


class LecturasAportadas(XmlModel):
    _sort_order = ('lecturesaportades', 'lectures')

    def __init__(self):
        self.lecturesaportades = XmlField('LecturasAportadas')
        self.lectures = []
        super(LecturasAportadas, self).__init__(
            'LecturasAportadas', 'lecturesaportades')


class VariableDetalleReclamacion(XmlModel):
    _sort_order = ('variable', 'num_expedient', 'data_incident',
                   'num_factura_atr', 'tipus_concepte_facturat', 'data_lectura',
                   'codidh', 'lectures', 'codi_incidencia', 'codi_sollicitud',
                   'param_contractacio', 'concepte_disconformitat',
                   'tipus_atencio_incorrecte', 'iban', 'contacto',
                   'codi_sollicitud_reclamacio', 'data_inici', 'data_fins',
                   'import_reclamat', 'ubicacio'
                   )

    def __init__(self):
        self.variable = XmlField('VariableDetalleReclamacion')
        self.numexpedient = XmlField('NumExpedienteAcometida')
        self.data_incident = XmlField('FechaIncidente')
        self.num_factura_atr = XmlField('NumFacturaATR')
        self.tipus_concepte_facturat = XmlField('TipoConceptoFacturado')
        self.data_lectura = XmlField('FechaLectura')
        self.codidh = XmlField('CodigoDH')
        self.lectures = LecturasAportadas()
        self.codi_incidencia = XmlField('CodigoIncidencia')
        self.codi_sollicitud = XmlField('CodigoSolicitud')
        self.param_contractacio = XmlField('ParametroContratacion')
        self.concepte_disconformitat = XmlField('ConceptoDisconformidad')
        self.tipus_atencio_incorrecte = XmlField('TipoDeAtencionIncorrecta')
        self.iban = XmlField('IBAN')
        self.contacto = Contacto()
        self.codi_sollicitud_reclamacio = XmlField('CodigoSolicitudReclamacion')
        self.data_inici = XmlField('FechaDesde')
        self.data_fins = XmlField('FechaHasta')
        self.import_reclamat = XmlField('ImporteReclamado')
        self.ubicacio = XmlField('UbicacionIncidencia')

        super(VariableDetalleReclamacion, self).__init__(
            'VariableDetalleReclamacion', 'variable')


class VariablesDetalleReclamacion(XmlModel):
    _sort_order = ('variables', 'detalls')

    def __init__(self):
        self.variables = XmlField('VariablesDetalleReclamacion')
        self.detalls = []
        super(VariablesDetalleReclamacion, self).__init__(
            'VariablesDetalleReclamacion', 'variables', drop_empty=False)


class IdReclamante(XmlModel):
    _sort_order = ('id_reclamant', 'tipus_cifnif', 'identificador')

    def __init__(self):
        self.id_reclamant = XmlField('IdReclamante')
        self.tipus_cifnif = XmlField('TipoCIFNIF')
        self.identificador = XmlField('Identificador')
        super(IdReclamante, self).__init__(
            'IdReclamante', 'id_reclamant')


class Reclamante(XmlModel):
    _sort_order = ('reclamant', 'id_reclamant', 'nom', 'fax', 'telefon',
                   'correu')

    def __init__(self):
        self.reclamant = XmlField('Reclamante')
        self.id_reclamant = IdReclamante()
        self.nom = Nombre()
        self.fax = Telefono()
        self.telefon = Telefono()
        self.correu = XmlField('CorreoElectronico')
        super(Reclamante, self).__init__(
            'Reclamante', 'reclamant')


class RegistroDoc(XmlModel):
    _sort_order = ('documento', 'tipus_doc', 'url')

    def __init__(self):
        self.documento = XmlField('RegistroDoc')
        self.tipus_doc = XmlField('TipoDocAportado')
        self.url = XmlField('DireccionUrl')
        super(RegistroDoc, self).__init__('RegistroDoc', 'documento')


class RegistrosDocumento(XmlModel):
    _sort_order = ('registros', 'documents')

    def __init__(self):
        self.registros = XmlField('RegistrosDocumento')
        self.documents = []
        super(RegistrosDocumento, self).__init__(
            'RegistrosDocumento', 'registros')


class SolicitudReclamacion(XmlModel):
    _sort_order = ('solicitud', 'dades', 'variables', 'client',
                   'tipus_reclamant', 'reclamant', 'comentaris',
                   'reg_documents')

    def __init__(self):
        self.solicitud = XmlField('SolicitudReclamacion')
        self.dades = DatosSolicitud()
        self.variables = VariablesDetalleReclamacion()
        self.client = Cliente()
        self.tipus_reclamant = XmlField('TipoReclamante')
        self.reclamant = Reclamante()
        self.comentaris = XmlField('Comentarios')
        self.reg_documents = RegistrosDocumento()
        super(SolicitudReclamacion, self).__init__('SolicitudReclamacion',
                                                   'solicitud')


class DatosAceptacion(XmlModel):
    _sort_order = (
        'dades_acceptacio',
        'data_acceptacio',
        'codi_reclamacio'
    )

    def __init__(self):
        self.dades_acceptacio = XmlField('DatosAceptacion')
        self.data_acceptacio = XmlField('FechaAceptacion')
        self.codi_reclamacio = XmlField('CodigoReclamacionDistribuidora')
        super(DatosAceptacion, self).__init__(
            'DatosAceptacion', 'dades_acceptacio'
        )


class AceptacionReclamacion(XmlModel):
    _sort_order = (
        'acceptacio_reclamacio',
        'dades_acceptacio',
    )

    def __init__(self):
        self.acceptacio_reclamacio = XmlField('AceptacionReclamacion')
        self.dades_acceptacio = DatosAceptacion()

        super(AceptacionReclamacion, self).__init__(
            'AceptacionReclamacion', 'acceptacio_reclamacio'
        )


class RechazoReclamacion(XmlModel):
    _sort_order = ('rechazo', 'secuencial', 'motiu', 'comentaris')

    def __init__(self, tagname=None):
        if not tagname:
            tagname = 'Rechazo'
        self.rechazo = XmlField(tagname)
        self.secuencial = XmlField('Secuencial')
        self.motiu = XmlField('CodigoMotivo', rep=lambda x: x.rjust(2, '0'))
        self.comentaris = XmlField('Comentarios')
        super(RechazoReclamacion, self).__init__(tagname, 'rechazo')


class RechazosReclamacion(XmlModel):
    _sort_order = ('rebuigs_reclamacio', 'rebuigs')

    def __init__(self):
        self.rebuigs_reclamacio = XmlField('Rechazos')
        self.rebuigs = []
        super(RechazosReclamacion, self).__init__(
            'Rechazos', 'rebuigs_reclamacio'
        )


# 01
class MensajeReclamacionIncidenciaPeticion(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'solicitud',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'MensajeReclamacionIncidenciaPeticion',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = CabeceraReclamacion()
        self.solicitud = SolicitudReclamacion()
        super(MensajeReclamacionIncidenciaPeticion, self).__init__(
            'MensajeReclamacionIncidenciaPeticion', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


# 02_ok
class MensajeAceptacionReclamacion(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'acceptacio',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'MensajeAceptacionReclamacion',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = CabeceraReclamacion()
        self.acceptacio = AceptacionReclamacion()
        super(MensajeAceptacionReclamacion, self).__init__(
            'MensajeAceptacionReclamacion', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


# 02_ko
class MensajeRechazoReclamacion(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'data',
        'rebuigs',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'MensajeRechazoReclamacion',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = CabeceraReclamacion()
        self.data = XmlField('Fecha')
        self.rebuigs = RechazosReclamacion()
        super(MensajeRechazoReclamacion, self).__init__(
            'MensajeRechazoReclamacion', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()



class DatosCierre(XmlModel):
    _sort_order = ('dades','num_expediente_acometida','data','hora','tipus',
    'subtipus','codi_reclamacio_distri','resultat_reclamacio',
    'detall_resultat','observacions','indemnitzacio_abonada',
    'num_expedient_anomalia_frau','data_moviment','codi_sollicitud'
    )

    def __init__(self):
        self.dades = XmlField('DatosCierre')
        self.num_expediente_acometida = XmlField('NumExpedienteAcometida')
        self.data = XmlField('Fecha')
        self.hora = XmlField('Hora')
        self.tipus = XmlField('Tipo')
        self.subtipus = XmlField('Subtipo')
        self.codi_reclamacio_distri = XmlField(
            'CodigoReclamacionDistribuidora'
        )
        self.resultat_reclamacio = XmlField('ResultadoReclamacion')
        self.detall_resultat = XmlField('DetalleResultado')
        self.observacions = XmlField('Observaciones')
        self.indemnitzacio_abonada = XmlField('IndemnizacionAbonada')
        self.num_expedient_anomalia_frau = XmlField(
            'NumExpedienteAnomaliaFraude'
        )
        self.data_moviment = XmlField('FechaMovimiento')
        self.codi_sollicitud = XmlField('CodigoSolicitud')
        super(DatosCierre, self).__init__('DatosCierre','dades')


class Retificacion(XmlModel):
    """ Retificacion Model """
    _sort_order = ('retificacio', 'tipus', 'subtipus',
                   'descripcio_retificacio')

    def __init__(self):
        self.retificacio = XmlField('Retipificacion')
        self.tipus = XmlField('Tipo')
        self.subtipus = XmlField('Subtipo')
        self.descripcio_retificacio = XmlField('DescRetipificacion')
        super(Retificacion, self).__init__('Retipificacion', 'retificacio')


class CierreReclamacion(XmlModel):
    _sort_order = ('tancament', 'dades', 'retificacio', 'cod_contracte',
                   'comentaris', 'reg_documents', )

    def __init__(self):
        self.tancament = XmlField('CierreReclamacion')
        self.dades = DatosCierre()
        self.retificacio = Retificacion()
        self.cod_contracte = XmlField('CodContrato')
        self.comentaris = XmlField('Comentarios')
        self.reg_documents = RegistrosDocumento()
        super(CierreReclamacion, self).__init__('CierreReclamacion',
                                                'tancament')


# 05
class MensajeCierreReclamacion(XmlModel):
    """ R1-05 Root class
    """
    _sort_order = (
        'mensaje',
        'capcalera',
        'tancament',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'MensajeCierreReclamacion',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = CabeceraReclamacion()
        self.tancament = CierreReclamacion()
        super(MensajeCierreReclamacion,
              self).__init__('MensajeCierreReclamacion', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()

# 03
class MensajePeticionInformacionAdicionalReclamacion(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'informacio_adicional',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'MensajePeticionInformacionAdicionalReclamacion',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = CabeceraReclamacion()
        self.informacio_adicional = InformacionAdicional()
        super(MensajePeticionInformacionAdicionalReclamacion, self).__init__(
            'MensajePeticionInformacionAdicionalReclamacion', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class InformacionAdicional(XmlModel):
    _sort_order = ('info_adicional', 'dades_informacio', 'info_intermitja',
                   'retificacio', 'sollicituds_info_adicional', 'comentaris', )

    def __init__(self):
        self.info_adicional = XmlField('InformacionAdicional')
        self.dades_informacio = DatosInformacion()
        self.info_intermitja = InformacionIntermedia()
        self.retificacio = Retificacion()
        self.sollicituds_info_adicional = SolicitudesInformacionAdicional()
        self.comentaris = XmlField('Comentarios')
        super(InformacionAdicional, self).__init__('InformacionAdicional',
                                                    'info_adicional')


class DatosInformacion(XmlModel):
    _sort_order = ('dades_informacio', 'num_expedient', 'tipus_comunicacio',
                   'codi_reclamant_distri')

    def __init__(self):
        self.dades_informacio = XmlField('DatosInformacion')
        self.num_expedient = XmlField('NumExpedienteAcometida')
        self.tipus_comunicacio = XmlField('TipoComunicacion')
        self.codi_reclamant_distri = XmlField('CodigoReclamacionDistribuidora')
        super(DatosInformacion, self).__init__('DatosInformacion',
                                               'dades_informacio')


class InformacionIntermedia(XmlModel):
    _sort_order = ('info_intermitja', 'desc_info_intermitja', 'intervencions', )

    def __init__(self):
        self.info_intermitja = XmlField('InformacionIntermedia')
        self.desc_info_intermitja = XmlField('DescInformacionIntermedia')
        self.intervencions = Intervenciones()
        super(InformacionIntermedia, self).__init__('InformacionIntermedia',
                                                    'info_intermitja')

class Intervencion(XmlModel):
    _sort_order = ('intervencio', 'tipus_intervencio', 'data', 'hora_desde',
                   'hora_fins', 'num_visita', 'resultat', 'detalls_resultat', )

    def __init__(self):
        self.intervencio = XmlField('Intervencion')
        self.tipus_intervencio = XmlField('TipoIntervencion')
        self.data = XmlField('Fecha')
        self.hora_desde = XmlField('HoraDesde')
        self.hora_fins = XmlField('HoraHasta')
        self.num_visita = XmlField('NumeroVisita')
        self.resultat = XmlField('Resultado')
        self.detalls_resultat = XmlField('DetalleResultado')

        super(Intervencion, self).__init__('Intervencion', 'intervencio')


class Intervenciones(XmlModel):
    _sort_order = ('intervencions', 'detalls')

    def __init__(self):
        self.intervencions = XmlField('Intervenciones')
        self.detalls = []
        super(Intervenciones, self).__init__(
            'Intervenciones', 'intervencions')


class SolicitudInformacionAdicional(XmlModel):
    _sort_order = ('sollicitud_info', 'tipus_info', 'desc_peticio_info',
                   'data_limit', )

    def __init__(self):
        self.sollicitud_info = XmlField('SolicitudInformacionAdicional')
        self.tipus_info = XmlField('TipoInformacionAdicional')
        self.desc_peticio_info = XmlField('DescPeticionInformacion')
        self.data_limit = XmlField('FechaLimiteEnvio')

        super(SolicitudInformacionAdicional, self).__init__('SolicitudInformacionAdicional',
                                           'sollicitud_info')


class SolicitudesInformacionAdicional(XmlModel):
    _sort_order = ('sollicituds_info', 'detalls')

    def __init__(self):
        self.sollicituds_info = XmlField('SolicitudesInformacionAdicional')
        self.detalls = []
        super(SolicitudesInformacionAdicional, self).__init__(
            'SolicitudesInformacionAdicional', 'sollicituds_info')


# 04
class MensajeEnvioInformacionReclamacion(XmlModel):
    _sort_order = (
        'mensaje',
        'capcalera',
        'enviament_info_reclamacio',
    )

    def __init__(self):
        self.doc_root = None
        self.mensaje = XmlField(
            'MensajeEnvioInformacionReclamacion',
            attributes={
                'xmlns': 'http://localhost/elegibilidad',
            }
        )
        self.capcalera = CabeceraReclamacion()
        self.enviament_info_reclamacio = EnvioInformacionReclamacion()
        super(MensajeEnvioInformacionReclamacion, self).__init__(
            'MensajeEnvioInformacionReclamacion', 'mensaje')

    def set_agente(self, agente):
        self.mensaje.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()


class EnvioInformacionReclamacion(XmlModel):
    _sort_order = ('enviament_info_reclamacio', 'dades_enviament_info',
                   'variables_aportacio_info', 'comentaris', 'reg_doc',)

    def __init__(self):
        self.enviament_info_reclamacio = XmlField('EnvioInformacionReclamacion')
        self.dades_enviament_info = DatosEnvioInformacion()
        self.variables_aportacio_info = VariablesAportacionInformacion()
        self.comentaris = XmlField('Comentarios')
        self.reg_doc = RegistrosDocumento()
        super(EnvioInformacionReclamacion, self).__init__(
            'EnvioInformacionReclamacion', 'enviament_info_reclamacio')


class DatosEnvioInformacion(XmlModel):
    _sort_order = ('dades_enviament_info', 'num_expedient', 'data_informacio')

    def __init__(self):
        self.dades_enviament_info = XmlField('DatosEnvioInformacion')
        self.num_expedient = XmlField('NumExpedienteAcometida')
        self.data_informacio = XmlField('FechaInformacion')
        super(DatosEnvioInformacion, self).__init__(
                'DatosEnvioInformacion', 'dades_enviament_info')


class VariablesAportacionInformacion(XmlModel):
    _sort_order = ('variables_aportacio_info', 'detalls')

    def __init__(self):
        self.variables_aportacio_info = XmlField('VariablesAportacionInformacion')
        self.detalls = []
        super(VariablesAportacionInformacion, self).__init__(
            'VariablesAportacionInformacion', 'variables_aportacio_info')


class VariableAportacionInformacion(XmlModel):
    _sort_order = ('variable_aportacio_info', 'tipus_info', 'desc_peticio_info',
                   'variable', 'valor', )

    def __init__(self):
        self.variable_aportacio_info = XmlField('VariableAportacionInformacion')
        self.tipus_info = XmlField('TipoInformacion')
        self.desc_peticio_info = XmlField('DescPeticionInformacion')
        self.variable = XmlField('Variable')
        self.valor = XmlField('Valor')

        super(VariableAportacionInformacion, self).__init__(
            'VariableAportacionInformacion', 'variable_aportacio_info')
