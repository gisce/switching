# -*- coding: utf-8 -*-

"""Helper functions for libComXml
"""

__all__ = ['codi_periode', 'codi_dh', 'extreu_periode', 'rodes',
           'codi_refact', 'nom_refact', 'codi_reg_refact', 'nom_reg_refact',
           'parse_totals_refact']

CODIS_REFACT = {'RT42011': '40',
                'RT12012': '41',
                'RM42012': '42'}

CODIS_REG_REFACT = {'RGT42011': '40',
                    'RGT12012': '41',
                    'RGM42012': '42'}

PERIODES_AGRUPATS = [('P1', 'P4'), ('P2', 'P5'), ('P3', 'P6')]

# Tarifes que SEMPRE es facturen amb maxímetre
TARIFES_MAXIMETRE = ['003', '011', '012', '013', '014', '015', '016', '018']


def get_rec_attr(obj, attr, default=None):
    try:
        res = reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        if not default is None:
            res = default
        else:
            raise
    return res


def rodes(giro):
    """Retorna el nombre de rodes senceres segons el giro
    """
    return len(str(giro)) - 1

def extreu_periode(name):
    """Extreu el nom del període del name de la lectura
    """
    if '(' not in name:
        return name
    return name.split('(')[-1].split(')')[0]

def codi_periode(codi_dh, periode):
    """Retorna el codi OCSUM del periode segons
       http://172.26.0.42:2500/wiki/show/Codificacio_Periodes_OCSUM
       Taula 42 del document d'OCSUM:
       OCSUM - E - Tablas de códigos 2012.05.23.doc

    :param codi_dh: codi dh de la tarifa
    :param periode: nom del periode en format Px on x = {1...6}
    """

    if codi_dh == '1':
        return '10'
    else:
        return '%s%s' % (codi_dh, periode[-1])

def codi_dh(tarifa, nlectures=6):
    """Retorna el codi ocsum de discriminació horaria
       Taules 35 i 107 del document d'OCSUM:
       OCSUM - E - Tablas de códigos 2012.05.23.doc

    :param tarifa: codi de la tarifa
    :param nlectures: nombre de lectures
    """

    if tarifa in ('001', '005'):
        return '1'
    elif tarifa in ('004', '006'):
        return '2'
    elif tarifa in ('003', '012', '013', '014', '015', '016'):
        return '6'
    elif tarifa == '011':
        if nlectures == 6:
            return '6' 
        else:
            return '3'
    elif tarifa in ('007', '008'):
        return '8'

def codi_refact(producte):
    """Retorna el codi ocsum de refacturació
    
    :param producte: nom del producte
    """
    return CODIS_REFACT.get(producte, False)

def nom_refact(producte):
    """Retorna el nom del producte
    
    :param producte: codi ocsum del producte
    """
    ref = dict(((v, k) for k, v in CODIS_REFACT.items()))
    return ref.get(producte, False)

def codi_reg_refact(producte):
    """Retorna el codi ocsum de refacturació

    :param producte: nom del producte
    """
    return CODIS_REG_REFACT.get(producte, False)

def nom_reg_refact(producte):
    """Retorna el nom del producte

    :param producte: codi ocsum del producte
    """
    ref = dict(((v, k) for k, v in CODIS_REG_REFACT.items()))
    return ref.get(producte, False)

def parse_totals_refact(cadena):
    """Retorna els totals de les línies de refacturacio"""
    totals = []
    for i, x in enumerate(cadena.split(' ')):
        if i in (4, 7):
            totals.append(float(x))
    return totals[0], totals[1]


def aggr_consums(consums):
    """Agrega els consums segons els periodes.

    És a dir P1 = P1 + P4, P2 = P2 + P5, P3 = P3 + P6
    :param consums: Diccionari de maxímetres
    :type consums: dict
    :returns: Un nou diccionari amb els consums agrupats P1, P2 i P3
    :rtype: dict
    """
    if len(consums.keys()) <= len(PERIODES_AGRUPATS):
        return consums

    resultat = {}
    for periode in PERIODES_AGRUPATS:
        resultat[periode[0]] = consums.get(periode[0], 0) \
                                    + consums.get(periode[1], 0)
    return resultat


def exces_reactiva(consum_activa, consum_reactiva, marge):
    """Calcula l'excés de reactiva segons un marge donat.

    :param consum_activa: El consum d'activa
    :type consum_activa: numeric
    :param consum_reactiva: El consum de reactiva
    :type consum_reactiva: numeric
    :param marge: Marge que es pot aplicar (en tant per 1 entre 0-1)
    :type marge: float
    """
    return consum_reactiva - (consum_activa * marge)
