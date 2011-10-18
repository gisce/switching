
# -*- coding: utf-8 -*

from lxml import objectify

class Message(object)
    """Classe base"""
    def __init__(self):
        """Construeix un missatge base.
        """
        self.tipus = ''

    def get_tipus_xml(self, f_xml):
        """Obtenir el tipus de missatge
        """
        obj = objectify.fromstring(f_xml)
        self.tipus = obj.Cabecera.CodigoDelProceso
        return self.tipus
    
