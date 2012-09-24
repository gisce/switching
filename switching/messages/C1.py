
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
        obj = getattr(self.obj, self._header)
        return Acceptacio(obj.DatosAceptacion)

    @property
    def rebuig(self):
        """Retorna l'objecte Rebuig"""
        return Rebuig(self.obj.RechazoATRDistribuidoras.Rechazo)

    @property
    def rebuig_anullacio(self):
        """Retorna l'objecte Rebuig"""
        return Rebuig(self.obj.RechazoDeAnulacion.RechazoAnulacion)

    @property
    def header(self):
        return self._header

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(PuntMesura(i))
        return data
    
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


class PuntMesura(object):
    """Classe que implementa el punt de mesura
    """
    # Es deixa per més endevant la implementació de la funció
    # obtenir_aparells() que retornaria una llista d'objectes Aparell
    # per a representar la informació del tag opcional <Aparatos>

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
        val = ''
        try:
            val = self.pm.FechaAlta.text
        except AttributeError:
            pass
        return val

    @property
    def baixa(self):
        """Fecha de baja del Punto de Medida"""
        val = ''
        try:
            val = self.pm.FechaBaja.text
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
            pass
        return data
    
    @property
    def hora(self):
        hora = ''
        try:
            hora = self.activacio.DatosActivacion.Hora.text
        except AttributeError:
            pass
        return hora

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
    def potencies(self):
        pot = []
        for i in self.cond.PotenciasContratadas.Potencia:
            pot.append(int(i.text))
        return pot

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
