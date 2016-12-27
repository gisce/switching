# -*- coding: utf-8 -*-

# Mapeig de distribuïdores

provincies_arago = ['22', '44', '50']  # Osca, Terol, Saragossa
conv_dict_5 = {
    # ENDESA
    '00311': '0023',  # cia sevillana
    '00313': '0120',  # Aragonesa actividades
    '00315': '0288',  # Balears: Gas y electricidad
    '00316': '0363',  # Unión Eléctrica Canárias SUP
    # FENOSA
    '03900': '0022',
}

conv_dict_6 = {'003130': '0029', }  # FECSA Aragó

# Not standarized table. Used in CIE forms
TIPUS_DOCUMENT_INST_CIE = [
    ('nif', 'NIF'),
    ('codigo', 'Código')
]
# For modcon wizard
SEL_CONFIG_MODCON_WIZ_TYPE = [
    ('tarpot', 'Tarifa/potència'),
    ('owner', 'Titular'),
    ('both', u'Ambdós')
]

# Pas 03
# Legacy table, now implemented in giscedata_switching_data.xml
REBUIG = [('1', u'No existe Punto de Suministro asociado al CUPS'),
          ('2', u'Inexistencia de Contrato de ATR previo en vigor'),
          ('3', u'NIF-CIF No coincide con el del Contrato en vigor'),
          ('6', u'Existencia de Solicitud ATR previa en curso'),
          ('8', u'Duración y/o Tipo de Renovación del Contrato sin '
                u'informar o no válida'),
          ('11', u'Comercializadora incorrecta'),
          ('12', u'Contrato cortado'),
          ('36', u'NIF-CIF Erróneo'),
          # ('37', u'Existencia de Solicitud previa en curso A3'),
          ('38', u'Existencia de Solicitud previa en curso C1'),
          # ('39', u'Existencia de Solicitud previa en curso C2'),
          # ('40', u'Existencia de Solicitud previa en curso M1'),
          # ('41', u'Existencia de Solicitud previa en curso B1'),
          ('43', u'Error al anular Solicitud finalizada'),
          ('45', u'Fecha de Finalización de Contrato sin informar '
                 u'(Eventuales, Temporada y Obras)'),
          ('46', u'Fecha de la operación solicitada con carácter retroactivo'),
          ('62', u'Actuación Solicitada por Comercializador no acorde con '
                 u'requerimientos Cliente'),
          ('99', u'Otros')]

# Pas 02 i 11
# TABLA_55
TABLA_55 = [('L', 'En ciclo de lectura'),
                   ('F', 'En fecha fixa'),
                   ('C', 'Tras actuaciones en campo')]

TIPUS_ACTIVACIO = TABLA_55


# TABLA_39
TABLA_39 = [('1', 'Alta'),
            ('2', 'Baja'),
            ('3', "Tramitación de Alta"),
            ('4', 'Tramitación de Baixa'),
            ('5', 'Tramitación de Modificación')]

ESTAT_PM = TABLA_39


# TABLA_40
TABLA_40 = [('C', 'Comprobante'),
             ('P', 'Principal'),
             ('R', 'Redundante')]

FUNCIO_PM = TABLA_40


# TABLA_38
TABLA_38 = [('1', 'Lectura local manual'),
            ('2', 'Lectura local optoacoplador'),
            ('3', 'Lectura local puerto serie'),
            ('4', 'Telemedida operativa'),
            ('5', 'Telemedida no operativa')]

MODE_PM = TABLA_38


# TABLA_30
TABLA_30 = [('01', u"Punto de medida tipo 1"),
            ('02', u"Punto de medida tipo 2"),
            ('03', u"Punto de medida tipo 3"),
            ('04', u"Punto de medida tipo 4"),
            ('05', u"Punto de medida tipo 5"),
            ]

TIPUS_PM = TABLA_30


# TABLA_37
TABLA_37 = [('A', 'Alta'), ('B', 'Baja'), ('M', 'Modificación')]

TIPUS_MOVIMENT = TABLA_37


# TABLA_6
TABLA_6 = [('CI', 'CIF'),
           ('CT', 'Carta de trabajo'),
           ('DN', 'DNI'),
           ('NI', 'NIF'),
           ('NV', 'N.I.V.A'),
           ('OT', 'Otro'),
           ('PS', 'Pasaporte'),
           ('NE', 'NIE'),
           ]

TIPUS_DOCUMENT = TABLA_6


# TABLA_26
# TABLA_34
TABLA_34 = [('S', 'Sí'), ('N', 'No')]

SINO = TABLA_34


# TABLA_25
TABLA_25 = [
    ('001', 'AB'),
    ('002', 'ABB'),
    ('003', 'ITRON'),
    ('004', 'AEG'),
    ('005', 'AEMSA'),
    ('006', 'AGORRIA'),
    ('007', 'AGS'),
    ('008', 'AGUT'),
    ('009', 'ALSTHOM'),
    ('010', 'ARON'),
    ('011', 'ARTECHE'),
    ('012', 'ASEA'),
    ('013', 'BAER'),
    ('014', 'BALTEAV'),
    ('015', 'BARBERG'),
    ('016', 'BERGMAN'),
    ('017', 'BK'),
    ('018', 'BRINER'),
    ('019', 'BROW BOVERI'),
    ('020', 'CDC/SCH'),
    ('021', 'CELSA'),
    ('022', 'CEPED'),
    ('023', 'CHAMON'),
    ('024', 'CHASSERAL'),
    ('025', 'CIAMA'),
    ('026', 'CIRCUTOR'),
    ('027', 'COMPACT MODEM GSM'),
    ('028', 'CONTIMETER'),
    ('029', 'DAG'),
    ('031', 'DIFERENCIAL'),
    ('032', 'DIMACO'),
    ('033', 'DINUY'),
    ('034', 'DOPAS'),
    ('035', 'DYTEMAT (CRADY)'),
    ('036', 'EGA'),
    ('037', 'EGUREN'),
    ('038', 'ELIOP'),
    ('039', 'ERICSON'),
    ('040', 'FECHA'),
    ('041', 'FIERRO'),
    ('042', 'FLASH'),
    ('043', 'FTM'),
    ('044', 'FTR'),
    ('045', 'G.E.E.'),
    ('046', 'GALEICO'),
    ('047', 'GALIL'),
    ('048', 'GANZ'),
    ('049', 'GAVE'),
    ('050', 'GEAL'),
    ('051', 'GENERAL ELEC.'),
    ('052', 'GRASSILIN'),
    ('053', 'GUIJARRO HNOS.'),
    ('054', 'HAGER'),
    ('055', 'HARDWARE'),
    ('056', 'HB'),
    ('057', 'HELIOWATT'),
    ('058', 'INDRA'),
    ('059', 'INDRA/TARCON'),
    ('060', 'ISKRA-METREGA (METRELEC)'),
    ('061', 'ISODEL'),
    ('062', 'ISOLUX WAT S.A.'),
    ('063', 'ISSARIA'),
    ('064', 'KAINAS'),
    ('065', 'KAINOTRAF'),
    ('066', 'KLOCKNER MOELLER'),
    ('067', 'KORTING-KANDEN'),
    ('068', 'LABORAT. ELEC.'),
    ('069', 'LANDIS'),
    ('070', 'LANDIS-ESPAÑA'),
    ('071', 'LANDIS/SIEM.METERING'),
    ('072', 'LARRAÑAGA'),
    ('073', 'LATECNO'),
    ('074', 'LAURK'),
    ('075', 'LEGRAND'),
    ('076', 'LEISA'),
    ('077', 'LEMAG'),
    ('078', 'M.M.E.'),
    ('079', 'MEDEX'),
    ('080', 'MERC LIBERALIZ CAPT'),
    ('081', 'MERLIN GERIN'),
    ('082', 'METREGA/ISKRA'),
    ('083', 'METRON'),
    ('084', 'MONTROUGE'),
    ('085', 'NORMA'),
    ('086', 'O.P.U.'),
    ('087', 'OCESA'),
    ('088', 'OCREICON'),
    ('089', 'OERLIKON'),
    ('090', 'ORBIS'),
    ('091', 'P.F.N.'),
    ('092', 'PELEPTRIC'),
    ('093', 'POPPER'),
    ('094', 'QL Y TOC'),
    ('095', 'RIESA (ROMANILLOS)'),
    ('096', 'ROMANILLOS'),
    ('097', 'ROMO'),
    ('098', 'S.C.G.'),
    ('099', 'SABADELL'),
    ('100', 'SACI'),
    ('101', 'SAGEM'),
    ('102', 'SAUTER'),
    ('103', 'SAVIR'),
    ('104', 'SCHLUMBERGER'),
    ('105', 'SIEMENS'),
    ('106', 'SIEMENS METERING'),
    ('107', 'SIFAN'),
    ('108', 'SIMON'),
    ('109', 'SISTELTROM'),
    ('110', 'SISTELTRON/ELECTROMATIC'),
    ('111', 'SKUPP'),
    ('112', 'SODECO'),
    ('113', 'SPRECHER'),
    ('114', 'STOTZ KONTAKT (ABB)'),
    ('115', 'STRONG'),
    ('116', 'SUMASA'),
    ('117', 'TARCON'),
    ('118', 'TAUBE'),
    ('119', 'TELEC'),
    ('120', 'TELEMECANICA'),
    ('121', 'TEMPER'),
    ('122', 'TERASAKI'),
    ('123', 'UNELCO'),
    ('124', 'UNELEC'),
    ('125', 'VAYRIS'),
    ('126', 'WANDLER BG'),
    ('127', 'WAVECOM'),
    ('128', 'WESTINGHOUSE'),
    ('129', 'WIKERS'),
    ('130', 'XACOM'),
    ('131', 'ZENIT'),
    ('132', 'ZIV'),
    ('133', 'ZURC'),
    # Migrate 134 to 003 (FORMER ACTARIS)
    ('134', 'ITRON'),
    ('198', 'VARIOS'),
    ('199', 'DESCONOCIDA'),
]

MARCA_APARATO = TABLA_25


# TABLA_24
TABLA_24 = [
    ('BP', 'Bloque pruebas'),
    ('CA', 'Contador activa'),
    ('CC', 'Contador combinado'),
    ('CG', 'Contador registrador'),
    ('CO', 'Contactor'),
    ('CR', 'Contador reactiva'),
    ('CT', 'Contador tarifador'),
    ('G', 'S.V.R.'),
    ('H', 'U.M.P.'),
    ('IH', 'Interruptor horario'),
    ('IP', 'I.C.P.'),
    ('MO', 'Modem'),
    ('P', 'Contador rpm'),
    ('RG', 'Registrador'),
    ('RT', 'Rele selector tension'),
    ('TA', 'Tarifador'),
    ('TC', 'Trasnformador combinado'),
    ('TI', 'Transformador intensidad'),
    ('TP', 'Transformador potencia'),
    ('TT', 'Transformador de tensión'),
]

TIPO_APARATO = TABLA_24


TIPO_EM_APARATO = [
    ('L00', 'El que corresponda Reglamentariamente'),
    ('L01', 'Tipo 1'),
    ('L02', 'Tipo 2'),
    ('L03', 'Tipo 3'),
    ('L04', 'Tipo 4 - 6 períodos'),
    ('L05', 'Tipo 4 - horario'),
    ('L06', 'Tipo 5 - un período'),
    ('L07', 'Tipo 5- dos períodos'),
    ('L08', 'Tipo 5 - seis períodos'),
    ('L09', 'Tipo 5 - horario'),
    ('L10', 'Tipo 4 - transitorio'),
    ('R00', 'Sin discriminación horaria'),
    ('R01', 'Sin contador discriminador'),
    ('R02', 'Dos períodos'),
    ('R03', 'Tres períodos, sin discriminación de sábados y festivos'),
    ('R04', 'Tres períodos, con discriminación de sábados y festivos'),
    ('R05', 'Cinco períodos'),
    ('R06', 'Seis períodos'),
    ('R07', 'Siete períodos'),
]


# TABLA_31
TABLA_31 = [
    ('CX', 'Conexión y precintado'),
    ('MO', 'Montaje'),
    ('RE', 'Reparametrización'),
    ('DX', 'Desconexión'),
]

TIPO_MOVIMIENTO_APARATO = TABLA_31


# TABLA_32
TABLA_32 = [
    ('1', 'Distribuidor'),
    ('2', 'Cliente'),
    ('3', 'Comercializador'),
    ('4', 'Otros'),
]

TIPO_PROPIEDAD_APARATO = TABLA_32


# TABLA_33
TABLA_33 = [
    ('C', 'Control'),
    ('M', 'Medición'),
]

FUNCION_APARATO = TABLA_33


# TABLA_35
TABLA_35 = [
    ('0', 'Dos períodos (Tarifa Nocturna)'),
    ('1', 'Sin discriminación horaria'),
    ('2', 'Dos períodos'),
    ('3', 'Tres períodos, sin discriminación de sábados y festivos'),
    ('4', 'Tres períodos, con discriminación de sábados y festivos'),
    ('5', 'Cinco períodos'),
    ('6', 'Seis períodos'),
    ('7', 'Siete períodos'),
    ('8', 'DH Supervalle'),
]

TIPO_DH_APARATO = TABLA_35


# TABLA_50
TABLA_50 = [
    ('1', 'Modo 1 sin maxímetro'),
    ('2', 'Modo 2 sin maxímetro'),
    ('3', 'Modo 3 con dos maxímetros'),
    ('4', 'Modo 4 con tres maxímetros'),
    ('5', 'Estacional tipo A'),
    ('6', 'Estacional tipo B'),
    ('7', 'THP'),
    ('8', 'Tarifa de 6 máximas'),
]

TIPO_DH_MAX = TABLA_50


ESTAT_TEL_PM = [
    ('1', 'Correcto'),
    ('2', 'No probado'),
    ('3', 'Línea tlf. fuera servicio'),
    ('4', 'Módem no enlaza'),
    ('5', 'Registrador desprogramado'),
    ('6', 'Falla la dire de enlace'),
    ('7', 'Falla el pto y clave medida'),
    ('8', 'El registrado mide ceros'),
    ('9', 'Otras'),
]


# TABLA_42
TABLA_42 = [
    ('00', 'Totalizador'),
    ('01', 'Punta+Llano'),
    ('03', 'Valle'),
    ('10', 'Totalizador'),
    ('20', 'Totalizador'),
    ('21', 'Punta'),
    ('22', 'Llano+Valle'),
    ('30', 'Totalizador'),
    ('31', 'Punta'),
    ('32', 'Llano'),
    ('33', 'Valle'),
    ('40', 'Totalizador'),
    ('41', 'Punta'),
    ('42', 'Llano'),
    ('43', 'Valle'),
    ('50', 'Totalizador'),
    ('51', 'Punta Alto'),
    ('52', 'Llano'),
    ('53', 'Valle'),
    ('54', 'Supervalle'),
    ('55', 'Punta Pico'),
    ('60', 'Totalizador'),
    ('61', 'Período 1'),
    ('62', 'Período 2'),
    ('63', 'Período 3'),
    ('64', 'Período 4'),
    ('65', 'Período 5'),
    ('66', 'Período 6'),
    ('70', 'Totalizador'),
    ('71', 'Período 1'),
    ('72', 'Período 2'),
    ('73', 'Período 3'),
    ('74', 'Período 4'),
    ('75', 'Período 5'),
    ('76', 'Período 6'),
    ('77', 'Período 7'),
    ('80', 'Totalizador'),
    ('81', 'Punta+Llano'),
    ('82', 'Valle'),
    ('83', 'SuperValle'),
]

PERIODO = TABLA_42


# TABLA_43
TABLA_43 = [
    ('AE', 'Energía activa entrante'),
    ('AS', 'Energía activa saliente'),
    ('EP', 'Excesos de potencia'),
    ('PM', 'Potencia máxima'),
    ('R1', 'Energía reactiva en cuadrante 1'),
    ('R2', 'Energía reactiva en cuadrante 2'),
    ('R3', 'Energía reactiva en cuadrante 3'),
    ('R4', 'Energía reactiva en cuadrante 4'),
]

MAGNITUD = TABLA_43

# TABLA_44
TABLA_44 = [
    ('10', 'Telemedida'),
    ('11', 'Telemedida corregida'),
    ('20', 'TPL'),
    ('21', 'TPL corregida'),
    ('30', 'Visual'),
    ('31', 'Visual corregida'),
    ('40', 'Estimada'),
    ('50', 'Autolectura'),
    ('99', 'Sin lectura'),
]

PROCEDENCIA = TABLA_44


# TABLA_45
TABLA_45 = [
    ('01', 'Punto de medida inaccesible'),
    ('02', 'Punta de medida ilocalizable'),
    ('03', 'Presunto fraude'),
    ('04', 'Registrador apagado'),
    ('05', 'Registrador no comunica'),
    ('99', 'Otras anomalías'),
]

ANOMALIA_MESURA = TABLA_45


CONTROL_POTENCIA = [
    ('1', 'ICP'),
    ('2', 'Maxímetro'),
]

REPRESENTANT = [('S', 'Substituto'),
                ('M', 'Mandatario')]

PERSONA = [('F', 'Física'),
           ('J', 'Jurídica')]

TABLA_7 = [('S', u"(S) La solicitud no implica cambios "
                 u"de condiciones contractuales"),
           ('N', u"(N) La solicitud implica cambios de "
                 u"condiciones contractuales"),
           ('A', u"(A) La solicitud implica cambios "
                 u"contractuales y administrativos"),
           ('P', u"(P) La solicitud implica cambios "
                 u"en la periodicitad de la facturación")]

TABLA_8 = [('S', 'Según ciclo de lectura'),
           ('N', 'Al cabo de 15 días (plazo legal)')]

TABLA_9 = [('01', 'Anual'),
           ('02', 'Eventual medido'),
           ('03', 'Temporada'),
           ('05', 'Subministro Régimen especial'),
           ('07', 'Subministro de Obras'),
           ('08', 'Subministro de Socorro'),
           ('09', 'Eventual a tanto alzado'),
           ('10', 'Pruebas')]

TABLA_10 = [('01', u"Cese Actividad"),
            ('02', u"Fin de contracto de energía"),
            ('03', u"Corte de subministro"),
            ('04', u"Baja por impago"),
            ('05', u"Baja sin deconexión definida de instalaciones")]

TABLA_11 = [('S', u"(S) Si el domicilio fiscal coincide "
                  u"con el de subministro"),
            ('F', u"(F) Si el domicilio fiscal no coincide "
                  u"con el de subministro")]

# TABLA_12 TIPO VIA Optional , thus not implemented

# TABLA_13 ESCALERA Optional , thus not implemented

# TABLA_14 PISO Optional , thus not implemented

# TABLA_15 PUERTA Optional , thus not implemented

# TABLA_16 ACLARADOR DE FINCA Optional , thus not implemented

TARIFES_SEMPRE_MAX = ['003', '011', '012', '013', '014', '015', '016', '017']
TARIFES_6_PERIODES = ['012', '013', '014', '015', '016', '017']

TABLA_17 = [
    ('001', '2.0A'),
    ('003', '3.0A'),
    ('004', '2.0DHA'),
    ('005', '2.1A'),
    ('006', '2.1DHA'),
    ('007', '2.0DHS'),
    ('008', '2.1DHS'),
    ('011', '3.1A'),
    ('012', '6.1A'),
    ('013', '6.2'),
    ('014', '6.3'),
    ('015', '6.4'),
    ('016', '6.5'),
    ('017', '6.1B'),
]

TABLA_18 = [
    ('C', 'Cliente comercialitzador'),
    ('D', 'Distribuidor'),
    ('N', 'Cliente/Comercializador no lo conoce'),
]

TABLA_19 = [
    ('Y', 'Ya està instalado'),
    ('C', 'Cliente/Comercializador'),
    ('D', 'Distribuidor'),
]

TABLA_20 = [
    ('C', 'Cliente comercializador'),
    ('D', 'Distribuidor'),
    ('N', 'Cliente/Comercializador desconoce'),
]

TABLA_21 = [
    ('Y', 'Ya està instalado'),
    ('C', 'Cliente/Comercializador'),
    ('D', 'Distribuidor'),
]

TABLA_22 = [
    ('L00', 'El que corresponda reglamentariamente'),
    ('L01', 'Tipo 1'),
    ('L02', 'Tipo 2'),
    ('L03', 'Tipo 3'),
    ('L04', 'Tipo 4 - 6 períodos'),
    ('L05', 'Tipo 4 - horario'),
    ('L06', 'Tipo 5 - un período'),
    ('L07', 'Tipo 5 - dos períodos'),
    ('L08', 'Tipo 5 - sis períodos'),
    ('L09', 'Tipo 5 - horario'),
    ('L10', 'Tipo 4 - transitorio'),
    ('R00', 'Sin discriminación horaria'),
    ('R01', 'Sin contador discriminador'),
    ('R02', 'Dos períodos'),
    ('R03', 'Tres períodos, sin discriminación de sábados y festivos'),
    ('R04', 'Tres períodos, amb discriminación de sábados y festivos'),
    ('R05', 'Cinco períodos'),
    ('R06', 'Seis períodos'),
    ('R07', 'Siete períodos'),
]

TABLA_23 = [
    ('S', 'Suministro'),
    ('F', 'Fiscal'),
    ('O', 'Otra'),
]

# You may use SINO table defined previously
TABLA_26 = [('S', 'Hay actuaciones en campo'),
            ('N', 'No hay actuaciones en campo')]

TABLA_28 = [
    ('01', '(01) Cliente ausente'),
    ('02', '(02) Acceso imposibilitado'),
    ('03', '(03) Instalación no reglamentaria'),
    ('04', u"(04) Las deficiencias en la instalación han sido "
           u"mal subsanadas"),
    ('05', u"(05) La instalación del suministro no se corresponde con la "
           u"prevista en la orden de servicio (anormalidades o fraudes)"),
    ('06', u"(06) El cliente no ha puesto el equipo de su propiedad "
           u"a disposición de la Distribuidora"),
    ('07', '(07) El equipo propiedad del cliente no es adecuado'),
]

TABLA_29 = [('S', 'Activado con las condiciones solicitadas'),
            ('N', u"Activado con las condiciones vigentes "
                  u"anteriores a la solicitud")]

TABLA_30 = [('01', u"Punto de medida tipo 1"),
            ('02', u"Punto de medida tipo 2"),
            ('03', u"Punto de medida tipo 3"),
            ('04', u"Punto de medida tipo 4"),
            ('05', u"Punto de medida tipo 5"),
            ]

# You may use SINO table defined previously
TABLA_36 = [('S', 'Lectura no acumulativa'),
            ('N', 'Lectura acumulativa')]

TABLA_41 = [('1', 'Correcto'),
            ('2', 'No probado'),
            ('3', 'Línea telef. fuera servicio'),
            ('4', 'Módem no enlaza'),
            ('5', 'Registrador desprogramado'),
            ('6', 'Falla la dire de enlace'),
            ('7', 'Falla el pto y clave medida'),
            ('8', 'El registrado mide ceros'),
            ('9', 'Otras'),
            ]

TABLA_53 = [
    ('T', 'Traspaso'),
    ('S', 'Subrogación'),
    ('J', 'Cambio por Justo Título'),
    ('A', 'Cambio datos administrativos'),
    ('B', 'Alta y baja'),
    ('H', 'Alta y baja en ciclo de lectura'),
]

# You may use SINO table defined previously
TABLA_54 = [
    ('S', 'Si coinciden'),
    ('N', 'No coinciden'),
]

TABLA_61 = [
    ('01', u'CIE'),
    ('02', u'Acta de Puesta en Marcha'),
    ('03', u'Acta de Inspección'),
    ('04', u'Reclamación'),
    ('05', u'Respuesta a reclamación'),
    ('06', u'Facturas'),
    ('07', u'Otra documentación del cliente'),
    ('08', u'Otros'),
]

TABLA_62 = [
    ('AL', u'Almacén'),
    ('AP', u'Alumbrado publico'),
    ('AS', u'Ascensores'),
    ('AT', u'Antena Telefonía Móvil'),
    ('BA', u'Batería de acumuladores'),
    ('CM', u'Centro de Maniobra y Control'),
    ('EA', u'Escalera-Ascensor'),
    ('ES', u'Escalera'),
    ('FT', u'Fabrica y Talleres sin Riesgo Especifico'),
    ('FV', u'Inst. Fotovoltaica'),
    ('GA', u'Garaje'),
    ('GB', u'Grupo Bombeo, Riego por Goteo'),
    ('HP', u'Loc.Húmedos con Riesgo Corrosión o Polv.'),
    ('IN', u'Nave industrial'),
    ('IT', u'Instalación Temporal en Emplazam.Abierto'),
    ('KC', u'Kioskos / cabinas tfno'),
    ('LB', u'Locales a Baja Temperatura'),
    ('LC', u'Local comercial'),
    ('OF', u'Oficina'),
    ('PC', u'Publica concurrencia'),
    ('RA', u'Refugio o Albergue Agrícola'),
    ('RT', u'Repetidor de Televisión'),
    ('SA', u'Servicios Auxiliares'),
    ('SC', u'Sumtro complementario'),
    ('SE', u'Sumtro eventual'),
    ('SG', u'Servicio general vivienda'),
    ('SM', u'Semáforo'),
    ('SO', u'Sumtro obras'),
    ('TL', u'Telecomunicaciones'),
    ('TR', u'Trastero'),
    ('UF', u'Uso finca'),
    ('UV', u'Usos Varios'),
    ('VI', u'Vivienda'),
]

TABLA_64 = [
    ('01', u'1X220'),
    ('02', u'1X230'),
    ('03', u'3X380'),
    ('04', u'3X380/220'),
    ('05', u'3X400'),
    ('06', u'3X400/230'),
    ('07', u'1X127'),
    ('08', u'1X133'),
    ('09', u'2X220'),
    ('10', u'2X230'),
    ('11', u'3X220'),
    ('12', u'3X220/127'),
    ('13', u'3X230'),
    ('14', u'3X230/133'),
    ('15', u'5.000'),
    ('16', u'6.000'),
    ('17', u'7.200'),
    ('18', u'8.000'),
    ('19', u'10.000'),
    ('20', u'11.000'),
    ('21', u'12.000'),
    ('22', u'13.000'),
    ('23', u'13.200'),
    ('24', u'15.000'),
    ('25', u'16.500'),
    ('26', u'17.000'),
    ('27', u'20.000'),
    ('28', u'22.000'),
    ('29', u'25.000'),
    ('30', u'26.500'),
    ('31', u'30.000'),
    ('32', u'36.000'),
    ('33', u'44.000'),
    ('34', u'45.000'),
    ('35', u'66.000'),
    ('36', u'110.000'),
    ('37', u'132.000'),
    ('38', u'220.000'),
    ('39', u'400.000'),
]

TABLA_65 = [
    ('ES', u'Estatal'),
    ('AU', u'Autonómico'),
    ('PR', u'Provincial'),
    ('LO', u'Local'),
]

# TABLA_73
# Implemented in giscedata_switching_data.xml

TABLA_74 = [('01', u'Concertacion de visita'),
            ('02', u'Ejecución visita')]

TABLA_75 = [('001', u'Ausente'),
            ('002', u'Imposible de localizar'),
            ('003', u'Deshabitado'),
            ('004', u'Anomalía instalación'),
            ('005', u'No realizada por causas imputables al cliente'),
            ('006', u'No realizada por causas imputables al distribuidor'),
            ('007', u'Concertación de Visita'),
            ('008', u'Concertación anterior anulada. Pendiente concertar'),
            ('009', u'Concertación fallida'),
            ('010', u'No concertado'),
            ('011', u'Programado en > 6 días')
            ]

TABLA_76 = [('01', u'Nuevo teléfono de contacto'),
            ('02', u'Nueva persona de contacto'),
            ('03', u'Nuevo email de contacto'),
            ('04', u'IBAN')
            ]

TABLA_77 = [('01', u'Potencia'),
            ('02', u'Reactiva'),
            ('03', u'Penalización ICP'),
            ('04', u'Alquiler de equipo de medida'),
            ('05', u'Impuestos'),
            ('06', u'Excesos de potencia'),
            ('07', u'Derechos'),
            ('08', u'Depósito de garantía'),
            ('09', u'Verificación de equipos de medida'),
            ('10', u'Derechos de corte y reconexión'),
            ('11', u'Abono por calidad de suministro'),
            ('12', u'Abono por calidad individual'),
            ('13', u'Coste de reposición'),
            ('14', u'Refacturaciones regulatorias'),
            ]

TABLA_79 = [('01', u'Potencia Contratada'),
            ('02', u'Titular'),
            ('03', u'Tarifa de acceso'),
            ('04', u'Propiedad del equipo de medida'),
            ('05', u'Fecha de activación'),
            ('06', u'Tipo de contrato'),
            ('07', u'Modo control-potencia'),
            ('08', u'Periodicidad facturación')
            ]


TABLA_80 = [('01', u'Procedente / Favorable'),
            ('02', u'Improcedente / Desfavorable'),
            ('03', u'No gestionable'),
            ('04', u'Mal Tipificada'),
            ('05', u'Duplicada')
            ]

TABLA_81 = [('01', u'ATENCIÓN PERSONAL'),
            ('02', u'FACTURACIÓN Y MEDIDA'),
            ('03', u'CONTRATACIÓN'),
            ('04', u'GESTIÓN DE ACOMETIDAS'),
            ('05', u'CALIDAD DE SUMINISTRO'),
            ('06', u'SITUACIÓN DE INSTALACIONES'),
            ('07', u'ATENCION REGLAMENTARIA'),
            ]

TABLA_83 = [('01', u'Cliente / Titular de PS'),
            ('02', u'Representante Legal'),
            ('03', u'Aseguradora'),
            ('04', u'Administraciones/Organísmos públicos'),
            ('06', u'Comercializador'),
            ('07', u'Juzgados'),
            ('08', u'Afectado no titular del PS'),
            ]

TABLA_84 = [('01', u'Solicitud de Información adicional'),
            ('02', u'Comunicación de estado intermedia'),
            ('03', u'Comunicación de retipificación de la reclamación')
            ]

TABLA_85 = [('01', u'Factura reparación'),
            ('02', u'Nuevos Datos de Contacto'),
            ('03', u'Documento oficial'),
            ('04', u'Contacto y documentos'),
            ('05', u'IBAN'),
            ('06', u'Información mínima incoherente'),
            ]

# Includes Description in field 2
TABLA_86 = [
    ('01',
     u'Comprobación',
     u'Cliente indica / solicita le comprueben el contador. En caso de equipo '
     u'correcto, implicará asumir los costes asociados a los derechos de '
     u'actuación (si el equipo es de alquiler y en cualquier caso si el '
     u'equipo es propiedad del cliente).'
     ),
    ('02',
     u'Verificación con patrón',
     u'Cliente indica / solicita le verifiquen el contador. El cliente debe '
     u'estar informado de los costes asociados. En caso de equipo correcto, '
     u'implicará asumir los costes asociados a la verificación (si el equipo '
     u'es de alquiler y en cualquier caso si el equipo es propiedad del '
     u'cliente).'
     ),
    ('03', u'Contador robado/ Sin contador', ''),
    ('04', u'Contador averiado: parado, pantalla apagada/falla, sigue contando '
           u'sin nada conectado en domicilio, quemado, error conexionado, '
           u'suministro sin tensión.',
           u'Parado, pantalla apagada / falla, sigue contando sin nada '
           u'conectado en domicilio, quemado, error conexionado, suministro '
           u'sin tensión. En caso de equipo correcto, implicará asumir los '
           u'costes asociados a los derechos de actuación (si el equipo es de '
           u'alquiler y en cualquier caso si el equipo es propiedad del '
           u'cliente).'
     ),
    ('05', u'Incidencias ICP', ''),
    ('06', u'Contador desprogramado: DH o reloj desprogramado (sólo marca en '
           u'punta o en valle o las muestra cambiadas, dígitos contador no se '
           u'corresponde con factura.',
           u'DH o reloj desprogramado (sólo marca en punta o en valle o las '
           u'muestra cambiadas, dígitos contador no se corresponde con '
           u'factura. En caso de equipo correcto, implicará asumir los costes '
           u'asociados a los derechos de actuación (si el equipo es de '
           u'alquiler y en cualquier caso si el equipo es propiedad del '
           u'cliente).'
     )
]

# Includes Description in field 2
TABLA_87 = [
    ('01',
     u'Por personal de canales de atención',
     u'Trato inapropiado del personal de atención telefónica, oficinas '
     u'presenciales o cualquier otro canal.'
     ),
    ('02',
     u'Por operarios de equipos de medida',
     u'Trato inapropiado por personal durante la ejecución de trabajos en '
     u'equipo de medida (corte, conexión, precintado, comprobación, etc..)'
     ),
    ('03',
     u'Por operarios de nuevos suministros',
     u'Trato inapropiado por personal durante trabajos de estudios de conexión '
     u'y ejecución de obras de acometidas'
     ),
    ('04',
     u'Por operarios de inspección',
     u'Trato inapropiado por personal de inspección derivados de expedientes '
     u'de anomalía y fraude.'
     ),
    ('05',
     u'Por operaciones',
     u'Trato inapropiado por personal de operación y mantenimiento de red y '
     u'descargos.'
     ),
    ('06',
     u'Por operarios de lecturas',
     u'Trato inapropiado del personal de lectura durante la  toma de lectura '
     u'en campo'
     ),
]

# TABLA_101
# giscedata_facturacio.defs.TIPO_FACTURA_SELECTION

# TABLA_102
# giscedata_facturacio.defs.TIPO_RECTIFICADORA_SELECTION

# TABLA_103 TIPO_CONCEPTO
# giscedata_facturacio_comer.data.xml id="concepte_xx"

# TABLA_104 TIPO_MONEDA
# not implemented

# TABLA_105 TIPO_FACTURACION
# giscedata_facturacio.defs.TIPO_FACTURACION_SELECTION

TABLA_106 = [('01', u'Verificación equipo de medida'),
             ('02', u'Avería en contador'),
             ('03', u'Avería en Trafo de Tensión'),
             ('04', u'Avería en Trafo de intensidad'),
             ('05', u'Desbordamiento del Registrador'),
             ('06', u'Problemas en la sincronización del registrador'),
             ('07', u'Pérdida de alimentación del registrador'),
             ('08', u'Manipulación de equipos'),
             ('09', u'Servicio Directo (sin EM)'),
             ('10', u'Punto de medida inaccesible'),
             ('11', u'Punto de medida ilocalizable'),
             ('99', u'Otros')
             ]

# TABLA_107 Código Tarifa
# Defined in tariff model `giscedata.polissa.tarifa`, field `codi_ocsum`

TABLA_108 = [('01', u'Mensual'),
             ('02', u'Bimestral')]

TABLA_109 = [('01', u'Telegestión Operativa con CCH'),
             ('02', u'Telegestión No Operativa'),
             ('03', u'Telegestión Operativa sin CCH'), ]

TABLA_110 = [('01', u'Acompaña curva de carga'),
             ('02', u'Perfilado'),
             ('03', u'No aplica'), ]

TABLA_111 = [('01', u'Telegestión Operativa con Curva de Carga Horaria'),
             ('02', u'Telegestión Operativa sin Curva de Carga Horaria'),
             ('03', u'Sin Telegestión'), ]

# Converts 109 Table vlues to 111 Table equivalence
CONV_T109_T111 = {'01': '01',  # TG with CCH
                  '02': '03',  # No TG
                  '03': '02'}  # TG without CCH

# Es un tipo de Autoconsumo 2, cuyas instalaciones  de producción conectadas en
# la red interior del consumidor están incluidas en el ámbito de aplicación del
# RD 1699/2011 , la suma de las potencias instaladas de producción no es
# superior a 100kW, el consumidor y los titulares de las instalaciones de
# producción son la misma persona física o jurídica, disponen de la
# configuración de medida establecida en el artículo 13.2.b) del RD 900/2015 y
# han formalizado un solo contrato de acceso conjunto para los SSAA y para el
# consumo asociado

TABLA_113 = [('00', u'Sin Autoconsumo'),
             ('01', u'Autoconsumo Tipo 1'),
             ('2A',
              u'Autoconsumo tipo 2 (según el Art. 13. 2. a) RD 900/2015)'
              ),
             ('2B',
              u'Autoconsumo tipo 2 (según el Art. 13. 2. b) RD 900/2015)'
              ),
             ('2G',
              (u'Servicios auxiliares de generación ligada a un autoconsumo '
               u'tipo 2')
              ),
             ]

# Data about R101 subtypes and their minimum fields
SUBTYPES_R101 = [
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente',
                               'telefono_contacto', 'cups',
                               'fecha_incidente', 'comentarios',
                               'persona_de_contacto',
                               'tipo_atencion_incorrecta'],
                'code': '01',
                'name': u'ATENCION INCORRECTA',
                'type': '01',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios'],
                'code': '02',
                'name':  u'PRIVACIDAD DE LOS DATOS',
                'type': '01',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente',
                               'telefono_contacto', 'cups', 'comentarios',
                               'codigo_incidencia'],
                'code': '03',
                'name': u'INCIDENCIA EN EQUIPOS DE MEDIDA',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente',
                               'telefono_contacto', 'cups',
                               'fecha_incidente', 'comentarios',
                               'importe_reclamado'],
                'code': '04',
                'name': u'DAÑOS ORIGINADOS POR EQUIPO DE MEDIDA',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente',
                               'telefono_contacto', 'cups', 'comentarios'],
                'code': '05',
                'name': u'CONTADOR EN FACTURA NO CORRESPONDE CON INSTALADO',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios'],
                'code': '06',
                'name': u'CONTRATOS ATR QUE NO SE FACTURAN',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact'],
                'code': '07',
                'name': u'CUPS NO PERTENECE A COMERCIALIZADORA O NO VIGENTE'
                        u' EN PERIODO DE FACTURA',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact',
                               'tipo_concepto_facturado'],
                'code': '08',
                'name': u'DISCONFORMIDAD CON CONCEPTOS FACTURADOS',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact'],
                'code': '09',
                'name': u'DISCONFORMIDAD CON LECTURA FACTURADA',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact'],
                'code': '10',
                'name': u'DISCONFORMIDAD EN FACTURA ANOMALÍA / FRAUDE',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact'],
                'code': '11',
                'name': u'RECLAMACIÓN FACTURA PAGO DUPLICADO',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact'],
                'code': '12',
                'name': u'REFACTURACION NO RECIBIDA',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'cups', 'comentarios',
                               'codigo_de_solicitud'],
                'code': '13',
                'name': u'DISCONFORMIDAD CON CAMBIO DE SUMINISTRADOR',
                'type': '03',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente',
                               'telefono_contacto', 'cups',
                               'persona_de_contacto', 'cta_banco'],
                'code': '14',
                'name': u'REQUERIMIENTO DE FIANZA / DEPÓSITO DE GARANTÍA',
                'type': '03',
            }),
            ({
                'min_fields': ['cups', 'codigo_de_solicitud'],
                'code': '15',
                'name': u'RETRASO CORTE DE SUMINISTRO',
                'type': '03',
            }),
            ({
                'min_fields': ['cups', 'codigo_de_solicitud'],
                'code': '16',
                'name': u'RETRASO EN PLAZO ACEPTACIÓN',
                'type': '03',
            }),
            ({
                'min_fields': ['cups', 'codigo_de_solicitud'],
                'code': '17',
                'name': u'RETRASO EN PLAZO ACTIVACIÓN',
                'type': '03',
            }),
            ({
                'min_fields': ['nif_cliente', 'comentarios',
                               'sol_nuevos_suministro'],
                'code': '18',
                'name': u'DISCONFORMIDAD CON CRITERIOS ECONÓMICOS / COBROS',
                'type': '04',
            }),
            ({
                'min_fields': ['nif_cliente', 'comentarios',
                               'sol_nuevos_suministro'],
                'code': '19',
                'name': u'DISCONFORMIDAD CON CRITERIOS TÉCNICOS / OBRA '
                        u'EJECUTADA',
                'type': '04',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'fecha_desde',
                               'fecha_hasta'],
                'code': '20',
                'name': u'CALIDAD DE ONDA',
                'type': '05',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'fecha_desde',
                               'fecha_hasta', 'importe_reclamado'],
                'code': '21',
                'name': u'CON PETICIÓN DE INDEMNIZACIÓN',
                'type': '05',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'fecha_desde',
                               'fecha_hasta'],
                'code': '22',
                'name': u'SIN PETICIÓN DE INDEMNIZACIÓN',
                'type': '05',
            }),
            ({
                'min_fields': ['cups', 'comentarios',
                               'cod_reclam_anterior'],
                'code': '23',
                'name': u'RETRASO EN PAGO INDEMNIZACION',
                'type': '05',
            }),
            ({
                'min_fields': ['comentarios', 'persona_de_contacto',
                               'fecha_desde', 'fecha_hasta',
                               'ubicacion_incidencia'],
                'code': '24',
                'name': u'DAÑOS A TERCEROS POR INSTALACIONES',
                'type': '06',
            }),
            ({
                'min_fields': ['telefono_contacto', 'comentarios',
                               'persona_de_contacto', 'fecha_desde',
                               'fecha_hasta'],
                'code': '25',
                'name': u'IMPACTO AMBIENTAL INSTALACIONES',
                'type': '06',
            }),
            ({
                'min_fields': ['comentarios', 'ubicacion_incidencia'],
                'code': '26',
                'name': u'RECLAMACIONES SOBRE INSTALACIONES',
                'type': '06',
            }),
            ({
                'min_fields': ['cups', 'comentarios'],
                'code': '27',
                'name': u'DISCONFORMIDAD DESCUENTO SERVICIO INDIVIDUAL',
                'type': '07',
            }),
            ({
                'min_fields': ['cups', 'comentarios'],
                'code': '28',
                'name': u'EJECUCIÓN INDEBIDA DE CORTE',
                'type': '07',
            }),
            ({
                'min_fields': ['comentarios', 'cod_reclam_anterior'],
                'code': '29',
                'name': u'RETRASO EN LA ATENCIÓN A RECLAMACIONES',
                'type': '07',
            }),
            ({
                'min_fields': ['comentarios', 'sol_nuevos_suministro'],
                'code': '30',
                'name': u'RETRASO PLAZO DE CONTESTACIÓN NUEVOS SUMINISTROS',
                'type': '07',
            }),
            ({
                'min_fields': ['comentarios', 'sol_nuevos_suministro'],
                'code': '31',
                'name': u'RETRASO PLAZO DE EJECUCIÓN NUEVO SUMINISTRO',
                'type': '07',
            }),
            ({
                'min_fields': ['cups', 'comentarios',
                               'codigo_de_solicitud'],
                'code': '32',
                'name': u'RETRASO REENGANCHE TRAS CORTE',
                'type': '07',
            }),
            ({
                'min_fields': ['cups', 'codigo_de_solicitud',
                               'concepto_contratacion'],
                'code': '34',
                'name': u'DISCONFORMIDAD CON CONCEPTOS DE CONTRATACIÓN '
                        u'ATR-PEAJE',
                'type': '03',
            }),
            ({
                'min_fields': ['cups', 'codigo_de_solicitud'],
                'code': '35',
                'name': u'DISCONFORMIDAD RECHAZO SOLICITUD ATR-PEAJE',
                'type': '03',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact', 'lectura',
                               'fecha_de_lectura'],
                'code': '36',
                'name': u'PETICIÓN DE REFACTURACIÓN APORTANDO LECTURA',
                'type': '02',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'num_fact'],
                'code': '37',
                'name': u'FICHERO XML INCORRECTO',
                'type': '02',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios'],
                'code': '38',
                'name': u'PRIVACIDAD DE LOS DATOS',
                'type': '01',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'fecha_desde',
                               'fecha_hasta'],
                'code': '39',
                'name': u'SOLICITUD DE CERTIFICADO / INFORME DE CALIDAD',
                'type': '05',
            }),
            ({
                'min_fields': ['nif_cliente', 'nombre_cliente', 'cups',
                               'comentarios', 'num_fact'],
                'code': '40',
                'name': u'SOLICITUD DE DUPLICADO DE FACTURA',
                'type': '02',
            }),
            ({
                'min_fields': ['telefono_contacto', 'comentarios',
                               'persona_de_contacto',
                               'ubicacion_incidencia'],
                'code': '41',
                'name': u'SOLICITUD DE ACTUACIÓN SOBRE INSTALACIONES',
                'type': '06',
            }),
            ({
                'min_fields': ['nif_cliente', 'telefono_contacto', 'cups',
                               'comentarios', 'persona_de_contacto'],
                'code': '42',
                'name': u'SOLICITUD DE DESCARGO',
                'type': '06',
            }),
            ({
                'min_fields': ['telefono_contacto', 'cups', 'comentarios',
                               'persona_de_contacto'],
                'code': '43',
                'name': u'PETICIÓN DE PRECINTADO / DESPRECINTADO DE '
                        u'EQUIPOS',
                'type': '06',
            }),
            ({
                'min_fields': ['telefono_contacto', 'cups', 'comentarios',
                               'persona_de_contacto'],
                'code': '44',
                'name': u'PETICIONES CON ORIGEN EN CAMPAÑAS DE TELEGESTIÓN',
                'type': '06',
            }),
            ({
                'min_fields': ['cups', 'comentarios'],
                'code': '45',
                'name': u'ACTUALIZACION DIRECCIÓN PUNTO DE SUMINISTRO',
                'type': '03',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'fecha_desde',
                               'fecha_hasta'],
                'code': '46',
                'name': u'CERTIFICADO DE LECTURA',
                'type': '02',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'num_fact'],
                'code': '47',
                'name': u'SOLICITUD RECALCULO CCH SIN MODIFICACION '
                        u'CIERRE ATR',
                'type': '02',
            }),
            ({
                'min_fields': ['cups', 'comentarios',
                               'codigo_de_solicitud'],
                'code': '48',
                'name': u'PETICIÓN INFORMACIÓN ADICIONAL RECHAZO',
                'type': '03',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'fecha_desde',
                               'fecha_hasta'],
                'code': '49',
                'name': u'FALTA FICHERO MEDIDA',
                'type': '02',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'num_fact'],
                'code': '55',
                'name': u'DISCONFORMIDAD SOBRE IMPORTE FACTURADO '
                        u'AUTOCONSUMO',
                'type': '02',
            }),
            ({
                'min_fields': ['cups', 'comentarios', 'num_fact'],
                'code': '56',
                'name': u'PETICIÓN DESGLOSE IMPORTE A FACTURAR AUTOCONSUMO',
                'type': '02',
            }),
        ]

TABLA_82 = [(x['code'], x['name']) for x in SUBTYPES_R101]
