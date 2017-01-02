
# -*- coding: utf-8 -*-
from switching.helpers.funcions import get_rec_attr

from message import Message, except_f1
import C1
from Deadlines import ProcessDeadline, DeadLine, Workdays, Naturaldays


class C2(Message, ProcessDeadline):
    """Classe que implementa C2."""

    steps = [
        DeadLine('01', Workdays(5), '02'),
        DeadLine('02_activation', Workdays(1), '05'),
        DeadLine('02', Naturaldays(60), '05'),
        DeadLine('03', Naturaldays(30), '05'),
        DeadLine('05_activation', Workdays(1), '05'),
        DeadLine('07_activation', Workdays(1), '05'),
        DeadLine('08', Workdays(5), '09')
    ]

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        tree = 'CambiodeComercializadoraConCambios.DatosSolicitud'
        sol = get_rec_attr(self.obj, tree, False)
        if sol:
            return C1.Sollicitud(sol)
        else:
            return False

    @property
    def contracte(self):
        """Retorna l'objecte Contracte"""
        tree = '{0}.Contrato'.format(self.header)
        cont = get_rec_attr(self.obj, tree, False)
        if cont:
            return C1.Contracte(cont)
        else:
            return False

    @property
    def client(self):
        """Retorna l'objecte Client"""
        tree = 'CambiodeComercializadoraConCambios.Cliente'
        cli = get_rec_attr(self.obj, tree, False)
        if cli:
            return C1.Client(cli)
        else:
            return False

    @property
    def acceptacio(self):
        """Retorna l'objecte Acceptacio"""
        obj = getattr(self.obj, self._header, False)
        if obj and hasattr(obj, 'DatosAceptacion'):
            return C1.Acceptacio(obj.DatosAceptacion)
        return False

    @property
    def rebuig(self):
        """Retorna una llista de Rebuig"""
        data = []
        for i in self.obj.RechazoATRDistribuidoras.Rechazo:
            data.append(C1.Rebuig(i))
        return data

    @property
    def rebuig_anullacio(self):
        """Retorna l'objecte Rebuig"""
        data = []
        for i in self.obj.RechazoDeAnulacion.RechazoAnulacion:
            data.append(C1.Rebuig(i))
        return data

    @property
    def header(self):
        return self._header

    @property
    def activacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Activacio(self.obj.\
                            ActivacionCambiodeComercializadoraConCambios)

    @property
    def notificacio(self):
        """Retorna l'objecte Activacio"""
        return C1.Notificacio(self.obj.NotificacionComercializadoraSaliente)
    

    @property
    def anullacio(self):
        """Retorna l'object Anullacio"""
        return C1.Anullacio(self.obj.AnulacionSolicitud)

    @property
    def punts_mesura(self):
        """Retorna una llista de punts de mesura"""
        data = []
        obj = getattr(self.obj, self._header)
        for i in obj.PuntosDeMedida.PuntoDeMedida:
            data.append(C1.PuntMesura(i))
        return data

    @property
    def mesura(self):
        """Retorna l'objecte mesura"""
        obj = getattr(self.obj, self._header)
        return Mesura(obj.Medida)

    @property
    def comentaris(self):
        """Retorna una llista de comentaris"""
        data = []
        obj = getattr(self.obj, self._header)
        if (hasattr(obj, 'Comentarios') and
            hasattr(obj.Comentarios, 'Comentario')):
            for i in obj.Comentarios.Comentario:
                data.append(Comentari(i))
        return data

    @property
    def incidencies(self):
        """Retorna una llista de incidencies"""
        data = []
        for i in self.obj.IncidenciasATRDistribuidoras.Incidencia:
            data.append(C1.Rebuig(i))
        return data

    @property
    def cnae(self):
        value = ''
        try:
            value = self.obj.CambiodeComercializadoraConCambios.CNAE.text
        except AttributeError:
            pass
        return value

    @property
    def vivenda(self):
        value = ''
        try:
            value = (self.obj.CambiodeComercializadoraConCambios.
                                        ViviendaHabitual.text)
        except AttributeError:
            pass
        return value

    @property
    def documents(self):
        """Retorna una llista de documents adjunts"""
        data = []
        obj = getattr(self.obj, self.header)
        if (hasattr(obj, 'RegistrosDocumento') and
                hasattr(obj.RegistrosDocumento, 'RegistroDoc')):
            for d in obj.RegistrosDocumento.RegistroDoc:
                data.append(C1.RegistroDoc(d))
        return data

    @property
    def canvi_titular(self):
        value = ''
        try:
            value = (self.obj.CambiodeComercializadoraConCambios.
                                        TipoCambioTitular.text)
        except AttributeError:
            pass
        return value

    @property
    def documentacio_tecnica(self):
        """Retorna l'objecte documentacio tecnica"""
        obj = getattr(self.obj, self.header)
        if hasattr(obj, 'DocTecnica'):
            return C1.DocumentacioTecnica(obj.DocTecnica)
        else:
            return None


class Comentari(object):

    def __init__(self, data):
        self.comentari = data
    
    @property
    def text(self):
        value = ''
        try:
            value = self.comentari.Texto.text
        except AttributeError:
            pass
        return value

    @property
    def data(self):
        value = ''
        try:
            value = self.comentari.Fecha.text
        except AttributeError:
            pass
        return value

    @property
    def hora(self):
        value = ''
        try:
            value = self.comentari.Hora.text
        except AttributeError:
            pass
        return value

class Mesura(object):

    def __init__(self, data):
        self.mesura = data
    
    @property
    def cp_propietat(self):
        value = ''
        try:
            value = self.mesura.ControlPotenciaPropiedad.text
        except AttributeError:
            pass
        return value

    @property
    def cp_installacio(self):
        value = ''
        try:
            value = self.mesura.ControlPotenciaInstalacion.text
        except AttributeError:
            pass
        return value

    @property
    def equip_aportat_client(self):
        value = ''
        try:
            value = self.mesura.EquipoAportadoCliente.text
        except AttributeError:
            pass
        return value

    @property
    def equip_installat_client(self):
        value = ''
        try:
            value = self.mesura.EquipoInstaladoCliente.text
        except AttributeError:
            pass
        return value

    @property
    def tipus_equip_mesura(self):
        value = ''
        try:
            value = self.mesura.TipoEquipoMedida.text
        except AttributeError:
            pass
        return value
