
# -*- coding: utf-8 -*-

from message import Message, except_f1


class C1(Message):
    """Classe que implementa C1."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Contracte"""
        return Sollicitud(self.obj.CambiodeComercializadoraSinCambios.\
                          DatosSolicitud)

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        return Contracte(self.obj.CambiodeComercializadoraSinCambios.Contrato)

    @property
    def client(self):
        """Retorna l'objecte Client"""
        return Client(self.obj.CambiodeComercializadoraSinCambios.Cliente)


class Sollicitud(object):
    """Classe que implementa la sol·licitud"""

    def __init__(self, data):
        self.sollicitud = data

    @property
    def linia_negoci(self):
        """Retorna '01' (elèctric) o '02' (gas)"""
        linia = ''
        try:
            linia = self.sollicitud.LiniaNegocioElectrica.text
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
            data = self.contracte.Fechafinalizacion.text
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
