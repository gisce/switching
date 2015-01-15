# -*- coding: utf-8 -*-

# pylint: disable=E1002
# pylint: disable=E1101
# pylint: disable=C0111

from libcomxml.core import XmlModel, XmlField

from switching.output.messages.base import Cabecera


# P1-01
class MensajeSolicitudInformacionAlRegistrodePS(XmlModel):                             
    _sort_order = ('missatge', 'capcalera')                       
                                                                                
    def __init__(self):                                                         
        self.doc_root = None                                                    
        self.missatge = XmlField('MensajeSolicitudInformacionAlRegistrodePS',          
                                 attributes={
                                     'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        super(MensajeSolicitudInformacionAlRegistrodePS,
              self).__init__('MensajeSolicitudInformacionAlRegistrodePS',
                             'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
    

# P1-02
class DatosRechazo(XmlModel):
    _sort_order = ('rechazo', 'motivo')

    def __init__(self):
        self.rechazo = XmlField('DatosRechazo')
        self.motivo = XmlField('Motivo')
        super(DatosRechazo, self).__init__('DatosRechazo', 'rechazo')


class RechazoSolicitudInfRegistroPS(XmlModel):
    _sort_order = ('rechazo_solicitud', 'datos_rechazo')

    def __init__(self):
        self.rechazo_solicitud = XmlField('RechazoSolicitudInfRegistroPS')
        self.datos_rechazo = DatosRechazo()
        super(RechazoSolicitudInfRegistroPS,
              self).__init__('RechazoSolicitudInfRegistroPS',
                             'rechazo_solicitud')


class MensajeRechazoSolicitudInfRegistroPS(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'rechazo_solicitud')                       
                                                                                
    def __init__(self):                                                         
        self.doc_root = None                                                    
        self.missatge = XmlField('MensajeRechazoSolicitudInfRegistroPS',
                                 attributes={
                                     'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.rechazo_solicitud = RechazoSolicitudInfRegistroPS()
        super(MensajeRechazoSolicitudInfRegistroPS,
              self).__init__('MensajeRechazoSolicitudInfRegistroPS', 'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()
    

# P1-03
class Consumos(XmlModel):
    _sort_order = ('consums', 'consums_list')

    def __init__(self):
        self.info_ps = XmlField('Consumos')

class EnvioInformacionAlRegistroDePuntosDeSuministroLinia(XmlModel):
    _sort_order = ('info_ps', 'dades_ps', 'consums', 'altres_dades_ps',
                   'equips', 'altres_dades_instala')

    def __init__(self):
        self.info_ps = XmlField(
            'EnvioInformacionAlRegistroDePuntosDeSuministroLinia')
        self.datos_ps = XmlField('DatosPuntoServicio')
        self.consums = XmlField('Consumos')
        self.altres_dades_ps = XmlField('OtrosDatosContrato')
        self.equips = XmlField('Equipos')
        self.altres_dades_instala = XmlField('OtrosDatosInstalacion')
        super(EnvioInformacionAlRegistroDePuntosDeSuministroLinia,
              self).__init__(
            'EnvioInformacionAlRegistroDePuntosDeSuministroLinia',
            'info_ps')

class EnvioInformacionAlRegistroDePuntosDeSuministro(XmlModel):
    _sort_order = ('missatge', 'capcalera', 'linia')

    def __init__(self):
        self.doc_root = None
        self.missatge = XmlField(
            'EnvioInformacionAlRegistroDePuntosDeSuministro',
            attributes={'xmlns': 'http://localhost/elegibilidad'})
        self.capcalera = Cabecera()
        self.linia = EnvioInformacionAlRegistroDePuntosDeSuministroLinia()
        super(EnvioInformacionAlRegistroDePuntosDeSuministro,
              self).__init__('EnvioInformacionAlRegistroDePuntosDeSuministro',
                             'missatge')

    def set_agente(self, agente):
        self.missatge.attributes.update({'AgenteSolicitante': agente})
        self.doc_root = self.root.element()