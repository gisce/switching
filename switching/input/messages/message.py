
# -*- coding: utf-8 -*-

import gettext
from lxml import objectify, etree

import switching
from switching.types import DecimalElement, check_decimal_element

XSD_DATA = {'F1': {'01': 'Facturacion.xsd'},
            'Q1': {'01': 'SaldoLecturasFacturacion.xsd'},
            'A3': {'01': 'PasoMRAMLConCambiosRestoTarifas.xsd',
                   '02': ('AceptacionPasoMRAMLConCambiosRestoTarifa.xsd',
                          'RechazoATRDistribuidoras.xsd'),
                   '03': 'IncidenciasATRDistribuidoras.xsd',
                   '04': 'RechazoATRDistribuidoras.xsd',
                   '05': 'ActivacionPasoMRAMLConCambiosRestoTarifas.xsd',
                   '06': 'AnulacionSolicitud.xsd',
                   '07': ('AceptacionAnulacion.xsd',
                          'RechazoAnulacion.xsd')},
            'B1': {'01': 'BajaEnergia.xsd',
                   '02': ('AceptacionBajaEnergia.xsd',
                          'RechazoATRDistribuidoras.xsd'),
                   '03': 'AnulacionSolicitud.xsd',
                   '04': ('AceptacionAnulacion.xsd',
                          'RechazoAnulacion.xsd'),
                   '05': 'NotificacionBajaEnergia.xsd'},
            'C1': {'01': 'CambiodeComercializadoraSinCambios.xsd',
                   '02': ('AceptacionCambiodeComercializadoraSinCambios.xsd',
                          'RechazoATRDistribuidoras.xsd'),
                   '05': 'ActivacionCambiodeComercializadoraSinCambios.xsd',
                   '06': 'NotificacionComercializadoraSaliente.xsd',
                   '08': 'AnulacionSolicitud.xsd',
                   '09': ('AceptacionAnulacion.xsd',
                          'RechazoAnulacion.xsd'),
                   '10': 'NotificacionComercializadoraSaliente.xsd',
                   '11': 'AceptacionCambiodeComercializadoraSinCambios.xsd'},
            'C2': {'01': 'CambiodeComercializadoraConCambios.xsd',
                   '02': ('AceptacionCambiodeComercializadoraConCambios.xsd',
                          'RechazoATRDistribuidoras.xsd'),
                   '03': 'IncidenciasATRDistribuidoras.xsd',
                   '04': 'RechazoATRDistribuidoras.xsd',
                   '05': 'ActivacionCambiodeComercializadoraConCambios.xsd',
                   '06': 'NotificacionComercializadoraSaliente.xsd',
                   '07': 'ActivacionCambiodeComercializadoraConCambios.xsd',
                   '08': 'AnulacionSolicitud.xsd',
                   '09': ('AceptacionAnulacion.xsd',
                          'RechazoAnulacion.xsd'),
                   '10': 'NotificacionComercializadoraSaliente.xsd',
                   '11': 'AceptacionCambiodeComercializadoraConCambios.xsd',
                   '12': 'AceptacionCambiodeComercializadoraConCambios.xsd',
                   },
            'D1': {'01': 'NotificacionCambiosATRDesdeDistribuidor.xsd'
                   },
            'M1': {'01': 'ModificacionDeATR.xsd',
                   '02': ('AceptacionModificacionDeATR.xsd',
                          'RechazoATRDistribuidoras.xsd'),
                   '03': 'IncidenciasATRDistribuidoras.xsd',
                   '04': 'RechazoATRDistribuidoras.xsd',
                   '05': 'ActivacionModificacionDeATR.xsd',
                   '06': 'AnulacionSolicitud.xsd',
                   '07': ('AceptacionAnulacion.xsd',
                          'RechazoAnulacion.xsd'),
                   },
            'R1': {'01': 'ReclamacionPeticion.xsd',
                   '02': ('AceptacionReclamacion.xsd',
                          'RechazoReclamacion.xsd'),
                   '03': 'PeticionInformacionAdicionalReclamacion.xsd',
                   '04': 'EnvioInformacionReclamacion.xsd',
                   '05': 'CierreReclamacion.xsd',
                   },
            'W1': {'01': 'MensajeAportacionLectura.xsd',
                   '02': ('AceptacionAportacionLectura.xsd',
                          'RechazoAportacionLectura.xsd'),
                   },
            }

_ = gettext.gettext

# register the decimal type with objectify
decimal_type = objectify.PyType('decimal', check_decimal_element,
                                DecimalElement)
decimal_type.register(before='float')


class MessageBase(object):
    """Classe base"""
    def __init__(self, xml, force_tipus=None):
        """Construeix un missatge base."""
        self.obj = None
        self.error = None
        if isinstance(xml, file):
            self.check_fpos(xml)
            xml = xml.read()
        self.xml_orig = xml
        # Fem desaparèixer el header amb l'encoding de l'xml
        # <?xml version="1.0" encoding="ISO-8859-1"?>
        try:
            root = etree.fromstring(xml)
        except etree.XMLSyntaxError:
            raise except_f1('Error', 'Fitxer XML erroni')
        uxml = etree.tostring(root).decode('iso-8859-1')
        self.str_xml = uxml
        self.tipus = ''
        self._header = ''
        self.pas = ''
        self.f_xsd = ''
        self.set_tipus()
        if force_tipus and self.tipus != force_tipus:
            msg = 'L\'XML no es correspon al tipus %s' % force_tipus
            raise except_f1('Error', _(msg))
        self.set_xsd()

    @property
    def valid(self):
        if self.obj is None:
            return None
        else:
            return not bool(self.error)

    def set_tipus(self):
        """Set type of message. To implement in child classes"""
        raise NotImplementedError('This method is not implemented!')

    def set_xsd(self):
        """Set xsd. To implement in child classes"""
        raise NotImplementedError('This method is not implemented!')

    def check_fpos(self, f_obj):
        """Setejar la posició actual dels fixers"""
        if (isinstance(f_obj, file) and f_obj.tell() != 0):
            f_obj.seek(0)

    def get_tipus_xml(self):
        """Obtenir el tipus de missatge"""
        return self.tipus

    def get_xml(self):
        """Obtenir el fitxer"""
        return self.xml_orig

    def parse_xml(self):
        """Import xml content. To implement in child classes"""
        raise NotImplementedError('This method is not implemented!')


class Message(MessageBase):
    """Classe base intercanvi informacio comer-distri"""

    @property
    def get_cabecera_model(self):
        """ Gets header model """
        try:
            obj = objectify.fromstring(self.str_xml)
            return obj.Cabecera
        except Exception, e:
            return obj.CabeceraReclamacion

    def set_tipus(self):
        """Setejar el tipus de missatge"""
        head = self.get_cabecera_model
        try:
            obj = objectify.fromstring(self.str_xml)
            self.tipus = head.CodigoDelProceso.text
            self.pas = head.CodigoDePaso.text
        except:
            msg = _('No s\'ha pogut identificar el codi de proces o '\
                    'codi de pas')
            raise except_f1('Error', msg)

    def set_xsd(self):
        """Setejar el fitxer xsd"""
        if self.tipus not in XSD_DATA:
            msg = _('Codi de proces \'%s\' no suportat') % self.tipus
            raise except_f1('Error', msg)
        if self.pas not in XSD_DATA[self.tipus]:
            msg = _('Codi de pas \'%s\'  no suportat') % self.pas
            raise except_f1('Error', msg)
        try:
            if isinstance(XSD_DATA[self.tipus][self.pas], tuple):
                trobat = False
                root = objectify.fromstring(self.str_xml)
                for fitxer in XSD_DATA[self.tipus][self.pas]:
                    if fitxer.split(".xsd")[0] in root.tag:
                        trobat = True
                        break
                if not trobat:
                    msg = (_('Tipus de fitxer \'%s\' no suportat') % root.tag)
                    raise except_f1('Error', msg)
            else:
                fitxer = XSD_DATA[self.tipus][self.pas]
            self._header = fitxer.split(".xsd")[0]
            xsd = switching.get_data(fitxer)
            self.f_xsd = open(xsd, 'r')
        except except_f1, e:
            raise e
        except:
            msg = (_('Fitxer \'%s\' corrupte') %
                     switching.get_data(XSD_DATA[self.tipus]))
            raise except_f1('Error', msg)

    def get_pas_xml(self):
        """Obtenir el pas del missatge"""
        return self.pas

    def parse_xml(self, validate=True):
        """Importar el contingut de l'xml"""
        self.check_fpos(self.f_xsd)
        schema = etree.XMLSchema(file=self.f_xsd)
        parser = objectify.makeparser(schema=schema)
        try:
            self.obj = objectify.fromstring(self.str_xml, parser)
        except Exception as e:
            self.error = e.message
            if validate:
                raise except_f1('Error', _(u'Document invàlid: {0}').format(e))
            else:
                parser = objectify.makeparser(schema=None)
                self.obj = objectify.fromstring(self.str_xml, parser)

    # Funcions relacionades amb la capçalera del XML
    @property
    def get_codi_emisor(self):
        head = self.get_cabecera_model
        ref = head.CodigoREEEmpresaEmisora.text
        if not ref:
            raise except_f1('Error', _('Document sense emisor'))
        return ref

    @property
    def get_codi_destinatari(self):
        head = self.get_cabecera_model
        ref = head.CodigoREEEmpresaDestino.text
        if not ref:
            raise except_f1('Error', _('Document sense destinatari'))
        return ref

    @property
    def get_codi(self):
        try:
            ref = self.obj.Cabecera.Codigo.text.strip()
        except Exception, e:
            ref = self.obj.CabeceraReclamacion.CUPS.text.strip()
        if not ref:
            raise except_f1('Error', _('Document sense codi'))
        return ref

    @property
    def cups(self):
        return self.get_codi

    @property
    def codi_sollicitud(self):
        head = self.get_cabecera_model
        ref = head.CodigoDeSolicitud.text
        if not ref:
            raise except_f1('Error', _('Document sense codi de'\
                                       ' sol·licitud'))
        return ref

    @property
    def seq_sollicitud(self):
        head = self.get_cabecera_model
        ref = head.SecuencialDeSolicitud.text
        if not ref:
            raise except_f1('Error', _('Document sense codi de'\
                                       ' seqüencial de sol·licitud'))
        return ref

    @property
    def data_sollicitud(self):
        head = self.get_cabecera_model
        ref = head.FechaSolicitud.text
        if not ref:
            raise except_f1('Error', _('Document sense data de'\
                                       ' sol·licitud'))
        return ' '.join(ref.split('T'))

    @property
    def versio(self):
        head = self.get_cabecera_model
        try:
            ref = head.Version.text
        except:
            raise except_f1('Error', _('Document sense versio'))
        if not ref:
            raise except_f1('Error', _('Document sense versio'))
        return ref


class MessageTG(MessageBase):
    """Classe base missatges telegestio"""

    def set_tipus(self):
        """Setejar el tipus de missatge"""
        try:
            obj = objectify.fromstring(self.str_xml)
            self.tipus = obj.get('IdRpt')
        except:
            msg = 'No s\'ha pogut identificar el tipus'
            raise except_f1('Error', _(msg))

    def set_xsd(self):
        """Set xsd file. TG XML files do not use xsd :("""
        pass

    def parse_xml(self):
        """Import xml content"""
        try:
            self.obj = objectify.fromstring(self.str_xml)
        except:
            raise except_f1('Error', _('Document invàlid'))

    # Funcions relacionades amb la capçalera del XML
    @property
    def version(self):
        ref = self.obj.get('Version')
        if not ref:
            raise except_f1('Error', _('Document sense versió'))
        return ref

    @property
    def petition(self):
        ref = self.obj.get('IdPet')
        if not ref:
            raise except_f1('Error', _('Document sense codi de'\
                                       ' petició'))
        return ref

    @property
    def supported(self):
        if self.tipus in ('S02', 'S04', 'S05', 'S12',
                          'S09', 'S13', 'S17', 'S15'):
            return True
        else:
            return False


class except_f1(Exception):
    def __init__(self, name, value):
        self.name = name
        self.value = value
