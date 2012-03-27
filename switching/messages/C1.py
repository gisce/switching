
# -*- coding: utf-8 -*-

from message import Message, except_f1


class C1(Message):
    """Classe que implementa C1."""
     
    @property
    def linia_negoci(self):
        """Retorna '01' (elèctric) o '02' (gas)"""
        linia = ''
        try:
            linia = self.obj.CambiodeComercializadoraSinCambios.\
                    DatosSolicitud.LiniaNegocioElectrica.text
        except AttributeError:
            pass
        return linia

    @property
    def activacio_cicle_lectura(self):
        """Indicatiu d'activació amb el cicle de lectura"""
        cicle = ''
        try:
            cicle = self.obj.CambiodeComercializadoraSinCambios.\
                    DatosSolicitud.IndActivacionLectura.text
        except AttributeError:
            pass
        return cicle

    @property
    def data_prevista_accio(self):
        """Retorna la data prevista del canvi o alta"""
        data = ''
        try:
            data = self.obj.CambiodeComercializadoraSinCambios.\
                   DatosSolicitud.FechaPrevistaAccion.text
        except AttributeError:
            pass
        return data

    @property
    def codi_contracte(self):
        """Retorna el codi de contracte de la comercialitzadora"""
        codi = ''
        try:
            codi = self.obj.CambiodeComercializadoraSinCambios.\
                   Contrato.IdContrato.CodContrato.text
        except AttributeError:
            pass
        return codi

    @property
    def durada(self):
        """Retorna la durada del contracte en mesos en el cas que la 
           durada del contracte sigui superior a 12 mesos"""
        mesos = ''
        try:
            mesos = int(self.obj.CambiodeComercializadoraSinCambios.\
                    Contrato.Duracion.text)
        except AttributeError:
            pass
        return mesos

    @property
    def data_finalitzacio(self):
        """Retorna la data de finalització en el cas que la durada del 
           contracte sigui inferior a 12 mesos"""
        data = ''
        try:
            data = self.obj.CambiodeComercializadoraSinCambios.\
                   Contrato.Fechafinalizacion.text
        except AttributeError:
            pass
        return data

    @property
    def tipus_contracte(self):
        """Retorna el tipus de contracte"""
        tipus = ''
        try:
            tipus = self.obj.CambiodeComercializadoraSinCambios.\
                    Contrato.TipoContratoATR.text
        except AttributeError:
            pass
        return tipus

    @property
    def direccio_correspondencia(self):
        """Retorna F/S/O"""
        adreca = ''
        try:
            adreca = self.obj.CambiodeComercializadoraSinCambios.\
                     Contrato.DireccionCorrespondencia.Indicador
        except AttributeError:
            pass
        return adreca
    
    @property
    def client(self):
        """Retorna l'objecte Client"""
        return Client(self.obj.CambiodeComercializadoraSinCambios.Cliente)

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
    def fax(self):
        try:
            return '+%s%s' % (str(self.client.Fax.PrefijoPais), 
                              str(self.client.Fax.Numero)
        except AttributeError:
            pass
