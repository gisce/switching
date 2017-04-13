# -*- coding: utf-8 -*-

# Definició de variables de llibreria
# Taula 107 del document d'OCSUM:
# OCSUM - E - Tablas de códigos 2012.05.23.doc
INFO_TARIFA = {
             #ocsum    descripcio  marge_reactiva   agrupar_consums
             '001': {'name': '2.0A', 'marge': 0.5, 'agrupat': False,
                     'reactiva': ['P1']},
             '005': {'name': '2.1A', 'marge': 0.5, 'agrupat': False,
                     'reactiva': ['P1']},
             '004': {'name': '2.0DHA', 'marge': 0.5, 'agrupat': False,
                     'reactiva': ['P1']},
             '007': {'name': '2.0DHS', 'marge': 0.5, 'agrupat': False,
                     'reactiva': ['P1']},
             '006': {'name': '2.1DHA', 'marge': 0.5, 'agrupat': False,
                     'reactiva': ['P1']},
             '008': {'name': '2.1DHS', 'marge': 0.5, 'agrupat': False,
                     'reactiva': ['P1']},
             '003': {'name': '3.0A', 'marge': 0.33, 'agrupat': True,
                     'reactiva': ['P1', 'P2']},
             '011': {'name': '3.1A', 'marge': 0.33, 'agrupat': True,
                     'reactiva': ['P1', 'P2']},
             '012': {'name': '6.1', 'marge': 0.33, 'agrupat': False,
                     'reactiva': ['P1', 'P2', 'P3', 'P4', 'P5']},
             '013': {'name': '6.2', 'marge': 0.33, 'agrupat': False,
                     'reactiva': ['P1', 'P2', 'P3', 'P4', 'P5']},
             '014': {'name': '6.3', 'marge': 0.33, 'agrupat': False,
                     'reactiva': ['P1', 'P2', 'P3', 'P4', 'P5']},
             '015': {'name': '6.4', 'marge': 0.33, 'agrupat': False,
                     'reactiva': ['P1', 'P2', 'P3', 'P4', 'P5']},
             '016': {'name': '6.5', 'marge': 0.33, 'agrupat': False,
                     'reactiva': ['P1', 'P2', 'P3', 'P4', 'P5']},
          }

# Retorna el nom de periode segons el periode d'OCSUM
PERIODE_OCSUM = {'01': 'P1',  # Punta + Llano
                 '03': 'P2',  # Valle
                 '10': 'P1',  # Totalizador
                 '21': 'P1',  # P1 Tarifes: 004, 006
                 '22': 'P2',  # P2 Tarifes: 004, 006
                 '31': 'P1',  # P1 Tarifa 011
                 '32': 'P2',  # P2 Tarifa 011
                 '33': 'P3',  # P3 Tarifa 011
                 '61': 'P1',  # Periodo 1 Tarifes: 003, 011, 012 - 016
                 '62': 'P2',  # Periodo 2 Tarifes: 003, 011, 012 - 016
                 '63': 'P3',  # Periodo 3 Tarifes: 003, 011, 012 - 016
                 '64': 'P4',  # Periodo 4 Tarifes: 003, 011, 012 - 016
                 '65': 'P5',  # Periodo 5 Tarifes: 003, 011, 012 - 016
                 '66': 'P6',  # Periodo 6 Tarifes: 003, 011, 012 - 016
                 '81': 'P1',  # P1 Tarifa 007
                 '82': 'P2',  # P2 Tarifa 007
                 '83': 'P3'}  # P3 Tarifa 007

# Magnituds d'OCSUM
MAGNITUDS_OCSUM = {'AE': 'A',
                   'R1': 'R',
                   'PM': 'M',
                   'EP': 'EP'}

# Totalitzadors a ignorar
SKIP_TOTALITZADORS = ('00', '60')
