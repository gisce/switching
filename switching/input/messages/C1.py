
# -*- coding: utf-8 -*-

from message import Message, except_f1


class C1(Message):
    """Classe que implementa C1."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        return Sollicitud(self.obj.CambiodeComercializadoraSinCambios.\
                          DatosSolicitud)

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        obj = getattr(self.obj, self._header)
        return Contracte(obj.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return Client(self.obj.CambiodeComercializadoraSinCambios.Cliente)

    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        obj = getattr(self.obj, self._header, False)
        if obj and hasattr(obj, 'DatosAceptacion'):
            return Acceptacio(obj.DatosAceptacion)
        return False

    @property
    def rebuig(self):
        """Retorna una llista de Rebuig"""
        data = []
        for i in self.obj.RechazoATRDistribuidoras.Rechazo:
            data.append(Rebuig(i))
        return data

    @property
    def rebuig_anullacio(self):
        """Retorna l'objecte Rebuig"""
        data = []
        for i in self.obj.RechazoDeAnulacion.RechazoAnulacion:
            data.append(Rebuig(i))
        return data

    @property
    def header(self):
        return self._header

    @property
    def activacio(self):
        """Retorna l'objecte Activacio"""
        return Activacio(self.obj.\
                         ActivacionCambiodeComercializadoraSinCambios)

    @property
    def notificacio(self):
        """Retorna l'objecte Activacio"""
        return Notificacio(self.obj.NotificacionComercializadoraSaliente)

    @property
    def anullacio(self):
        """Retorna l'object Anullacio"""
        return Anullacio(self.obj.AnulacionSolicitud)

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(PuntMesura(i))
        return data


class PuntMesura(object):
    """Classe que implementa el punt de mesura
    """

    def __init__(self, data):
        self.pm = data

    @property
    def codi(self):
        codi = ''
        try:
            codi = self.pm.CodPM.text.strip()
        except AttributeError:
            pass
        return codi

    @property
    def tipus(self):
        val = ''
        try:
            val = self.pm.TipoPM.text
        except AttributeError:
            pass
        return val

    @property
    def tipus_moviment(self):
        mov = ''
        try:
            mov = self.pm.TipoMovimiento.text
        except AttributeError:
            pass
        return mov

    @property
    def cups(self):
        val = ''
        try:
            val = self.pm.CUPS.text
        except AttributeError:
            pass
        return val

    @property
    def codi_principal(self):
        """Código del punto de medida principal al que está asociado este
           punto de medida"""
        val = ''
        try:
            val = self.pm.CodPMPrincipal.text
        except AttributeError:
            pass
        return val

    @property
    def mode_lectura(self):
        """Indicando si es por Telemedida o TPL."""
        val = ''
        try:
            val = self.pm.ModoLectura.text
        except AttributeError:
            pass
        return val

    @property
    def estat(self):
        """Indicando si es por Telemedida o TPL."""
        val = ''
        try:
            val = self.pm.EstadoPM.text
        except AttributeError:
            pass
        return val

    @property
    def funcio(self):
        val = ''
        try:
            val = self.pm.Funcion.text
        except AttributeError:
            pass
        return val

    @property
    def direccio(self):
        val = ''
        try:
            val = self.pm.DireccionPuntoMedida.text
        except AttributeError:
            pass
        return val

    @property
    def tensio(self):
        """Tensión del punto de medida"""
        val = ''
        try:
            val = self.pm.TensionPM.text
        except AttributeError:
            pass
        return val

    @property
    def data_vigor(self):
        """Fecha de entrada en vigor de la versión del punto de medida"""
        val = ''
        try:
            val = self.pm.FechaVigor.text
        except AttributeError:
            pass
        return val

    @property
    def alta(self):
        """Fecha de alta del Punto de Medida"""
        val = False
        try:
            val = self.pm.FechaAlta.text
        except AttributeError:
            pass
        return val

    @property
    def baixa(self):
        """Fecha de baja del Punto de Medida"""
        val = False
        try:
            val = self.pm.FechaBaja.text
        except AttributeError:
            pass
        return val

    @property
    def codree(self):
        """Código de REE del punto de medida"""
        val = ''
        try:
            val = self.pm.CodREE.text
        except AttributeError:
            pass
        return val

    @property
    def direccion_enlace(self):
        """Direccion de enlace para comunicacion con el registrador"""
        val = ''
        try:
            val = self.pm.DireccionEnlace.text
        except AttributeError:
            pass
        return val

    @property
    def numlinea(self):
        """Numero de linea para comunicacion con el registrador"""
        val = ''
        try:
            val = self.pm.NumLinea.text
        except AttributeError:
            pass
        return val

    @property
    def telefono_telemedida(self):
        """Teléfono para telemedida"""
        val = ''
        try:
            val = self.pm.TelefonoTelemedida.text
        except AttributeError:
            pass
        return val

    @property
    def estado_telefono(self):
        """Estado del teléfono"""
        val = ''
        try:
            val = self.pm.EstadoTelefono.text
        except AttributeError:
            pass
        return val

    @property
    def clave_acceso(self):
        """Clave de acceso al punto de medida"""
        val = ''
        try:
            val = self.pm.ClaveAcceso.text
        except AttributeError:
            pass
        return val

    @property
    def password(self):
        val = ''
        try:
            val = self.pm.PasswordPM.text
        except AttributeError:
            pass
        return val

    @property
    def aparatos(self):
        """Retorna una llista d'aparells"""
        data = []
        for i in self.pm.Aparatos.Aparato:
            data.append(Aparato(i))
        return data

    @property
    def comentarios(self):
        """Retorna una llista de comentaris"""
        data = []
        if hasattr(self.pm, 'ComentariosPM'):
            for i in self.pm.ComentariosPM.ComentarioPM:
                data.append(i.ComentarioPM.Texto.text)
        return data


class Aparato(object):
    '''Classe que implementa els aparells de mesura'''

    def __init__(self, data):
        self.aparato = data

    @property
    def modelo(self):
        return ModeloAparato(self.aparato.Modelo)

    @property
    def tipo_movimiento(self):
        val = ''
        try:
            val = self.aparato.TipoMovimiento.text
        except AttributeError:
            pass
        return val

    @property
    def tipo_equipo(self):
        val = ''
        try:
            val = self.aparato.TipoEquipoMedida.text
        except AttributeError:
            pass
        return val

    @property
    def tipo_propiedad(self):
        val = ''
        try:
            val = self.aparato.TipoPropiedadAparato.text
        except AttributeError:
            pass
        return val

    @property
    def propietario(self):
        val = ''
        try:
            val = self.aparato.Propietario.text
        except AttributeError:
            pass
        return val

    @property
    def extraccion_lecturas(self):
        val = ''
        try:
            val = self.aparato.ExtraccionLecturas.text
        except AttributeError:
            pass
        return val

    @property
    def dh_activa(self):
        val = ''
        try:
            val = self.aparato.DiscriminacionHorariaActiva.text
        except AttributeError:
            pass
        return val

    @property
    def lectura_directa(self):
        val = ''
        try:
            val = self.aparato.LecturaDirecta.text
        except AttributeError:
            pass
        return val

    @property
    def cod_precinto(self):
        val = ''
        try:
            val = self.aparato.CodPrecinto.text
        except AttributeError:
            pass
        return val

    @property
    def icp(self):
        if hasattr(self.aparato, 'DatosAparatoICP'):
            return True
        else:
            return False

    @property
    def datos_aparato(self):
        if hasattr(self.aparato, 'DatosAparatoICP'):
            return DatosAparato(self.aparato.DatosAparatoICP)
        else:
            return DatosAparato(self.aparato.DatosAparatoNoICP)

    @property
    def medidas(self):
        """Retorna una llista de mesures"""
        data = []
        if hasattr(self.aparato, 'Medidas'):
            for i in self.aparato.Medidas.Medida:
                data.append(Medida(i))
        return data


class ModeloAparato(object):
    '''Classe que implementa els models dels aparells'''

    def __init__(self, data):
        self.datosmodelo = data

    @property
    def tipo(self):
        val = ''
        try:
            val = self.datosmodelo.Tipo.text
        except AttributeError:
            pass
        return val

    @property
    def marca(self):
        val = ''
        try:
            val = self.datosmodelo.Marca.text
        except AttributeError:
            pass
        return val

    @property
    def modelo(self):
        val = ''
        try:
            val = self.datosmodelo.ModeloMarca.text
        except AttributeError:
            pass
        return val


class DatosAparato(object):

    def __init__(self, data):
        self.datos = data

    @property
    def periodo_fabricacion(self):
        val = ''
        try:
            val = self.datos.PeriodoFabricacion.text
        except AttributeError:
            pass
        return val

    @property
    def numero_serie(self):
        val = ''
        try:
            val = self.datos.NumeroSerie.text
        except AttributeError:
            pass
        return val

    @property
    def funcion(self):
        val = ''
        try:
            val = self.datos.FuncionAparato.text
        except AttributeError:
            pass
        return val

    @property
    def integradores(self):
        val = ''
        try:
            val = self.datos.NumIntegradores.text
        except AttributeError:
            pass
        return val

    @property
    def constante_energia(self):
        val = ''
        try:
            val = self.datos.ConstanteEnergia.text
        except AttributeError:
            pass
        return val

    @property
    def constante_maximetro(self):
        val = ''
        try:
            val = self.datos.ConstanteMaximetro.text
        except AttributeError:
            pass
        return val

    @property
    def ruedas_enteras(self):
        val = ''
        try:
            val = self.datos.RuedasEnteras.text
        except AttributeError:
            pass
        return val

    @property
    def ruedas_decimales(self):
        val = ''
        try:
            val = self.datos.RuedasDecimales.text
        except AttributeError:
            pass
        return val


class Medida(object):

    def __init__(self, data):
        self.medida = data

    @property
    def tipo_dh(self):
        val = ''
        try:
            val = self.medida.TipoDH.text
        except AttributeError:
            pass
        return val

    @property
    def periodo(self):
        val = ''
        try:
            val = self.medida.Periodo.text
        except AttributeError:
            pass
        return val

    @property
    def magnitud(self):
        val = ''
        try:
            val = self.medida.MagnitudMedida.text
        except AttributeError:
            pass
        return val

    @property
    def procedencia(self):
        val = ''
        try:
            val = self.medida.Procedencia.text
        except AttributeError:
            pass
        return val

    @property
    def lectura_anterior(self):
        val = ''
        try:
            val = self.medida.LecturaAnterior.text
        except AttributeError:
            pass
        return val

    @property
    def anomalia(self):
        val = ''
        try:
            val = self.medida.Anomalia.text
        except AttributeError:
            pass
        return val

    @property
    def texto_anomalia(self):
        val = ''
        try:
            val = self.medida.TextoAnomalia.text
        except AttributeError:
            pass
        return val


class Notificacio(object):
    """Classe que implementa la notificació"""

    def __init__(self, data):
        self.notificacio = data

    @property
    def data(self):
        data = ''
        try:
            data = self.notificacio.DatosNotificacion.FechaActivacion.text
        except AttributeError:
            pass
        return data

    @property
    def contracte(self):
        contracte = ''
        try:
            contracte = Contracte(self.notificacio.Contrato)
        except AttributeError:
            pass
        return contracte


class Activacio(object):
    """Classe que implementa l'activació"""

    def __init__(self, data):
        self.activacio = data

    @property
    def data(self):
        data = ''
        try:
            data = self.activacio.DatosActivacion.Fecha.text
        except AttributeError:
            try:
                data = self.activacio.DatosActivacionYBaja.Fecha.text
            except AttributeError:
                pass
        return data

    @property
    def hora(self):
        hora = ''
        try:
            hora = self.activacio.DatosActivacion.Hora.text
        except AttributeError:
            try:
                hora = self.activacio.DatosActivacionYBaja.Hora.text
            except AttributeError:
                pass
        return hora

    @property
    def tipus(self):
        tipus = ''
        try:
            tipus = self.activacio.DatosActivacion.TipoActivacion.text
        except AttributeError:
            pass
        return tipus

    @property
    def contracte(self):
        contracte = ''
        try:
            contracte = Contracte(self.activacio.Contrato)
        except AttributeError:
            pass
        return contracte


class Sollicitud(object):
    """Classe que implementa la sol·licitud"""

    def __init__(self, data):
        self.sollicitud = data

    @property
    def linia_negoci(self):
        """Retorna '01' (elèctric) o '02' (gas)"""
        linia = ''
        try:
            linia = self.sollicitud.LineaNegocioElectrica.text
        except AttributeError:
            pass
        return linia

    @property
    def sollicitudadm(self):
        """Sol·licitud administrativa contractual"""
        sol = ''
        try:
            sol = self.sollicitud.SolicitudAdmContractual.text
        except AttributeError:
            pass
        return sol

    @property
    def cicle_activacio(self):
        """Indicatiu d'activació amb el cicle de lectura"""
        cicle = ''
        try:
            cicle = self.sollicitud.IndActivacionLectura.text
        except AttributeError:
            pass
        return cicle

    @property
    def data_prevista_accio(self):
        """Retorna la data prevista del canvi o alta"""
        data = ''
        try:
            data = self.sollicitud.FechaPrevistaAccion.text
        except AttributeError:
            pass
        return data

    @property
    def representant(self):
        """Indicatiu del representat"""
        rep = ''
        try:
            rep = self.sollicitud.IndSustitutoMandatario.text
        except AttributeError:
            pass
        return rep

    @property
    def canvi_titular(self):
        value = ''
        try:
            value = (self.sollicitud.TipoCambioTitular.text)
        except AttributeError:
            pass
        return value

    @property
    def periodicitat_facturacio(self):
        value = ''
        try:
            value = (self.sollicitud.PeriodicidadFacturacion.text)
        except AttributeError:
            pass
        return value

    @property
    def cnae(self):
        value = ''
        try:
            value = (self.sollicitud.CNAE.text)
        except AttributeError:
            pass
        return value
    
    @property
    def motiu(self):
        value = ''
        try:
            value = (self.sollicitud.Motivo.text)
        except AttributeError:
            pass
        return value


class Contracte(object):
    """Classe Contracte"""

    def __init__(self, data):
        self.contracte = data

    @property
    def codi_contracte(self):
        """Retorna el codi de contracte"""
        codi = ''
        try:
            codi = self.contracte.IdContrato.CodContrato.text
        except AttributeError:
            try:
                codi = self.contracte.CodContrato.text
            except AttributeError:
                pass
        return codi

    @property
    def durada(self):
        """Retorna la durada del contracte en mesos en el cas que la
           durada del contracte sigui superior a 12 mesos"""
        mesos = ''
        try:
            mesos = int(self.contracte.Duracion.text)
        except AttributeError:
            pass
        return mesos

    @property
    def data_finalitzacio(self):
        """Retorna la data de finalització en el cas que la durada del
           contracte sigui inferior a 12 mesos"""
        data = ''
        try:
            data = self.contracte.FechaFinalizacion.text
        except AttributeError:
            pass
        return data

    @property
    def tipus_contracte(self):
        """Retorna el tipus de contracte"""
        tipus = ''
        try:
            tipus = self.contracte.TipoContratoATR.text
        except AttributeError:
            try:
                tipus = self.contracte.TipoContrato.text
            except AttributeError:
                pass
        return tipus

    @property
    def direccio_correspondencia(self):
        """Retorna F/S/O"""
        adreca = ''
        try:
            adreca = self.contracte.DireccionCorrespondencia.Indicador.text
        except AttributeError:
            pass
        return adreca

    @property
    def direccio(self):
        direccio = False
        try:
            direccio = Direccio(self.contracte.DireccionCorrespondencia.\
                                Direccion)
        except AttributeError:
            pass
        return direccio

    @property
    def condicions(self):
        """Retorna l'objecte Condicions"""
        return Condicions(self.contracte.CondicionesContractuales)

    @property
    def consum_anual(self):
        """Retorna el consum anual estimat"""
        consum = ''
        try:
            consum = int(self.contracte.ConsumoAnualEstimado.text)
        except AttributeError:
            pass
        return consum

    @property
    def tipus_activacio(self):
        """Retorna el tipus d'activacio"""
        tipus = ''
        try:
            tipus = self.contracte.TipoActivacionPrevista.text
        except AttributeError:
            pass
        return tipus

    @property
    def data_activacio(self):
        """Retorna la data d'activació prevista"""
        data = ''
        try:
            data = self.contracte.FechaActivacionPrevista.text
        except AttributeError:
            pass
        return data


class Client(object):
    """Classe Client"""

    def __init__(self, data):
        self.client = data

    @property
    def tipus_identificacio(self):
        return self.client.IdCliente.TipoCIFNIF.text

    @property
    def codi_identificacio(self):
        return self.client.IdCliente.Identificador.text

    @property
    def nom(self):
        nom = ''
        try:
            nom = self.client.Nombre.NombreDePila.text
        except AttributeError:
            try:
                nom = self.client.Nombre.RazonSocial.text
            except AttributeError:
                pass
        return nom

    @property
    def cognom_1(self):
        nom = ''
        try:
            nom = self.client.Nombre.PrimerApellido.text
        except AttributeError:
            pass
        return nom

    @property
    def cognom_2(self):
        nom = ''
        try:
            nom = self.client.Nombre.SegundoApellido.text
        except AttributeError:
            pass
        return nom

    @property
    def fax(self):
        try:
            return '+%s%s' % (str(self.client.Fax.PrefijoPais),
                              str(self.client.Fax.Numero))
        except AttributeError:
            pass

    @property
    def telf_num(self):
        num = ''
        try:
            num = self.client.Telefono.Numero.text
        except AttributeError:
            pass
        return num

    @property
    def telf_prefix(self):
        prefix = ''
        try:
            prefix = self.client.Telefono.PrefijoPais.text
        except AttributeError:
            pass
        return prefix

    @property
    def indicador(self):
        '''Indicador tipus adreça'''
        indicador = ''
        try:
            indicador = self.client.IndicadorTipoDireccion.text
        except AttributeError:
            pass
        return indicador

    @property
    def direccio(self):
        if hasattr(self.client, 'Direccion'):
            return Direccio(self.client.Direccion)
        return False

    @property
    def titular_pagador(self):
        '''Indicador titular = pagador'''
        value = ''
        try:
            value = self.client.TitularContratoVsTitularPago.text
        except AttributeError:
            pass
        return value


class Acceptacio(object):
    """Classe Acceptacio"""

    def __init__(self, data):
        self.acc = data

    @property
    def data_acceptacio(self):
        data = ''
        try:
            data = self.acc.FechaAceptacion.text
        except AttributeError:
            pass
        return data

    @property
    def potencia(self):
        pot = ''
        try:
            pot = int(self.acc.PotenciaActual.text)
        except AttributeError:
            pass
        return pot

    @property
    def actuacio_camp(self):
        act = ''
        try:
            act = self.acc.ActuacionCampo.text
        except AttributeError:
            pass
        return act

    @property
    def data_ult_lect(self):
        data = ''
        try:
            data = self.acc.FechaUltimaLectura.text
        except AttributeError:
            pass
        return data


class Condicions(object):
    """Classe Condicions"""

    def __init__(self, data):
        self.cond = data

    @property
    def tarifa(self):
        tarifa = ''
        try:
            tarifa = self.cond.TarifaATR.text
        except AttributeError:
            pass
        return tarifa

    @property
    def periodicitat_facturacio(self):
        periodicitat = ''
        try:
            periodicitat = self.cond.PeriodicidadFacturacion.text
        except AttributeError:
            pass
        return periodicitat

    @property
    def tipus_telegestio(self):
        tipus_telegestio = ''
        try:
            tipus_telegestio = self.cond.TipodeTelegestion.text
        except AttributeError:
            pass
        return tipus_telegestio

    @property
    def potencies(self):
        pot = []
        for i in self.cond.PotenciasContratadas.Potencia:
            pot.append((int(i.get('Periodo')), int(i.text)))
        return sorted(pot)

    @property
    def control_potencia(self):
        control_potencia = ''
        try:
            control_potencia = self.cond.ModoControlPotencia.text
        except AttributeError:
            pass
        return control_potencia


class Rebuig(object):
    """Classe Rebuig"""

    def __init__(self, data):
        self.rebuig = data

    @property
    def sequencial(self):
        seq = ''
        try:
            seq = int(self.rebuig.Secuencial.text)
        except AttributeError:
            pass
        return seq

    @property
    def motiu(self):
        motiu = ''
        try:
            motiu = str(int(self.rebuig.CodigoMotivo.text))
        except AttributeError:
            pass
        return motiu

    @property
    def descripcio(self):
        motiu = ''
        try:
            motiu = self.rebuig.Texto.text
        except AttributeError:
            pass
        return motiu

    @property
    def data(self):
        data = ''
        try:
            data = self.rebuig.Fecha.text
        except AttributeError:
            pass
        return data

    @property
    def hora(self):
        hora = ''
        try:
            hora = self.rebuig.Hora.text
        except AttributeError:
            pass
        return hora

    @property
    def contracte(self):
        contracte = ''
        try:
            contracte = self.rebuig.IdContrato.CodContrato.text
        except AttributeError:
            pass
        return contracte


class Anullacio(object):
    """Classe Anul·lació"""

    def __init__(self, data):
        self.obj = data

    @property
    def sollicitud(self):
        val = ''
        try:
            val = Sollicitud(self.obj.DatosSolicitud)
        except AttributeError:
            pass
        return val

    @property
    def client(self):
        val = ''
        try:
            val = Client(self.obj.Cliente)
        except AttributeError:
            pass
        return val

    @property
    def contracte(self):
        vals = ''
        try:
            val = self.obj.IdContrato.CodContrato.text
        except AttributeError:
            pass
        return val


class Direccio(object):
    """Classe que implementa la direccio"""

    def __init__(self, data):
        self.direccio = data

    @property
    def pais(self):
        pais = ''
        try:
            pais = self.direccio.Pais.text
        except AttributeError:
            pass
        return pais

    @property
    def provincia(self):
        provincia = ''
        try:
            provincia = self.direccio.Provincia.text
        except AttributeError:
            pass
        return provincia

    @property
    def municipi(self):
        municipi = ''
        try:
            municipi = self.direccio.Municipio.text
        except AttributeError:
            pass
        return municipi

    @property
    def poblacio(self):
        poblacio = ''
        try:
            poblacio = self.direccio.Poblacion.text
        except AttributeError:
            pass
        return poblacio

    @property
    def tv(self):
        tv = ''
        try:
            tv = self.direccio.TipoVia.text
        except AttributeError:
            pass
        return tv

    @property
    def cp(self):
        cp = ''
        try:
            cp = self.direccio.CodPostal.text
        except AttributeError:
            pass
        return cp

    @property
    def carrer(self):
        carrer = ''
        try:
            carrer = self.direccio.Calle.text
        except AttributeError:
            pass
        return carrer

    @property
    def num(self):
        '''Numero de finca'''
        num = ''
        try:
            num = self.direccio.NumeroFinca.text
        except AttributeError:
            pass
        return num

    @property
    def dup(self):
        '''Duplicador de finca'''
        dup = ''
        try:
            dup = self.direccio.DuplicadorFinca.text
        except AttributeError:
            pass
        return dup

    @property
    def escala(self):
        escala = ''
        try:
            escala = self.direccio.Escalera.text
        except AttributeError:
            pass
        return escala

    @property
    def pis(self):
        pis = ''
        try:
            pis = self.direccio.Piso.text
        except AttributeError:
            pass
        return pis

    @property
    def porta(self):
        porta = ''
        try:
            porta = self.direccio.Puerta.text
        except AttributeError:
            pass
        return porta

    @property
    def tipus_aclarador(self):
        tipus = ''
        try:
            tipus = self.direccio.TipoAclarador.text
        except AttributeError:
            pass
        return tipus

    @property
    def aclarador(self):
        aclarador = ''
        try:
            aclarador = self.direccio.Aclarador.text
        except AttributeError:
            pass
        return aclarador
