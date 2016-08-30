
# -*- coding: utf-8 -*-
from switching.helpers.funcions import get_rec_attr

from message import Message, except_f1
import C1, C2


class M1(Message):
    """Classe que implementa M1."""

    @property
    def sollicitud(self):
        """Retorna l'objecte Sollicitud"""
        tree = 'ModificacionDeATR.DatosSolicitud'
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
        tree = 'ModificacionDeATR.Cliente'
        cli = get_rec_attr(self.obj, tree, False)
        if cli:
            return C1.Client(cli)
        else:
            return False

    @property
    def client_sortint(self):
        """Retorna l'objecte Client sortint"""
        return C1.Client(self.obj.ModificacionDeATR.ClienteSaliente)

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
                            ActivacionModificacionDeATR)

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
        return C2.Mesura(obj.Medida)

    @property
    def comentaris(self):
        """Retorna una llista de comentaris"""
        data = []
        obj = getattr(self.obj, self._header)
        if (hasattr(obj, 'Comentarios') and
            hasattr(obj.Comentarios, 'Comentario')):
            for i in obj.Comentarios.Comentario:
                data.append(C2.Comentari(i))
        return data

    @property
    def incidencies(self):
        """Retorna una llista de incidencies"""
        data = []
        for i in self.obj.IncidenciasATRDistribuidoras.Incidencia:
            data.append(C1.Rebuig(i))
        return data

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
    def documentacio_tecnica(self):
        """Retorna l'objecte documentacio tecnica"""
        obj = getattr(self.obj, self.header)
        if hasattr(obj, 'DocTecnica'):
            return C1.DocumentacioTecnica(obj.DocTecnica)
        else:
            return None
