
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
        return getattr(self.obj, '%s.Contrato' % self.header)
#        return Contracte(self.obj.CambiodeComercializadoraSinCambios.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return Client(self.obj.CambiodeComercializadoraSinCambios.Cliente)

    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        return Acceptacio(self.obj.\
                          AceptacionCambiodeComercializadoraSinCambios.\
                          DatosAceptacion)

    @property
    def rebuig(self):
        """Retorna l'objecte Rebuig"""
        return Rebuig(self.obj.RechazoATRDistribuidoras.Rechazo)


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
        """Retorna el codi de contracte de la comercialitzadora"""
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
            data = self.contracte.FachaActivacionPrevista.text
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
            tarifa = self.acc.TarifaATR.text
        except AttributeError:
            pass
        return tarifa
        
    @property
    def potencies(self):
        pot = []
        for i in self.cond.PotenciasContratadas.Potencia:
            pot.append(int(i.text))
        return pot

class Rebuig(self):
    """Classe Rebuig"""
    
    def __init__(self, data)
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
            motiu = int(self.rebuig.CodigoMotivo.text)
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
    
