# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField

from sw_c1 import Cliente, Nombre, Telefono


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


class VariableDetalleReclamacion(XmlModel):
    _sort_order = ('variable', 'num_expedient')

    def __init__(self):
        self.variable = XmlField('VariableDetalleReclamacion')
        #self.num_expedient = XmlField('NumExpedienteAcometida')
        super(VariableDetalleReclamacion, self).__init__(
            'VariableDetalleReclamacion', 'variable', drop_empty=False)


class VariablesDetalleReclamacion(XmlModel):
    _sort_order = ('variables', 'detalls')

    def __init__(self):
        self.variables = XmlField('VariablesDetalleReclamacion')
        self.detalls = XmlField('VariableDetalleReclamacion')
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
        self.reg_documents = XmlField('RegistrosDocumentos')
        super(SolicitudReclamacion, self).__init__('SolicitudReclamacion',
                                                   'solicitud')


#01
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
