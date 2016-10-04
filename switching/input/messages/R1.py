# -*- coding: utf-8 -*-
from switching.helpers.funcions import get_rec_attr

from message import Message
import C1
import W1
from ...defs import SUBTYPES_R101


class R1(Message):
    """Classe que implementa R1."""

    def set_xsd(self):
        super(R1, self).set_xsd()
        if self._header == 'ReclamacionPeticion':
            self._header = 'SolicitudReclamacion'
        else:
            pass

    @property
    def header(self):
        return self._header

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        tree = 'SolicitudReclamacion.DatosSolicitud'
        sol = get_rec_attr(self.obj, tree, False)
        if sol:
            return DatosPasoSollicitud(sol)
        else:
            return False

    @property
    def reclamacions(self):
        """Retorna una llista de Reclamacions"""
        data = []
        try:
            varis = self.obj.SolicitudReclamacion.VariablesDetalleReclamacion
            for var in varis.VariableDetalleReclamacion:
                if len(var.getchildren()):
                    data.append(
                        VariableDetalleReclamacion(
                            var
                        )
                    )
        except AttributeError:
            pass
        return data

    @property
    def client(self):
        """Retorna l'objecte Client"""
        obj = getattr(self.obj, self._header)
        if len(getattr(obj, 'Cliente', [])):
            return C1.Client(obj.Cliente)

    @property
    def tipus_reclamant(self):
        """Retorna l'objecte Tipo Reclamante"""
        tree = 'SolicitudReclamacion.TipoReclamante.text'
        return get_rec_attr(self.obj, tree, '')

    @property
    def reclamant(self):
        """Retorna l'objecte Client"""
        obj = getattr(self.obj, self._header)
        if len(getattr(obj, 'Reclamante', [])):
            return C1.Client(obj.Reclamante, 'IdReclamante')

    @property
    def comentaris(self):
        """Retorna els comentaris (si hi son)"""
        obj = getattr(self.obj, self._header)
        if len(getattr(obj, 'Comentarios', [])):
            return obj.Comentarios.text
        else:
            return ''

    @property
    def documents(self):
        """Return docuemnts if availables"""
        obj = getattr(self.obj, self._header)
        registros = getattr(obj, 'RegistrosDocumento', [])
        doc_registry = C1.RegistrosDocumento(registros)
        return doc_registry.get_documents()

    # 02 KO
    @property
    def data(self):
        """ Data Rebuig """
        data = None
        try:
            return self.obj.Fecha.text
        except AttributeError:
            pass
        return data

    @property
    def rebuig(self):
        """Retorna una llista de Rebuig"""
        data = []
        for i in self.obj.Rechazos.Rechazo:
            data.append(C1.Rebuig(i))
        return data

    # 02 OK
    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        try:
            obj = getattr(self.obj, self._header, False)
            return C1.Acceptacio(obj.DatosAceptacion)
        except AttributeError:
            return False

    # 03
    @property
    def informacio_adicional(self):
        """Retorna l'objecte InformacionAdicional"""
        return InformacionAdicional(self.obj.InformacionAdicional)


    # 05
    @property
    def tancament(self):
        """Retorna l'objecte Activacio"""
        return Cierre(self.obj.CierreReclamacion)

    # @property
    # def anullacio(self):
    #     """Retorna l'object Anullacio"""
    #     return C1.Anullacio(self.obj.AnulacionSolicitud)
    #
    #
    # @property
    # def rebuig_anullacio(self):
    #     """Retorna l'objecte Rebuig"""
    #     data = []
    #     for i in self.obj.RechazoDeAnulacion.RechazoAnulacion:
    #         data.append(C1.Rebuig(i))
    #     return data
    #
    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self.header)
        if hasattr(obj, 'Contrato'):
            try:
                idcontrato = C1.Contracte(obj.IdContrato)
            except AttributeError:
                # Step 04 Acceptacio has the classic structure
                idcontrato = C1.Contracte(obj.Contrato)
            return idcontrato
        else:
            return None
    #
    # @property
    # def direccio_correspondecia(self):
    #     direccio = False
    #     try:
    #         direccio = DireccioAmbIndicador(self.obj.BajaEnergia.DireccionCorrespondencia)
    #     except AttributeError:
    #         pass
    #     return direccio
    # @property
    # def punts_mesura(self):
    #     """Retorna una llista de punts de mesura"""
    #     data = []
    #     obj = getattr(self.obj, self._header)
    #     for i in obj.PuntosDeMedida.PuntoDeMedida:
    #         data.append(C1.PuntMesura(i))
    #     return data

    def get_subtypes(self, type):
        return [x['code'] for x in SUBTYPES_R101 if x['type'] == type]

    def get_type_from_subtype(self, subtype):
        for x in SUBTYPES_R101:
            if x['code'] == subtype:
                return x['type']
        return []


class DatosPasoSollicitud(object):
    """Classe que implementa la sol·licitud"""

    def __init__(self, data):
        self.sollicitud = data

    @property
    def tipus(self):
        return self.sollicitud.Tipo.text

    @property
    def subtipus(self):
        return self.sollicitud.Subtipo.text

    @property
    def sollicitudadm(self):
        """Referència orígen"""
        ref = None
        try:
            ref = self.sollicitud.ReferenciaOrigen.text
        except AttributeError:
            pass
        return ref


class VariableDetalleReclamacion(object):
    """Classe que implementa la sol·licitud"""

    def __init__(self, data):
        self.variable = data

    @property
    def numexpedient(self):
        """ Número de expediente """
        ref = None
        try:
            return self.variable.NumExpedienteAcometida.text
        except AttributeError:
            pass
        return ref

    @property
    def data_incident(self):
        """ Data incident """
        data = None
        try:
            return self.variable.FechaIncidente.text
        except AttributeError:
            pass
        return data

    @property
    def num_factura_atr(self):
        """ Num factura ATR """
        num = None
        try:
            return self.variable.NumFacturaATR.text
        except AttributeError:
            pass
        return num

    @property
    def tipus_concepte_facturat(self):
        """ Tipus Concepte """
        tipus = None
        try:
            return self.variable.TipoConceptoFacturado.text
        except AttributeError:
            pass
        return tipus

    @property
    def data_lectura(self):
        """ Data lectura """
        data = None
        try:
            return self.variable.FechaLectura.text
        except AttributeError:
            pass
        return data

    @property
    def codidh(self):
        """ Codi DH """
        codi = None
        try:
            return int(self.variable.CodigoDH.text)
        except AttributeError:
            pass
        return codi

    @property
    def lectures(self):
        """Retorna una llista de lectures"""
        data = []
        try:
            varis = self.variable.LecturasAportadas
            for var in varis.LecturaAportada:
                if len(var.getchildren()):
                    data.append(
                        W1.LecturaAportada(
                            var
                        )
                    )
        except AttributeError:
            pass
        return data

    @property
    def codi_incidencia(self):
        """ Data incidencia """
        codi = None
        try:
            return self.variable.CodigoIncidencia.text
        except AttributeError:
            pass
        return codi

    @property
    def codi_sollicitud(self):
        """ Data solicitud """
        codi = None
        try:
            return self.variable.CodigoSolicitud.text
        except AttributeError:
            pass
        return codi

    @property
    def param_contractacio(self):
        """ Paràmetre de contractació """
        param = None
        try:
            return self.variable.ParametroContratacion.text
        except AttributeError:
            pass
        return param

    @property
    def concepte_disconformitat(self):
        """ Concepte de disconformitat """
        con = None
        try:
            return self.variable.ConceptoDisconformidad.text
        except AttributeError:
            pass
        return con

    @property
    def tipus_atencio_incorrecte(self):
        """ Tipus atenció incorrete """
        tipus = None
        try:
            return self.variable.TipoDeAtencionIncorrecta.text
        except AttributeError:
            pass
        return tipus

    @property
    def contacto(self):
        """ Número de expediente """
        contacto = None
        try:
            contacto = C1.Contacto(self.variable.Contacto)
        except AttributeError:
            pass
        return contacto

    @property
    def iban(self):
        """ IBAN """
        iban = None
        try:
            return self.variable.IBAN.text
        except AttributeError:
            pass
        return iban

    @property
    def codi_sollicitud_reclamacio(self):
        """ Codi solicitud de reclamació """
        codi = None
        try:
            return self.variable.CodigoSolicitudReclamacion.text
        except AttributeError:
            pass
        return codi

    @property
    def data_inici(self):
        """ Data inici """
        data = None
        try:
            return self.variable.FechaDesde.text
        except AttributeError:
            pass
        return data

    @property
    def data_fins(self):
        """ Data fi """
        data = None
        try:
            return self.variable.FechaHasta.text
        except AttributeError:
            pass
        return data

    @property
    def import_reclamat(self):
        """ Import Reclamat """
        imp = None
        try:
            return float(self.variable.ImporteReclamado.text)
        except AttributeError:
            pass
        return imp

    @property
    def ubicacio(self):
        """ Import Reclamat """
        ubi = None
        try:
            return self.variable.UbicacionIncidencia.text
        except AttributeError:
            pass
        return ubi


class Cierre(object):
    """Classe que implementa el tancament"""

    def __init__(self, data):
        self.cierre = data

    @property
    def dades_tancament(self):
        """Retorna l'objecte Dades de tancament"""
        try:
            return DatosCierre(self.cierre.DatosCierre)
        except AttributeError, e:
            return None

    @property
    def retipificacio(self):
        """Retorna l'objecte Retificacio"""
        try:
            return Retipificacio(self.cierre.Retipificacion)
        except AttributeError, e:
            return None

    @property
    def codi_contracte(self):
        try:
            return self.cierre.CodContrato.text
        except AttributeError, e:
            return ''

    @property
    def comentaris(self):
        try:
            return self.cierre.Comentarios.text
        except AttributeError, e:
            return ''


class DatosCierre(object):
    """Classe que implementa les dades del tancament"""

    def __init__(self, data):
        self.dadescierre = data

    @property
    def num_expediente_acometida(self):
        try:
            return self.dadescierre.NumExpedienteAcometida.text
        except AttributeError, e:
            return ''

    @property
    def data(self):
        try:
            return self.dadescierre.Fecha.text
        except AttributeError, e:
            return ''

    @property
    def hora(self):
        try:
            return self.dadescierre.Hora.text
        except AttributeError, e:
            return ''

    @property
    def tipus(self):
        try:
            return self.dadescierre.Tipo.text
        except AttributeError, e:
            return ''

    @property
    def subtipus(self):
        try:
            return self.dadescierre.Subtipo.text
        except AttributeError, e:
            return ''
    @property
    def codi_reclamacio_distri(self):
        try:
            return self.dadescierre.CodigoReclamacionDistribuidora.text
        except AttributeError, e:
            return ''

    @property
    def resultat_reclamacio(self):
        try:
            return self.dadescierre.ResultadoReclamacion.text
        except AttributeError, e:
            return ''

    @property
    def detall_resultat(self):
        try:
            return self.dadescierre.DetalleResultado.text
        except AttributeError, e:
            return ''

    @property
    def observacions(self):
        try:
            return self.dadescierre.Observaciones.text
        except AttributeError, e:
            return ''

    @property
    def indemnitzacio_abonada(self):
        try:
            return float(self.dadescierre.IndemnizacionAbonada.text)
        except AttributeError, e:
            return 0.0

    @property
    def num_expedient_anomalia_frau(self):
        try:
            return self.dadescierre.NumExpedienteAnomaliaFraude.text
        except AttributeError, e:
            return ''

    @property
    def data_moviment(self):
        try:
            return self.dadescierre.FechaMovimiento.text
        except AttributeError, e:
            return ''

    @property
    def codi_sollicitud(self):
        try:
            return self.dadescierre.CodigoSolicitud.text
        except AttributeError, e:
            return ''


class Retipificacio(object):
    def __init__(self, data):
        self.retipificacio = data

    @property
    def tipus(self):
        return self.retipificacio.Tipo.text

    @property
    def subtipus(self):
        return self.retipificacio.Subtipo.text

    @property
    def descripcio_retipificacio(self):
        """Referència orígen"""
        ref = None
        try:
            ref = self.retipificacio.DescRetipificacion.text
        except AttributeError, e:
            pass
        return ref


class InformacionAdicional(object):
    """Classe que implementa la informacio addicional"""

    def __init__(self, data):
        self.info = data

    @property
    def dades_informacio(self):
        """Retorna l'objecte Dades de informacio"""
        try:
            return DatosInformacion(self.info.DatosInformacion)
        except AttributeError, e:
            return None

    @property
    def informacio_intermitja(self):
        """Retorna l'objecte Informacio Intermitja"""
        try:
            return InformacionIntermedia(self.info.InformacionIntermedia)
        except AttributeError, e:
            return None

    @property
    def retipificacio(self):
        """Retorna l'objecte Retificacio"""
        try:
            return Retipificacio(self.info.Retipificacion)
        except AttributeError, e:
            return None

    @property
    def sollicituds_info_addicional(self):
        """Retorna una llista de Solicituds de informacio adicional"""
        data = []
        try:
            for i in self.info.SolicitudesInformacionAdicional.SolicitudInformacionAdicional:
                if len(i.getchildren()):
                    data.append(SolicitudInformacionAdicional(i))
        except AttributeError:
            pass
        return data

    @property
    def comentaris(self):
        try:
            return self.info.Comentarios.text
        except AttributeError, e:
            return ''


class DatosInformacion(object):
    def __init__(self, data):
        self.dades_info = data

    @property
    def num_expedient_acometida(self):
        ref = None
        try:
            ref = self.dades_info.NumExpedienteAcometida.text
        except AttributeError, e:
            pass
        return ref

    @property
    def tipus_comunicacio(self):
        return self.dades_info.TipoComunicacion.text

    @property
    def codi_reclamacio_distri(self):
            return self.dades_info.CodigoReclamacionDistribuidora.text


class InformacionIntermedia(object):
    def __init__(self, data):
        self.info_intermitja = data

    @property
    def descripcio_info_intermitja(self):
        ref = None
        try:
            ref = self.info_intermitja.DescInformacionIntermedia.text
        except AttributeError, e:
            pass
        return ref

    @property
    def intervencions(self):
        """Retorna una llista de intervencions"""
        data = []
        try:
            for i in self.info_intermitja.Intervenciones.Intervencion:
                if len(i.getchildren()):
                    data.append(Intervencion(i))
        except AttributeError:
            pass
        return data


class SolicitudInformacionAdicional(object):
    def __init__(self, data):
        self.solicitud_info = data

    @property
    def tipus_info_adicional(self):
        return self.solicitud_info.TipoInformacionAdicional.text

    @property
    def descripcio_peticio_informacio(self):
        ref = None
        try:
            ref = self.solicitud_info.DescPeticionInformacion.text
        except AttributeError, e:
            pass
        return ref

    @property
    def data_limit(self):
        return self.solicitud_info.FechaLimiteEnvio.text


class Intervencion(object):
    def __init__(self, data):
        self.intervencio = data

    @property
    def tipus_intervencio(self):
        return self.intervencio.TipoIntervencion.text

    @property
    def data(self):
        return self.intervencio.Fecha.text

    @property
    def hora_desde(self):
        return self.intervencio.HoraDesde.text

    @property
    def hora_fins(self):
        return self.intervencio.HoraHasta.text

    @property
    def numero_visita(self):
        ref = None
        try:
            ref = self.intervencio.NumeroVisita.text
        except AttributeError, e:
            pass
        return ref

    @property
    def resultat(self):
        return self.intervencio.Resultado.text

    @property
    def detall_resultat(self):
        ref = None
        try:
            ref = self.intervencio.DetalleResultado.text
        except AttributeError, e:
            pass
        return ref

