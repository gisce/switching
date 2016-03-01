# -*- coding: utf-8 -*-

from message import Message
import C1
import W1


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
        return DatosPasoSollicitud(self.obj.SolicitudReclamacion.DatosSolicitud)

    @property
    def reclamacions(self):
        """Retorna una llista de Reclamacions"""
        data = []
        try:
            varis = self.obj.SolicitudReclamacion.VariablesDetalleReclamacion
            for var in varis:
                if len(var.VariableDetalleReclamacion.getchildren()):
                    data.append(
                        VariableDetalleReclamacion(
                            var.VariableDetalleReclamacion
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
        return self.obj.SolicitudReclamacion.TipoReclamante.text

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
        if len(getattr(obj, 'RegistrosDocumento', [])):
            doc_registry = C1.RegistrosDocumento(obj.RegistrosDocumento)
            return doc_registry.get_documents()
        else:
            return None

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

    # @property
    # def activacio(self):
    #     """Retorna l'objecte Activacio"""
    #     return C1.Activacio(self.obj.NotificacionBajaEnergia)
    #
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
    # @property
    # def contracte(self):
    #     """Retorna l'objecte Contracte"""
    #     obj = getattr(self.obj, self._header)
    #     try:
    #         idcontrato = C1.Contracte(obj.IdContrato)
    #     except AttributeError:
    #         # Step 04 Acceptacio has the classic structure
    #         idcontrato = C1.Contracte(obj.Contrato)
    #     return idcontrato
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
            ref = self.sollicitud.RefernciaOrigen.text
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
            return self.variable.NumExpedienteAcomentida.text
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
        for i in self.variable.LecturasAportadas.LecturaAportada:
            data.append(W1.LecturaAportada(i))
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
