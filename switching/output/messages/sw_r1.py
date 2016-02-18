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
    _sort_order = ('variable', 'num_expedient', 'data_incident', 'num_factura'
                   'tipus_concepte_facturat', 'codi_dh', 'lectures',
                   'codi_incidencia', 'codi_solicitud',
                   'parametre_contractacio', 'concepte_disconformitat',
                   'tipus_atencio_incorrecte', 'iban', 'contacto',
                   'codi_solicitud_reclamacio', 'fecha_desde', 'fecha_hasta',
                   'import_reclamat', 'ubicacio_incidencia'
                   )

    def __init__(self):
        self.variable = XmlField('VariableDetalleReclamacion')
        self.num_expedient = XmlField('NumExpedienteAcometida')
        self.fecha_incidente = XmlField('NumExpedienteAcometida')
        self.num_factura = XmlField('NumFacturaATR')
        self.tipus_concepte_facturat = XmlField('TipoConceptoFacturado')
        self.codigodh = XmlField('CodigoDH')
        self.lectures = LecturasAportadas()
        self.codi_incidencia = XmlField('CodigoIncidencia')
        self.codi_incidencia = XmlField('CodigoSolicitud')
        self.parametre_contractacio = XmlField('ParametroContractacion')
        self.concepte_disconformitat = XmlField('ConceptoDisconformidad')
        self.tipus_atencio_incorrecte = XmlField('TipoDeAtencionIncorrecta')
        self.iban = XmlField('IBAN')
        self.contacto = Contacto()
        self.codi_solicitud_reclamacio = XmlField('CodigoSolicitudReclamacion')
        self.fecha_desde = XmlField('FechaDesde')
        self.fecha_hasta = XmlField('FechaHasta')
        self.import_reclamat = XmlField('ImporteReclamado')
        self.ubicacio_incidencia = XmlField('UbicacionIncidencia')

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
