# Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import unicodedata
from unidecode import unidecode
import seaborn as sns
import geopandas as gpd

# Leer el dataset
df = pd.read_csv(r'F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\raw\Dataset Historico\dnrpa-robos-recuperos-autos-historico.csv', sep=',', 
    low_memory=False)

# Ver el tamaño
#print(df.shape)

# Revisar qué columnas hay
#print(df.columns)

# Info general (nulos, tipos de datos, etc.)
#print(df.info())

# Cantidad de valores nulos por columna
#print(df.isnull().sum())

# Nulos por columna
#print(df.isnull().sum())

# Estas columnas las vamos a eliminar
columnas_a_eliminar = [
    'registro_seccional_codigo',
    'automotor_tipo_codigo',
    'automotor_marca_codigo',
    'automotor_modelo_codigo',
    'automotor_uso_codigo',
    'automotor_uso_descripcion',
    'titular_porcentaje_titularidad',
    'titular_domicilio_provincia_indec_id',
    'titular_pais_nacimiento_indec_id',
    'titular_domicilio_provincia_id',
    'titular_pais_nacimiento_id'
]

# Eliminamos esas columnas
df = df.drop(columns=columnas_a_eliminar)

#print(df.head())

# Nulos por columna
#print(df.isnull().sum())

# Eliminamos filas con nulos
df_clean = df.dropna()

# Verificamos nuevamente los nulos
#print(df_clean.isnull().sum())
#print(f"Nuevo tamaño del dataset: {df_clean.shape}")

# Guardamos el dataset limpio
df_clean.to_csv(r'F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\processed\dnrpa-robos-limpio.csv', index=False)

# 1. Leer el dataset
df_clean = pd.read_csv(r'F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\processed\dnrpa-robos-limpio.csv')

# 2. Convertir columnas de fecha a tipo datetime
df_clean['tramite_fecha'] = pd.to_datetime(df_clean['tramite_fecha'], errors='coerce')
df_clean['fecha_inscripcion_inicial'] = pd.to_datetime(df_clean['fecha_inscripcion_inicial'], errors='coerce')

# 3. Crear columnas de año y mes
df_clean['tramite_anio'] = df_clean['tramite_fecha'].dt.year
df_clean['tramite_mes'] = df_clean['tramite_fecha'].dt.month
df_clean['inscripcion_anio'] = df_clean['fecha_inscripcion_inicial'].dt.year
df_clean['inscripcion_mes'] = df_clean['fecha_inscripcion_inicial'].dt.month

# 4. Verificamos
#print(df_clean[['tramite_fecha', 'tramite_anio', 'tramite_mes', 
#                'fecha_inscripcion_inicial', 'inscripcion_anio', 'inscripcion_mes']].head())

# Verificar que la conversión fue bien
#print(df_clean[['tramite_fecha', 'tramite_anio', 'tramite_mes' ,'fecha_inscripcion_inicial', 'inscripcion_anio', 'inscripcion_mes']].dtypes)

def corregir_marcas(df, columna):

    marcas = df[columna].str.upper().str.strip()  # Convertir a mayúsculas y eliminar espacios

    # Diccionario de correcciones
    correcciones = {
        'VOLKSWGEN': 'VOLKSWAGEN',
        'VOLSKWAGEN': 'VOLKSWAGEN',
        'VOLKSWAGN': 'VOLKSWAGEN',
        'VOLKSWAGEN (136)': 'VOLKSWAGEN',
        'VOLKSWAGEN/MARCOPOLO': 'VOLKSWAGEN',
        'EGA098VOLKSWAGEN': 'VOLKSWAGEN',
        'VOLKSWGAEN': 'VOLKSWAGEN',
        'VOLKWAGEN': 'VOLKSWAGEN',
        'VOKKSWAGEN': 'VOLKSWAGEN',
        'VOKSWAGEN': 'VOLKSWAGEN',
        'VOLSWAGEN': 'VOLKSWAGEN',
        'VOLKSWAGENVOLKSWAGEN': 'VOLKSWAGEN',
        'VOLKSAWGEN': 'VOLKSWAGEN',
        'VOLKSWWAGEN': 'VOLKSWAGEN',
        'VLOKSWAGEN': 'VOLKSWAGEN',
        'VOLKSWAGEN G': 'VOLKSWAGEN',
        'VOLKSWAGUEN': 'VOLKSWAGEN',
        'VOLKSWAAGEN': 'VOLKSWAGEN',
        'VOLKSWAFGEN': 'VOLKSWAGEN',
        'VOLKSAGEN': 'VOLKSWAGEN',
        'VOLKDWAGEN': 'VOLKSWAGEN',
        '-VOLKSWAGEN': 'VOLKSWAGEN',
        'WOLKSWAGEN': 'VOLKSWAGEN',
        '-136-VOLKSWAGEN': 'VOLKSWAGEN',
        '-136- VOLKSWAGEN': 'VOLKSWAGEN',
        'MERCEDES-BENZ': 'MERCEDES BENZ',
        'M. BENZ': 'MERCEDES BENZ',
        'MERCEDEZ BENZ': 'MERCEDES BENZ',
        'M.BENZ': 'MERCEDES BENZ',
        'MERCERDES BENZ': 'MERCEDES BENZ',
        'MERCEDES BENZ/COMIL': 'MERCEDES BENZ',
        '-092-MERCEDES BENZ': 'MERCEDES BENZ',
        'REANULT': 'RENAULT',
        'RANAULT': 'RENAULT',
        'RENUALT': 'RENAULT',
        'R E N A U L T': 'RENAULT',
        'RENAULT \(112\)': 'RENAULT',
        '-112- RENAULT': 'RENAULT',
        '-112-RENAULT': 'RENAULT',
        'RENAUL': 'RENAULT',
        'RENAULT R': 'RENAULT',
        'RENAULT \(033\)': 'RENAULT',
        'REANUT': 'RENAULT',
        'CHEROLET': 'CHEVROLET',
        'CHEVROELT': 'CHEVROLET',
        'CHEVRVOLET': 'CHEVROLET',
        'CHEVROLET \(024\)': 'CHEVROLET',
        '\.CHEVROLET': 'CHEVROLET',
        '-024-CHEVROLET': 'CHEVROLET',
        '-024- CHEVROLET': 'CHEVROLET',
        'FIAR': 'FIAT',
        'FIAT.': 'FIAT',
        'FIAT \(044\)': 'FIAT',
        '044 FIAT': 'FIAT',
        '-044-FIAT': 'FIAT',
        'FIAT3': 'FIAT',
        '-044- FIAT': 'FIAT',
        'FIAT AUTO ARGENTINA S.A': 'FIAT',
        'FIAT IVECO': 'FIAT',
        '\.PEUGEOT': 'PEUGEOT',
        'PEOGEOT': 'PEUGEOT',
        'PEUIGEOT': 'PEUGEOT',
        'PEUGET': 'PEUGEOT',
        'PEUGROT': 'PEUGEOT',
        'PUEGEOT': 'PEUGEOT',
        'OEUGEOT': 'PEUGEOT',
        '3PEUGEOT': 'PEUGEOT',
        'PEUGEOT \(039\)': 'PEUGEOT',
        '-104-PEUGEOT': 'PEUGEOT',
        'PEUGEOT 306 XRD': 'PEUGEOT',
        'ALFA ROMERO': 'ALFA ROMEO',
        'ALFA ROEMO': 'ALFA ROMEO',
        'SSANYONG': 'SSANGYONG',
        'SANGYONG': 'SSANGYONG',
        'CITROËN': 'CITROEN',
        'CITRÖEN': 'CITROEN',
        'FORS': 'FORD',
        'FORD \(047\)': 'FORD',
        '047-FORD': 'FORD',
        '-047- FORD': 'FORD',
        'FORD FALCON': 'FORD',
        'FORD F-100 XLT': 'FORD',
        '19 - FORD': 'FORD',
        'B M W': 'BMW',
        'B.M.W.': 'BMW',
        'G.M.C.': 'GMC',
        'VW': 'VOLKSWAGEN',
        'M. BENZ': 'MERCEDES BENZ',
        'CHEVETTE': 'CHEVROLET',
        'SUZUKI SWIFT SEDAN NLX': 'SUZUKI',
        'GMC CHEVETTE': 'GMC',
        '-130- TOYOTA': 'TOYOTA',
        'SUZUKI CARRY': 'SUZUKI',
        'DEUTZ - AGRALE': 'DEUTZ',
        'GMC CHEVROLET': 'GMC',
        'PICK UP': 'NO DEFINIDO',
        '-058-HYUNDAI': 'HYUNDAI',
        'GENERAL MOTORS': 'GMC',
        '-102-NISSAN': 'NISSAN',
        'CIADEA SA': 'CIADEA',
        'JEEP ESTANCIERA': 'JEEP',
        'VW': 'VOLKSWAGEN',
        'SUZUKI SWIFT SEDAN GLX': 'SUZUKI',
        'NISSAN DIESEL': 'NISSAN',
        'GMC  CHEVETTE': 'GMC',
        'RASTROJERO DIESEL': 'RASTROJERO',
        'NO POSEE': 'NO DEFINIDO',
        'KIA MOTORS': 'KIA',
        'NAVATUC NT': 'NAVATUC',
        'SUZUKI SWIFT GTI': 'SUZUKI',
        'RENAULT (112)': 'RENAULT',
        'BELGRANO MET.BEL.SRL': 'BELGRANO',
        '.TOYOTA': 'TOYOTA',
        'A.F.F.': 'AFF',
        'FIAT (044)': 'FIAT',
        '127 SUZUKI': 'SUZUKI',
        'SUZUKI SWIFT SEDAN NL': 'SUZUKI',
        'NO CONSTA': 'NO DEFINIDO',
        'GMC 500': 'GMC',
        'FORD (047)': 'FORD',
        'SAAB SCANIA': 'SCANIA',
        'TOYOTA (030)': 'TOYOTA',
        '-072-KIA': 'KIA',
        '69 - BONANO': 'BONANO',
        'CHEVROET': 'CHEVROLET',
        'FORD ARGENTINA S. C. A.': 'FORD',
        '-047-FORD': 'FORD',
        'NISSAN PATHFINDER': 'NISSAN',
        'DODGE/CHRYSLER': 'CHRYSLER-DODGE',
        'CHRYSLER DODGE': 'CHRYSLER-DODGE',
        'DODGE': 'CHRYSLER-DODGE',
        'RENAULT                      R': 'RENAULT',
        'PEUGEOT (039)': 'PEUGEOT',
        'DEUTZ AGRALE': 'DEUTZ',
        'DEUTZ-AGRALE': 'DEUTZ',
        'AGRALE': 'DEUTZ',
        'RAM': 'CHRYSLER-DODGE',
        '.PEUGEOT': 'PEUGEOT',
        'CARROCERIAS APEZ': 'APEZ',
        'RAMBLER IKA': 'RAMBLER-IKA',
        '19': 'NO DEFINIDO',
        'MERDECES BENZ': 'MERCEDES BENZ',
        'SUZUKI VITARA': 'SUZUKI',
        '-032-DAIHATSU': 'DAIHATSU',
        'CHEVROLET (024)': 'CHEVROLET',
        'SIN MARCA REGISTRADA': 'NO DEFINIDO',
        '.CHEVROLET': 'CHEVROLET',
        'SIN MARCA': 'NO DEFINIDO',
        '37 - RENAULT': 'RENAULT',
        'SIN IDENTIFICACION': 'NO DEFINIDO',
        'SIN ESPECIFICACION': 'NO DEFINIDO',
        'VOLKSWAGEN         G': 'VOLKSWAGEN',
        'CHERVROLET': 'CHEVROLET',
        'GENERAL MOTORS ARGENTINA S. R.  L.': 'GMC',
        'CHEVETTE': 'GMC',
        'CHEVROLET LUMINA APV': 'CHEVROLET',
        'RENAUTL': 'RENAULT',
        'MERCEDES BENZ.': 'MERCEDES BENZ',
        'GMC CHEVETTE (GENERAL MOTORS CORPORATION)': 'GMC',
        'G.M.C. CHEVETTE': 'GMC',
        'GMC (GENERAL MOTORS CORPORATION)': 'GMC',
        'G.MOTORS': 'GMC',
        'RENAULT (033)': 'RENAULT',
        'VOLKSWGAGEN': 'VOLKSWAGEN',
        'MARCA   INVALIDA': 'NO DEFINIDO',
        '*': 'NO DEFINIDO',
        'DUNA W.E. 1.6': 'FIAT',
        'VW (VOLKSWAGEN)': 'VOLKSWAGEN',

    }

    # Aplicar correcciones
    marcas_corregidas = marcas.replace(correcciones)

    return marcas_corregidas

# Aplicar la función y actualizar la columna
df_clean['automotor_marca_descripcion'] = corregir_marcas(df_clean, 'automotor_marca_descripcion')

def agrupar_tipo_vehiculo(df, columna):

    marcas = df[columna].str.upper().str.strip()  # Convertir a mayúsculas y eliminar espacios

    # Diccionario de correcciones
    correcciones = {
        #'': 'SEDAN',
        #'': 'RURAL',
        #'': 'PICK-UP',
        #'': 'FURGON',
        #'': 'COUPE',
        #'': 'TODOTERRENO',
        #'': 'CHASIS CON CABINA',
        #'': 'CHASIS SIN CABINA',
        #'': 'TRACTOR',
        #'': 'MINIBUS',
        #'': 'UTILITARIO',
        #'': 'OMNIBUS',
        #'': 'LIMUSINA',
        #'': 'CAMION',
        #'': 'CASA RODANTE',
        #'': 'ACOPLADO',
        #'': 'GRUA',
        #'': 'MOTORHOME',
        #'': 'CABRIOLET',
        #'': 'TREN',
        #'': 'NO DEFINIDO',
        'SEDAN 5 PTAS': 'SEDAN',
        'SEDAN 5 PUERTAS': 'SEDAN',
        'SEDAN 4 PTAS': 'SEDAN',
        'SEDAN 4 PUERTAS': 'SEDAN',
        'SEDAN 3 PTAS': 'SEDAN',
        'SEDAN 3 PUERTAS': 'SEDAN',
        'RURAL 5 PTAS': 'RURAL',
        'RURAL 5 PUERTAS': 'RURAL',
        'TODO TERRENO': 'TODOTERRENO',
        'FURGONETA': 'FURGON',
        'PICK UP': 'PICK-UP',
        'SEDAN 2 PTAS': 'SEDAN',
        'PICK-UP CABINA DOBLE': 'PICK-UP',
        'FAMILIAR': 'RURAL',
        'CHASIS C/CABINA': 'CHASIS CON CABINA',
        'SEDAN 2 PUERTAS': 'SEDAN',
        'FURGON VIDRIADO C/ASIENTOS': 'FURGON',
        'SIN ESPECIFICACION': 'NO DEFINIDO',
        'TRACTOR DE CARRETERA': 'TRACTOR',
        'FURGON 600': 'FURGON',
        'SEMIRREMOLQUE': 'ACOPLADO',
        'FURGON VIDRIADO': 'FURGON',
        'FURGON VIDRIADO CON ASIENTOS': 'FURGON',
        'BERLINA 5 PTAS': 'SEDAN',
        'BERLINA 5 PUERTAS': 'SEDAN',
        'FURGON VIDRIADO C/ ASIENTOS': 'FURGON',
        'TRANSP. DE PASAJEROS': 'UTILITARIO',
        'PICK-UP CABINA SIMPLE': 'PICK-UP',
        'MINIBUS': 'MINIBUS',
        'TRACTOR C/CABINA DORMITORIO': 'TRACTOR',
        'FURGON 800': 'FURGON',
        'CHASIS CON CABINA': 'CHASIS CON CABINA',
        'RURAL 4/5 PTAS' : 'RURAL',
        'CAMION': 'CAMION',
        'FURGON VIDRIADO C/AS': 'FURGON',
        'RURAL 3 PTAS' : 'RURAL',
        'AUTOMOVIL': 'SEDAN',
        'PICK-UP CABINA Y MEDIA': 'PICK-UP',
        'BERLINA 4 PTAS': 'SEDAN',
        'PICK-UP CABINA SIMPL': 'PICK-UP',
        'RURAL 3 PUERTAS' : 'RURAL',
        'BERLINA 5 PTAS.': 'SEDAN',
        'ACOPLADO': 'ACOPLADO',
        'RURAL 4 PUERTAS' : 'RURAL',
        'RURAL 4/5 PUERTAS' : 'RURAL',
        'DESCAPOTABLE': 'CABRIOLET',
        'BERLINA 3 PTAS': 'SEDAN',
        'PICK-UP CABINA Y MED': 'PICK-UP',
        'BERLINA 4 PUERTAS': 'SEDAN',
        'FOURGON COURT TYPE 600': 'FURGON',
        'FURGON 3000': 'FURGON',
        'FURGON VID C/ASIENTOS': 'FURGON',
        'TRACTOR C/ CABINA DORMITORIO': 'TRACTOR',
        'BERLINA 3 PUERTAS': 'SEDAN',
        'FOURGON COURT TYPE 6': 'FURGON',
        'FURGON VID. C/ASIENTOS': 'FURGON',
        'RURAL 2/3 PTAS' : 'RURAL',
        'CHASIS CON CABINA DORMITORIO': 'CHASIS CON CABINA',
        'FURGON VID.C/ASIENTOS': 'FURGON',
        'RURAL': 'RURAL',
        'RURAL 4 PTAS' : 'RURAL',
        'TRANS.DE PASAJEROS': 'UTILITARIO',
        'CHASIS C/CABINA DORMITORIO': 'CHASIS CON CABINA',
        'TRACTOR C/CABINA DOR': 'TRACTOR',
        'COUPE 2 PUERTAS': 'COUPE',
        'MIDIBUS': 'MINIBUS',
        'FURGON 3550': 'FURGON',
        'BERLINA': 'SEDAN',
        'SEDAN 4 PTAS.': 'SEDAN',
        'COMBI 3550': 'UTILITARIO',
        'BERLINA 4 PTAS.': 'SEDAN',
        'CAMIONETA': 'PICK-UP',
        'FURGONETA VIDRIADA': 'FURGON',
        'TRANSPORTE DE CARGA': 'CAMION',
        'S.WAGON': 'RURAL',
        'BERLINA 3 PTAS.': 'SEDAN',
        'FURGON VID C/ASIENTO': 'FURGON',
        'AMBULANCIA': 'UTILITARIO',
        'FURGON VID.C/ASIENTO': 'FURGON',
        '3 PTAS': 'SEDAN',
        'CHASIS C/CABINA P/CAMION': 'CHASIS CON CABINA',
        'AUTOMOTOR': 'SEDAN',
        'MINIBUS (O MICROOMNIBUS)' : 'MINIBUS',
        'FURGON LARGO': 'FURGON',
        'FURGON VID C/ ASIENTOS': 'FURGON',
        'SEDAN 5 PTAS.': 'SEDAN',
        'FURGON COURT TYPE 600': 'FURGON',
        'FURGON COURT TYPE 60': 'FURGON',
        'JEEP': 'TODOTERRENO',
        'BREAK': 'RURAL',
        'CHASIS C/ CABINA': 'CHASIS CON CABINA',
        'CAMION TRACTOR': 'CAMION',
        'TRANSPORTE DE PASAJEROS': 'UTILITARIO',
        'FURGON TERMICO': 'FURGON',
        'FURGON CON ASIENTOS': 'FURGON',
        'CONVERTIBLE': 'CABRIOLET',
        'STATION WAGON': 'RURAL',
        'MICROOMNIBUS': 'MINIBUS',
        'FURGON VIDR C/ASIENTOS': 'FURGON',
        'FURGON VIDRIADO C/A': 'FURGON',
        'S. WAGON': 'RURAL',
        'FURGON VIDRIADO C/ASIENTO': 'FURGON',
        'CHASIS C/ CABINA DOR': 'CHASIS CON CABINA',
        'FURGON VID. C/ ASIENTOS': 'FURGON',
        'CHASIS C/CABINA P/CA': 'CHASIS CON CABINA',
        'DEPORTIVO 3 PUERTAS': 'COUPE',
        'BREAK 4 PUERTAS': 'RURAL',
        'FURGON VIDR.C/ASIENTOS': 'FURGON',
        'FURGON VIDRIADO C/ASI': 'FURGON',
        'UNIDAD TRACTORA': 'TRACTOR',
        'SEDAN 3 PTAS.': 'SEDAN',
        'SEDAN 3 PUERTAS CON PORTON': 'SEDAN',
        'TRANSPORTE ESCOLAR': 'UTILITARIO',
        'OMNIBUS': 'OMNIBUS',
        'FURGON VIDRIADO CON ASIENTO': 'FURGON',
        'FURGON VIDR. C/ASIENTOS': 'FURGON',
        'FAMILIAR 5 ASIENTOS': 'SEDAN',
        'FURGON VIDR.C/ASIENT': 'FURGON',
        'PICK UP CABINA DOBLE': 'PICK-UP',
        'OTROS': 'NO DEFINIDO',
        'FURGÓN VIDRIADO C/ASIENTOS': 'FURGON',
        'SEMIRREMOLQUE BATEA': 'ACOPLADO',
        'FURGON FAMILIAR': 'FURGON',
        'FURGON 4P': 'FURGON',
        'SEDAN 5 P': 'SEDAN',
        'FURG.VIDRIADO C/ASIENTOS': 'FURGON',
        'COUPE 3 PUERTAS': 'COUPE',
        'ARENERO': 'TODOTERRENO',
        'JEEP CARROZADO': 'TODOTERRENO',
        'OTROS AUTOMOVILES': 'NO DEFINIDO',
        'CHASIS S/CABINA': 'CHASIS SIN CABINA',
        'FAMILIAR 5 PUERTAS': 'SEDAN',
        'SEDAN 4 P': 'SEDAN',
        'S. 5 PTAS.': 'SEDAN',
        '3 PUERTAS': 'SEDAN',
        'FURGON VIDRIADO CON': 'FURGON',
        'FURGON C/ASIENTOS': 'FURGON',
        'TRANS. DE PASAJEROS': 'UTILITARIO',
        'BERLINA 3PTAS': 'SEDAN',
        'SEDAN 2 PTAS.': 'SEDAN',
        '12 - SEDAN 4 PUERTAS': 'SEDAN',
        'TRACTOR': 'TRACTOR',
        'CHASSIS C/CABINA': 'CHASIS CON CABINA',
        'FURGONETA VID C/ASIENTOS': 'FURGON',
        'RURAL 3 PTAS.': 'RURAL',
        'FURGONETA O UTILITAR': 'FURGON',
        'SEMIACOPLADO': 'ACOPLADO',
        'COUPE 2 PTAS': 'COUPE',
        '5 PTAS': 'SEDAN',
        'LIMUSINA': 'LIMUSINA',
        'CAMION PORTA VOLQUETE': 'CAMION',
        'SEDAN NAFTERO': 'SEDAN',
        'CAMION MEDIANO': 'CAMION',
        'FURGON  600': 'FURGON',
        'FURGON VID. CON ASIENTOS': 'FURGON',
        'FURGON VIDR C/ ASIENTOS': 'FURGON',
        'SEDAN 5 PTS': 'SEDAN',
        'SEMIREMOLQUE': 'ACOPLADO',
        'CHASIS C/ CABINA DORMITORIO': 'CHASIS CON CABINA',
        'SEDAN 5  PUERTAS': 'SEDAN',
        'SEMIRREMOLQUE TANQUE': 'ACOPLADO',
        'MOTORHOME': 'MOTORHOME',
        'SEMI-ACOPLADO': 'ACOPLADO',
        'BERLINE 5 PORTES': 'SEDAN',
        'FURGON VIDRIADO C/ AS': 'FURGON',
        'FURGONETA VID. C/ASIENTOS': 'FURGON',
        'SEDAN 4 PTS': 'SEDAN',
        'BERLINA 5PTAS': 'SEDAN',
        'FURGON VID C/AS': 'FURGON',
        'FURGONETA VIDR C/ASIENTOS': 'FURGON',
        'COMBI 3000': 'UTILITARIO',
        'CASA RODANTE': 'CASA RODANTE',
        'FURGON VIDRIADO C/ASIEN': 'FURGON',
        'FURGON VIDRIAD C/ASIENTOS': 'FURGON',
        'PICK-UP C/CAJA MUDANCERA': 'PICK-UP',
        'FURGONETA O UTILITARIO': 'FURGON',
        'VAN': 'RURAL',
        'PICK - UP': 'PICK-UP',
        'MICROBUS': 'MINIBUS',
        'FURGON VID. C/ASIENT': 'FURGON',
        '5 PUERTAS': 'SEDAN',
        'CAMION VOLCADOR': 'CAMION',
        '4 (CUATRO) PUERTAS': 'SEDAN',
        'CHASIS C/CAB C/CAJA ABIERTA': 'CHASIS CON CABINA',
        'RURAL 4X4' : 'RURAL',
        'BERLINA 3TAS.AA': 'SEDAN',
        'FURGON PAQUETERO': 'FURGON',
        'SEDAN 4 PUERTAS.': 'SEDAN',
        'BERLINA 3PT.AA': 'SEDAN',
        'RURAL 2 PUERTAS': 'RURAL',
        'CH.CABINA 3550': 'CHASIS CON CABINA',
        'COMBI': 'UTILITARIO',
        'CAMION CON CAJA ABIERTA': 'CAMION',
        'AUTO': 'SEDAN',
        'FURGON  VIDRIADO C/ASIENTOS': 'FURGON',
        'FURGONETA VID.C/ASIENTOS': 'FURGON',
        'FOURGON C.TYPE 600': 'FURGON',
        'FURGON 4 PUERTAS': 'FURGON',
        'SEDAN  3 PUERTAS': 'SEDAN',
        'FURGONETA VIDRIADA C/ASIENT': 'FURGON',
        'SEDAN  4 PUERTAS': 'SEDAN',
        'CHASIS CON CABINA P/CAMION': 'CHASIS CON CABINA',
        'SEDAN 5P'  : 'SEDAN',
        'CAMION PORTAVOLQUETE': 'CAMION',
        'FURGONETA VIDRIADA C/ASI': 'FURGON',
        'BERLINA  5 PUERTAS': 'SEDAN',
        'CHASIS C/CABINA C/CAJA PLAYA': 'CHASIS CON CABINA',
        'FURGON  VIDRIADO': 'FURGON',
        'COUPE 2 PTAS.': 'COUPE',
        'SEDAN 3 P': 'SEDAN',
        'SEDAN 5 P.': 'SEDAN',
        'FURGONETA VIDRIADA C/AS': 'FURGON',
        'SEDAN 4PTAS': 'SEDAN',
        'PICK-UP CON CAJA MUDANCERA': 'PICK-UP',
        'CASA RODANTE C/MOTOR': 'CASA RODANTE',
        'FURGONETA VIDRIADA C/ASIENTO': 'FURGON',
        'VEHICULO UTILITARIO 4X4 5 PU': 'UTILITARIO',
        'FURGON VID C/ASIEN': 'FURGON',
        'FURGON COURT TYPE600': 'FURGON',
        '5 PTAS.': 'SEDAN',
        'BERLINA 3 PT AA': 'SEDAN',
        'SEDAN 4  PUERTAS': 'SEDAN',
        'BERLINA 3PTAS.': 'SEDAN',
        'S. 3 PTAS.': 'SEDAN',
        'PICK-UP C/ CAJA MUDANCERA': 'PICK-UP',
        'SEMI ACOPLADO': 'ACOPLADO',
        'CAJA ABIERTA': 'CHASIS CON CABINA',
        'BERLINA 5PTAS.': 'SEDAN',
        'FURGON VIDRIADO C/ ASIENTO': 'FURGON',
        'FURGO': 'FURGON',
        '4 PUERTAS': 'SEDAN',
        'SEDAN 3 PTAS.-': 'SEDAN',
        'FURG.VIDRIADO C/ASIE': 'FURGON',
        'FGON.VID.C/ASIENTOS': 'FURGON',
        'FURGON VIDRI C/ASIEN': 'FURGON',
        'RURAL 5 PUERTAS.': 'RURAL',
        'FURGON VIDRIADO C ASIENTOS': 'FURGON',
        'FURGON VIDR. C/ ASIENTOS': 'FURGON',
        'FURGÓN': 'FURGON',
        'FURGONETA CON ASIENTOS': 'FURGON',
        'FURGON TERMICO C/EQ DE FRIO': 'FURGON',
        'MINI BUS': 'MINIBUS',
        'PICK UP CABINA Y MED': 'PICK-UP',
        'FURGON VIDR C/ASIENT': 'FURGON',
        'CHASIS C/CAB C/CAJA CERRADA': 'CHASIS CON CABINA',
        'FURGON VID/ CON ASIENTOS': 'FURGON',
        'FURGON VID CON ASIENTOS': 'FURGON',
        'FURGON C/ ASIENTOS' : 'FURGON',
        'FURGON VIDRIADO C/ A': 'FURGON',
        'FURGON VID.CON ASIENTOS': 'FURGON',
        'CAMION GRUA': 'CAMION',
        'FURG.VIDR.C/ASIENTOS': 'FURGON',
        'RURAL 5 PTAS.': 'RURAL',
        'CHASIS C/CAB C/CAJA': 'CHASIS CON CABINA',
        'CHASIS C/CAB.P/CAMIO': 'CHASIS CON CABINA',
        'furgon vidriado': 'FURGON',
        'FURGON VIDRIADO C/ASIENT': 'FURGON',
        'FURGON CON EQUIPO DE FRIO': 'FURGON',
        'FURGON VIDRIADO C/ AS.': 'FURGON',
        'FURGON VIDRI C/ASIENTOS': 'FURGON',
        'CAJA CERRADA': 'CHASIS CON CABINA',
        'FURGON VIDRIADA': 'FURGON',
        'FURGONETA VID. C/ ASIENTOS': 'FURGON',
        'CHASIS C/CAB. C/CAJA PLAYA': 'CHASIS CON CABINA',
        'FURGON VID.C/ ASIENTOS': 'FURGON',
        'FURGON VID/CON ASIENTOS': 'FURGON',
        'SEDÁN 4 PUERTAS': 'SEDAN',
        'SEDÁN 3 PUERTAS': 'SEDAN',
        'CAMION CAMILLA': 'CAMION',
        'FURG VID C/ASIENTOS': 'FURGON',
        'S WAGON': 'RURAL',
        'PICK-UP CARROZADA': 'PICK-UP',
        '3 PTAS.': 'SEDAN',
        'FURGÓN VIDRIADO C/ ASIENTOS': 'FURGON',
        '17 - SEDAN 5 PUERTAS': 'SEDAN',
        'SEDAN KPGL': 'SEDAN',
        'SEDAN 5': 'SEDAN',
        'SED. 4 PTAS': 'SEDAN',
        'CASA RODANTE CON MOTOR': 'CASA RODANTE',
        'T TERRENO': 'TODOTERRENO',
        'FURGON VIDRIADO C/ASIE TRAS': 'FURGON',
        'AUTOMOVIL 4 PTAS': 'SEDAN',
        'VIDRIADO CON ASIENTO': 'FURGON',
        'SEDAN  5 PUERTAS': 'SEDAN',
        'FURGON  C/ ASIENTOS': 'FURGON',
        'SEDAN 3': 'SEDAN',
        'FURGON V/C.ASIENTOS': 'FURGON',
        'TCA CAJA ABIERTA': 'CHASIS CON CABINA',
        'FURG VIDRIADO C/ASIENTOS': 'FURGON',
        'CAMION TRACT C/CAB DORM': 'CAMION',
        'SEDAN 4 PTAS Y TRASE': 'SEDAN',
        '4 PTAS.': 'SEDAN',
        'FURGON VIDRIADO C/ ASIENT': 'FURGON',
        'CAJA TERMICA': 'CHASIS CON CABINA',
        'FURGON TERMICO C/EQU': 'FURGON',
        'FURGON VIDRIADO S/ ASIENTOS': 'FURGON',
        'SEDAN 3PUERTAS': 'SEDAN',
        'S 5 PUERTAS': 'SEDAN',
        'FURGONETA VIDRIADA C/ ASIENT': 'FURGON',
        'CAMION PLAYO': 'CAMION',
        'CAMION CON CAJA METALICA': 'CAMION',
        'BERLINA 3 PUERTAS AA': 'SEDAN',
        'CAMION C/CAJA VOLCADORA': 'CAMION',
        'FURG/VIDRIADO/ASIENT': 'FURGON',
        'furgon vidriado c/as' : 'FURGON',
        'R. 5 PTAS.': 'RURAL',
        'CHASIS C/CAB.P/CAMION': 'CHASIS CON CABINA',
        'SEMIRREMOLQUE PLAYO': 'ACOPLADO',
        'PICK UP C/FURGON TER': 'PICK-UP',
        'FURG.VID.C/ASIENTOS': 'FURGON',
        'PICK-UP 3550': 'PICK-UP',
        'ACOPLADO BARANDA VOLCABLE': 'ACOPLADO',
        'PICK UP C/C': 'PICK-UP',
        'CAMION COMPACT. DE BASURA': 'CAMION',
        'FURGON VIDRIAD C/ASIENTO': 'FURGON',
        'PLATAFORMA PORTA VEHICULOS': 'ACOPLADO',
        'RURAL NAFTERO': 'RURAL',
        'FOURGON COURT T. 600': 'FURGON',
        'SEDA 5 PUERTAS': 'SEDAN',
        'FURGON CERRADO': 'FURGON',
        'FURGON VIDRIA C/ASIE': 'FURGON',
        'FURGON VIDR C/ASIENTO': 'FURGON',
        'SEDÁN 5 PUERTAS': 'SEDAN',
        'CAMION HORMIGONERO': 'CAMION',
        'CHASIS C/CAB. P/CAMION': 'CHASIS CON CABINA',
        'CHASIS C/CAB C/CAM HIDR': 'CHASIS CON CABINA',
        'FURGON 4 PTAS.': 'FURGON',
        'CASA RODANTE AUTOPROPULSADA': 'CASA RODANTE',
        'RURAL 4 PTAS.': 'RURAL',
        'FURGON VIDRIA C/ASIENTOS': 'FURGON',
        'FURGON VIDR. C/ASIEN': 'FURGON',
        'BERLINA 3 PTAS. AA': 'SEDAN',
        'FURGON VID.C/ASIENT.': 'FURGON',
        'FURGON TERMICO E.FRI': 'FURGON',
        'PICK-UP D.A.': 'PICK-UP',
        'FURGONETA VID C/ASIE': 'FURGON',
        'PICK UP 2 PUERTAS': 'PICK-UP',
        'FURGONETA VIDR.C/ASI': 'FURGON',
        'PICK UP 3550': 'PICK-UP',
        'SEMIRREMOL BARANDA VOLCABLE': 'ACOPLADO',
        'FURGON C/EQUIPO DE FRIO': 'FURGON',
        'RURAL 5 P': 'RURAL',
        'FURGON VIDR C/AS': 'FURGON',
        'FURGONETA C/ASIENTOS': 'FURGON',
        'FAMILIAR 5 PTAS': 'SEDAN',
        'TTE. DE CARGA': 'CAMION',
        'FURGON VIDRIADA C/ASIENTOS': 'FURGON',
        'FURGONETA VIDRIAD C/ASIENTOS': 'FURGON',
        'CARRETON': 'UTILITARIO',
        'FURGON VIDIRADO C/ASIENTOS': 'FURGON',
        'BERLINA  5 PTAS': 'SEDAN',
        'S. 5 P.': 'SEDAN',
        'CAMION CON CAJA CERRADA': 'CAMION',
        'CHASSIS CON CABINA': 'CHASIS CON CABINA',
        'PLATAF. HIDRAULICA': 'ACOPLADO',
        'FURGONETA VIDR. C/ASIENTOS': 'FURGON',
        'FURGON VID C/ ASIENT': 'FURGON',
        'SEDAN 3  PUERTAS': 'SEDAN',
        'CHASIS C/CAB.C/CAJA': 'CHASIS CON CABINA',
        'PICKUP': 'PICK-UP',
        'CHASIS P/CAMION': 'CHASIS SIN CABINA',
        'SEDAN KPR8': 'SEDAN',
        'AUTOMOVIL FURGON 4 PUERTAS': 'FURGON',
        'RURAL 2 PTAS': 'RURAL',
        'KOMBI': 'UTILITARIO',
        'TRACTOR CON CABINA D': 'TRACTOR',
        'SEDAN 2PUERTAS': 'SEDAN',
        'CAJA PAQUETERA': 'UTILITARIO',
        'SEMIREMOLQUE TANQUE': 'ACOPLADO',
        'FURGONETA VID C/ ASIENTOS': 'FURGON',
        'CHASIS C/CABINA C/CAJA CARGA': 'CHASIS CON CABINA',
        'SEDAN 5PTAS': 'SEDAN',
        'AUTOMOVIL 4 PUERTAS': 'SEDAN',
        'CAJA PLAYA C/HIDROGRUA': 'GRUA', 
        'SEDAN 4 PURTAS': 'SEDAN',
        'FURGONETA VIDRIADO C': 'FURGON',
        'SEDAN 4P': 'SEDAN',
        'FURGON VIDRIAD C/ASI': 'FURGON',
        'CONVERTIBLE 2 PUERTAS': 'CABRIOLET',
        'CHASIS C/CAB. C/ CAJA PLAYA': 'CHASIS CON CABINA',
        'TRACTOR CAB.DORM.C/PLATO': 'TRACTOR',
        'FURGON TERMI C/EQUI DE FRIO': 'FURGON',
        'RENAULT 12 TL M 1.6': 'SEDAN',
        'CAMION CON HIDROGRUA': 'CAMION',
        'RURAL 5PTAS': 'RURAL',
        'TRANSP.DE CARGA': 'CAMION',
        'PICK-UP C/CAJA PAQUETERA': 'PICK-UP',
        'CHASSIS CABINADO': 'CHASIS CON CABINA',
        'FURGON VID. C/ASIENTO': 'FURGON',
        'FURGON 600 VIDRIADO': 'FURGON',
        'FURG.VIDRIADA C/ASIENTOS': 'FURGON',
        'CAM.C/CAJ.ABIERT.HIDROGRUA': 'CAMION',
        'SEDAN 4 PUERTTAS': 'SEDAN',
        'FURG VIDR CON ASIEN': 'FURGON',
        'FURGON VIDRID C/ASIEN': 'FURGON',
        'UNID.ESPEC.MED.FISIC': 'UTILITARIO',
        'FURGON VID.CON ASIEN': 'FURGON',
        'FURGON COUNT TYPE 600': 'FURGON',
        'MINIBUS VIDRIADO': 'MINIBUS',
        'TRACTOR C/CAB.DORMIT': 'TRACTOR',
        'CH/CAB EQ ROLOF E HIDROG': 'CHASIS CON CABINA',
        'CAMION C/ CAJA CERRADA': 'CAMION',
        'TRACTOR DE CARRE C/ CAB DORM' : 'TRACTOR',
        'CHASIS C/CAB C/FURGO': 'CHASIS CON CABINA',
        'PORTA VOLQUETE': 'ACOPLADO',
        'CHASIS C/CABINA PLAT.HIDRAU': 'CHASIS CON CABINA',
        'CAMION C/ HIDROGRUA Y VOLC': 'CAMION',
        'PICK - UP CABINA Y MEDIA': 'PICK-UP',
        'CHASIS C/CAB C/CAJ.METALICA': 'CHASIS CON CABINA',
        'TRAC. DE CARR. C/DOB EJE': 'TRACTOR',
        'PICK-UP CON CAJA TERMICA': 'PICK-UP',
        'FOURGON CUORT T.600': 'FURGON',
        'FURG VIDR CON ASIET': 'FURGON',
        'TRACTOR CON CAB DORMITORIO': 'TRACTOR',
        'SEDAN BI.': 'SEDAN',
        'FURG.VIDRIAD C/ASIENTOS': 'FURGON',
        'FURGON V CON ASIENTOS': 'FURGON',
        'CAMION C/ CAJA VOLCADORA': 'CAMION',
        'CHASIS C/CAB C/CAJA  ABIERTA': 'CHASIS CON CABINA',
        'MICROOMNIBUS 5 PTAS': 'MINIBUS',
        'FURGON C/ASIENTOS.-': 'FURGON',
        'RURAL 2PTAS': 'RURAL',
        'CAMION CAJA PLAYA HIDROGRUA': 'CAMION',
        'PICK-UP C/CAJA MUD': 'PICK-UP',
        'SEMIRREMOLQUE BARAND VOL': 'ACOPLADO',
        '02 - SEDAN 4 PUERTAS': 'SEDAN',
        'PLATAFORMA HIDRAULICA': 'ACOPLADO',
        'CHASIS C/CABINA C/CAJA ABIER': 'CHASIS CON CABINA',
        'BERLINA 5 PTAS.-': 'SEDAN',
        'FURG VIDRIADO C/ASIE': 'FURGON',
        'FURGON COUT TYPE 600': 'FURGON',
        'FURG. VIDRIADO CON ASIENTOS': 'FURGON',
        'FURGON VID. C/AS.': 'FURGON',
        'CAMION TRACTOR C/TERCER EJE': 'CAMION',
        'COMBI I 3550': 'UTILITARIO',
        'TRACTOR CON CABINA DRIO': 'TRACTOR',
        'TRACTOR CON CABINA DORMI': 'TRACTOR',
        'SEDAN 5 PTAS.-': 'SEDAN',
        'FURGON VID C ASIENTO': 'FURGON',
        'TRANS. DE AUTOMOTORES': 'CAMION',
        'CHASIS C/CAB C/PORTAV': 'CHASIS CON CABINA',
        'PICK-UP C/EQUIPO P/V': 'PICK-UP',
        'SEMIRREMOLQUE CARRET': 'ACOPLADO',
        'CHAS.C/CAB.C/FURGON': 'CHASIS CON CABINA',
        'SEMI REMOLQUE': 'ACOPLADO',
        'CHASIS C/CABINAP/CAM': 'CHASIS CON CABINA',
        'SEMIR TERM C/EQUI DE FRIO': 'ACOPLADO',
        'S. 3 PUERTAS': 'SEDAN',
        'BERLINA 3 PTAS AA': 'SEDAN',
        'PICK-UP C/CAJA TTE DE CARGA': 'PICK-UP',
        'CAMIONETA TODO TERRENO': 'PICK-UP',
        'CAMION C/PL. HID. P/TRA.AUT': 'CAMION',
        'FURGON VIDRIADOS C/ASIENTOS': 'FURGON',
        'PICK UPAUTO': 'PICK-UP',
        'FUR VID C/ASIENTOS': 'FURGON',
        'camion c/caja volcad': 'CAMION',
        'FOURGON COURT T.600': 'FURGON',
        'CAM.TIS.C/CERR.ISOT.C/E.FRIO': 'CAMION',
        'FURGON  3550': 'FURGON',
        'AUTOMOVIL SEDAN 2 PUERTAS': 'SEDAN',
        'AUTOMOVIL UTILITARIO': 'UTILITARIO',
        'S. 4 PTAS.': 'SEDAN',
        'FURGON CON EQ.DE FRIO': 'FURGON',
        'FURGON VID C/ASIE': 'FURGON',
        'TRACTOR C/CAB. DORMITORIO': 'TRACTOR',
        'PICK-UP C/CAJA MUDANZERA': 'PICK-UP',
        'CHASIS C/CABINA C/CAJA P.': 'CHASIS CON CABINA',
        'SEDAN4 PUERTAS': 'SEDAN',
        'FURGON TERM.C/EQP DE FRIO': 'FURGON',
        'CH C/CAB C/PLAT PORTA VEHIC': 'CHASIS CON CABINA',
        'FURGON VID C/ ASIEN': 'FURGON',
        'TRACTOR DE CARRET C/PLAT ENG': 'TRACTOR',
        'CAMION C/EJE BAL Y CAJA VOL': 'CAMION',
        'SEMIRR C/CAJA SIDER': 'ACOPLADO',
        'CHASIS C/CABINA C/CAM HIDR': 'CHASIS CON CABINA',
        'SEDAN 4 P.': 'SEDAN',
        'FGON.': 'FURGON',
        'FAMILIAR 5 PTS': 'SEDAN',
        'AUTOMOVIL 5 PUERTAS' : 'SEDAN',
        'CHASIS C/CAB.C/CAJA ABIERTA': 'CHASIS CON CABINA',
        'CHAS C/CAB C/PLATO': 'CHASIS CON CABINA',
        'FURGONETA VIDRIA. C/AS': 'FURGON',
        'COUPE O MICRO-COUPE': 'COUPE',
        'CONVERTIBLE 2 PUERTA': 'CABRIOLET',
        'FURGONETA VIDRIADA C/ASIENT.'  : 'FURGON',
        'FURG VIDRIAD C/ASIEN': 'FURGON',
        'BERLINA BI': 'SEDAN',
        'SEMIRREMOLQUE VOLCAD TRASERO': 'ACOPLADO',
        '05': 'NO DEFINIDO',
        '020': 'NO DEFINIDO',
        'FURGON.VID.CON ASIENTOS': 'FURGON',
        'CAMION PLAYO CON BAR': 'CAMION',
        'FURGON VIDRIADO C AS': 'FURGON',
        'PLATAFORMA HIDRAULIC': 'ACOPLADO',
        'FURGON VIDIRAD. C/ASIEN': 'FURGON',
        'CHAS.CCAB/C.PLAT.PORTAVEHI': 'CHASIS CON CABINA',
        'FURGON VID. C/ASI': 'FURGON',
        'FURGON TERMICO C/EQUIP.FRIO': 'FURGON',
        'FURGON TERMICO C/EQUIPO FRIO': 'FURGON',
        'FURG/VIDRIAD/ASIENTOS': 'FURGON',
        'FURGON TYPE 600': 'FURGON',
        'FOURGON COURT TYPE 8': 'FURGON',
        'CH/C/CAB C/CAJ P/TRANSP CARG': 'CHASIS CON CABINA',
        'CHASISC/CAB P/CAMION': 'CHASIS CON CABINA',
        'TRAC DE CARRETERA HIDROGRUA': 'TRACTOR',
        'FURGONETA VIDRI. C/ASIENTOS': 'FURGON',
        'CHASIS C/CAB, DORMIT': 'CHASIS CON CABINA',
        'SEDAN 47 PUERTAS': 'SEDAN',
        'FURGON VID C/ASI': 'FURGON',
        'FURGON VIDRIADO  C/ASIENTOS': 'FURGON',
        'SEDAN 2 PURTAS': 'SEDAN',
        'BELINA 4 PUERTAS': 'SEDAN',
        'FURGON VIID. C/ASIENTOS': 'FURGON',
        'FURGON VIDRIAD. C/ASIENT': 'FURGON',
        'CHASIS C/CABINA P/ CAMION': 'CHASIS CON CABINA',
        'FAMI': 'SEDAN',
        'F.VIDRIADO C/ASIENTO': 'FURGON',
        'FURGON VID.C/ ASIENTO': 'FURGON',
        'FURG.VID C/ASIENTOS.': 'FURGON',
        'BERLINA 3P': 'SEDAN',
        'RURAL FAMILIAR': 'RURAL',
        'FURGON VID C. ASIENT': 'FURGON',
        'TRACTOR CON CAB. DORMITORIO': 'TRACTOR',
        'FURGON VIDRIADO.': 'FURGON',
        'CAMION COMPACTADOR': 'CAMION',
        'CAM.CA.SIM.POR.VEHI.C,ISAJ': 'CAMION',
        'CHASIS C/CAB CAMILLA HIDR': 'CHASIS CON CABINA',
        'CHASIS C/CAB C/CAM. HID.': 'CHASIS CON CABINA',
        'FURG/VID/ASIENTOS': 'FURGON',
        'CAMION C/CJA MET.BARAN.ALTA': 'CAMION',
        'PICK UP-CABINA DOBLE': 'PICK-UP',
        'SEDAN 2 PTAS.-': 'SEDAN',
        'FURGON VIDIRIADO C/ASIENTOS': 'FURGON',
        'CHASIS C/CAB.C/ CAJA TERMICA': 'CHASIS CON CABINA',
        'COMBI I 3000': 'UTILITARIO',
        'CAMION C/C.PLAYA E HIDROGRUA': 'CAMION',
        'FUR.VID.C/ASIENTOS': 'FURGON',
        'CHASIS CON CABINA GRUA': 'CHASIS CON CABINA',
        'RENAULT 9 RL': 'SEDAN',
        'SEDAN DIESEL': 'SEDAN',
        'SEDAN 5 PUERAS': 'SEDAN',
        'VEHICULO UTILITARIO 4X4': 'UTILITARIO',
        'CAJA TERMICA EQUIP.FRIO': 'CHASIS CON CABINA',
        'CHASIS C/ CABINA P/ CAMION': 'CHASIS CON CABINA',
        'SEDAN 2  PUERTAS': 'SEDAN',
        'FURGON VIDRIADO S/ASIENTOS': 'FURGON',
        '27 - SEMIRREMOLQUE': 'ACOPLADO',
        'CHASIS CON CABINA P/': 'CHASIS CON CABINA',
        'SEDAN PUERTAS': 'SEDAN',
        'CAMION C/C.DE CARGA E HIDRO': 'CAMION',
        'CAMIONETA C/CAJA ABIERTA': 'PICK-UP',
        'TRANSPORTE  DE CARGA': 'CAMION',
        'FURGON VIDRIADO C/ASIENTO T': 'FURGON',
        'CAMION CAJA PLAYA C BRAZO H': 'CAMION',
        'CAMION FURGON TERM. FRIO': 'CAMION',
        'FURGON VIDRIAD/C/ASI': 'FURGON',
        'PICK UP C/CAJA AB.': 'PICK-UP',
        'FURGON 300': 'FURGON',
        'AUTOMOVIL COMBI II 5': 'UTILITARIO',
        'CHASIS ACOPLADO TOLVA': 'ACOPLADO',
        'FURGON VIDRIADOL': 'FURGON',
        'FURGON VIDRI. C/ ASIEN': 'FURGON',
        'PICK-UP CAB Y MEDIA': 'PICK-UP',
        'SEMIRREMOLQUE 2 +1': 'ACOPLADO',
        'CHASSIS ACOPLADO': 'ACOPLADO',
        'TRACTOR DE CARRETERAS': 'TRACTOR',
        'CASILLA AUTOPORTANTE': 'CASA RODANTE',
        'FURGON TÉRMICO': 'FURGON',
        'COMPACTADOR RESIDUOS': 'CAMION',
        'SEDAN 4 PÙERTAS': 'SEDAN',
        'FURGONETA C/ ASIENTOS': 'FURGON',
        'TRAC DE CARRE C/CAB DTORIO': 'TRACTOR',
        'CAJ.CER.ISOT.C/PLAT.D CARGA': 'CHASIS CON CABINA',
        'SEDAN3 PUERTAS': 'SEDAN',
        'CH C/CAB DORM C/CAJA DE C.': 'CHASIS CON CABINA',
        'CAMION PLANCHA': 'CAMION',
        'CAJA CERRADA C/ PLAT DE CAR': 'CHASIS CON CABINA',
        'CHA C/CAB C/CA TERM EQ FRIO': 'CHASIS CON CABINA',
        'RURAL FLIAR': 'RURAL',
        'CAJ.CARG.BARANDA VOLCABLE': 'CHASIS CON CABINA',
        'CHAS C/CAB C/CAJAVOLCADORA': 'CHASIS CON CABINA',
        'SEDAN 3P.': 'SEDAN',
        'CHASIS C/C. CAJA T.C/E.F.': 'CHASIS CON CABINA',
        'CHASIS C/CAB C/PORTAVOLQUETE': 'CHASIS CON CABINA',
        'UTILITARIO FURGON 4 PUERTAS': 'UTILITARIO',
        'SEDAN  2 PUERTAS': 'SEDAN',
        'SEDAN 5 PUERTAS.': 'SEDAN',
        'FURGON MIXTO 4X1': 'FURGON',
        'FURGON VIDRIADO C /ASIENTOS': 'FURGON',
        'FURGON/VIDRIAD/ASIENT': 'FURGON',
        'FORGON 600': 'FURGON',
        'SEMIRREMOLQUE 3EJ1+2': 'ACOPLADO',
        'FOURGON COURT TYPE': 'FURGON',
        'ACOPLADO SUP.L': 'ACOPLADO',
        'FURGON VIDRIAD ASIEN': 'FURGON',
        'MICRO-OMNIBUS': 'MINIBUS',
        'PICK UP C/CAJA MUDAN': 'PICK-UP',
        'JEEP TODO TERRENO': 'TODOTERRENO',
        'CAMION PORTA VOLQUETES': 'CAMION',
        'TRANSP DE CARGA': 'CAMION',
        'TCCG CARGA GENERAL': 'CAMION',
        'TRACTOR C.C/CAB DOR': 'TRACTOR',
        'SEMIRREMOLQUE PLAZYO': 'ACOPLADO',
        'FURGON VIDRIADO CON AS': 'FURGON',
        'CHASIS C/CAB C/CJA TERMICA': 'CHASIS CON CABINA',
        'CH. C/CAB C/CAJA VOLCADORA': 'CHASIS CON CABINA',
        'AUTOMOVIL FURGON 4 P': 'FURGON',
        'CHASIS P/ CAMION': 'CHASIS SIN CABINA',
        'CHASIS C/CABINA C/CAJA CERR': 'CHASIS CON CABINA',
        'FURGON NAFTERO': 'FURGON',
        'ambulancia': 'UTILITARIO',
        'CONVERTIBLE 2 PTAS': 'CABRIOLET',
        'CHASIS CON CABINA Y FURGON': 'CHASIS CON CABINA',
        'S 3 PTAS': 'SEDAN',
        'CHASIS C/CABINA CARR SAIDER': 'CHASIS CON CABINA',
        'CAMION CHASIS CABINA': 'CAMION',
        'FURGON VIDRIADO 12 A': 'FURGON',
        'CAMIONETA 3 PUERTAS': 'PICK-UP',
        'FURGON TERM.C/EQUI-D': 'FURGON',
        'FUR VIDRIADO C/ASIEN': 'FURGON',
        'SEMIRREMOLQUE CISTERNA': 'ACOPLADO',
        'FURGONETA C/CAJA TERMICA Y E': 'FURGON',
        'FURG.VIDRIADO C/ASIENOTS' : 'FURGON',
        'FURGON VIDRIADO.-': 'FURGON',
        'FURGONETA VID.C/ASIE': 'FURGON',
        'JEEP 2 PUERTAS': 'TODOTERRENO',
        'DOBLE CABINA 3 PUERTAS': 'PICK-UP',
        'FURGONETA VIDR.C/ASIENTO': 'FURGON',
        'KOMBI 4 PUERTAS': 'UTILITARIO',
        'FURGON VIDR. CON ASIENTOS': 'FURGON',
        'FURGONETA VID/ASIENTOS': 'FURGON',
        'PICK UP CABINA DOBLE 4X4': 'PICK-UP',
        'FURGONETA VIDRIADAC/ASIENTOS' : 'FURGON',
        'FURGONETA C/ASIENTO': 'FURGON',
        'CHASIS C/ CAB. C/CAJA MUD': 'CHASIS CON CABINA',
        'CHAS.C.CAB.C.CAJA.CERRADA': 'CHASIS CON CABINA',
        'PICK UP C/D': 'PICK-UP',
        'CHASIS C/ CAB Y CAJA TERM': 'CHASIS CON CABINA',
        'CHASIS C/CAB.C.VOLC/ HIDRO': 'CHASIS CON CABINA',
        'SEDAN AUTOMOVIL': 'SEDAN',
        'CAMION C/PLANCHA HIDRAULICA': 'CAMION',
        'FURGON VIDR/C/ASIENTOS': 'FURGON',
        'CHASIS C/CABINA C/C TERM': 'CHASIS CON CABINA',
        'ACOPLADO SEMIRREMOLQ': 'ACOPLADO',
        'FURG.VIDRIAD.C/ASIENTOS': 'FURGON',
        'CHASIS C/CAB Y CAJA': 'CHASIS CON CABINA',
        'CAMILLA HIDRAULICA': 'ACOPLADO',
        'CHASIS C/CAB.': 'CHASIS CON CABINA',
        'DODGE 1500': 'SEDAN',
        'F0URGON COURT T600': 'FURGON',
        'BERLINA 3PTAS.AA': 'SEDAN',
        '4X4': 'PICK-UP',
        'OTROS AUTOMOTORES DE CARGA': 'UTILITARIO',
        'AUTOMOTOR RURAL': 'RURAL',
        'FURGONETA VIDR./C/ASIENTOS': 'FURGON',
        'FURGON VIADRIADO': 'FURGON',
        'SEDAN 4 PUER0TAS': 'SEDAN',
        'CAMION CAJA ABIERTA': 'CAMION',
        'CHASIS C/CAB. C/C. REFRIGERA': 'CHASIS CON CABINA',
        'PANORAMA': 'NO DEFINIDO',
        'CAJA  MUDANCERA C/ LONA': 'CHASIS CON CABINA',
        'CAMION C/CAJA DESMONTABLE': 'CAMION',
        'CHASIS C/CAB C/ CAM HIDRAUL': 'CHASIS CON CABINA',
        'S': 'NO DEFINIDO',
        'FURGONETA  CON ASIENTOS': 'FURGON',
        'CAMION C/CAJ VOLC BRAZO HID': 'CAMION',
        'FURGON VIDR.CON ASIENTOS': 'FURGON',
        'FURGONETA VIDRIADA C/ ASIEN': 'FURGON',
        'CH C/CAB.3550 C/CAJA': 'CHASIS CON CABINA',
        'CH. C/CAB. C/CAJA TTE CARGA': 'CHASIS CON CABINA',
        'RURAL 4 PTAS.-': 'RURAL',
        'SEMIREMOLQUE TIPO BATEA': 'ACOPLADO',
        'CHASISC/CAB C/TANQUE': 'CHASIS CON CABINA',
        'CHASIS C/C C/CAJA MUDANCERA': 'CHASIS CON CABINA',
        'SEDAN 4 PTAS C/7 ASIENTOS': 'SEDAN',
        'SACHS' : 'NO DEFINIDO',
        'BLANK' : 'NO DEFINIDO',
        'BREAK 4 PTAS' : 'RURAL',
        'CHASIS C/ CAB.C/3 EJE' : 'CHASIS CON CABINA',
        'SEDAN 4 OUERTAS' : 'SEDAN',
        'TRACTOR CARRET.P/SEM' : 'TRACTOR',
        'FURGON VIDRIADO C7ASIENTOS' : 'FURGON',
        'CHASIS C/CABINA C/CAJA C' : 'CHASIS CON CABINA',
        'CAMIÓN C/CAJA P/CARGA GRAL.' : 'CAMION',
        'CHASIS C/CABINA CAJA CERRADA' : 'CHASIS CON CABINA',
        '20 - PICK-UP' : 'PICK-UP',
        'SEDAN 4 PUERRTAS' : 'SEDAN',
        'CAMION PORT.VOLQ' : 'CAMION',
        'FURGONETA VIDRIAD C/ ASIENT' : 'FURGON',
        'COMERCIAL LIVIANO' : 'UTILITARIO',
        'COUPE 2 P. KF/R8' : 'COUPE',
        'JEEP 4X4' : 'TODOTERRENO',
        'CAMION C/EQ ROLLOFF C/B HIDR' : 'CAMION',
        'CHASIS C/CAB C/CAJA TR CARGA' : 'CHASIS CON CABINA',
        'VIDRIADO C/ ASIENTOS' : 'FURGON',
        'CAM.TISOF C.CER.C/EQ.DE FRI' : 'CAMION',
        'FURGON.VIDRIADO C/ASIENTOS' : 'FURGON',
        'BERLINA 4 PUERTAS.' : 'SEDAN',
        'FURG.VID C/ ASIENTOS' : 'FURGON',
        'SEDAN 3 PUERTTAS' : 'SEDAN',
        'CHASIS C/CAB C/CAM HID' : 'CHASIS CON CABINA',
        'FURGON VIDRADO C/ ASIENTOS' : 'FURGON',
        'UNO CS' : 'SEDAN',
        'FURGON VIDIRADO CON ASIENTOS' : 'FURGON',
        'FURGON LARGO VIDR C/ASIENT' : 'FURGON',
        'FURGONETA VDRA. C/ASIENTOS' : 'FURGON',
        'BERLINA 3PT AA' : 'SEDAN',
        'SEDAN 4 PUTAS' : 'SEDAN',
        'CAMIONETA CAB SIM CAJ FRIGO' : 'PICK-UP',
        'BERLINA 4 PTS' : 'SEDAN',
        'FURGON TERM C/EQ FRIO' : 'FURGON',
        'UTILITARIO.COMBI.II.5 PTAS' : 'UTILITARIO',
        'PICK-UP C/C.ABIERT-MUDANCERA' : 'PICK-UP',
        'CAM.C/PCHA.REM.Y BZO HID.' : 'CAMION',
        'T.TERRENO' : 'TODOTERRENO',
        'CAMION A CAJA ABIERTA' : 'CAMION',
        'FURGON VID/C/ASIENTOS.' : 'FURGON',
        'AUTOMOVIL-WAGON 5 PUERTAS' : 'RURAL',
        'BREAK 5 P' : 'RURAL',
        'FURGON TERMICO C/EQ FRIO' : 'FURGON',
        'CHASIS C/CAB. C/C ABIERTA' : 'CHASIS CON CABINA',
        'FURGON VIDRIADO C/ ACIENTOS' : 'FURGON',
        'SEDA 4 PUERTAS Y 1 T' : 'SEDAN',
        'CAMION C/ CAJA METALICA' : 'CAMION',
        'PICK-UP TCCE (CAJA CERRADA)' : 'PICK-UP',
        'FURGONETA VIDRIADA C/AS.' : 'FURGON',
        'CORSA GL 1.6 MPFI' : 'SEDAN',
        'CAMION C/CAJ VOLC/HIDROGRUA' : 'CAMION',
        'PICK-UP C/CAJA TERM REFRIGER' : 'PICK-UP',
        'FURGON BLINDADO' : 'FURGON',
        'PLATAF.HIDRAULICA' : 'ACOPLADO',
        'FURGONETA VIDRIADA C ASIENTO' : 'FURGON',
        'TRANSPOTE DE CARGA' : 'CAMION',
        'UTILITARIO 4X4' : 'UTILITARIO',
        'FURGON ISOTER C/EQUIP FRIO' : 'FURGON',
        'TRACTOR DE CARR.P/SEMIRREMOL' : 'TRACTOR',
        'PICK- UP' : 'PICK-UP',
        'SEMIRREMOLQUE FRAQ-TANQ-MINE' : 'ACOPLADO',
        'CHASIS C/CAB.C/EQUIP ROLOFF' : 'CHASIS CON CABINA',
        'CAMION CON CAJA' : 'CAMION',
        'CAMION VOL TRES EJES' : 'CAMION',
        'FOURGONCOURTTYPE 600 VID/AS' : 'FURGON',
        'FURGONETA VIDR.C/ASIEN' : 'FURGON',
        'FURGON 800 VID C/ASIENTOS' : 'FURGON',
        'AUTOM. PLATAFORMA 2' : 'ACOPLADO',
        'CHASIS C/CAB C/BRAZO' : 'CHASIS CON CABINA',
        'TRACTOR C/CAB DORMITORIO' : 'TRACTOR',
        'SEMIRREMOLQUE CARGA' : 'ACOPLADO',
        'FURGON COURT T 600' : 'FURGON',
        'RURAL 4 PUARTAS' : 'RURAL',
        'PICK-UP S/C' : 'PICK-UP',
        'TRACTOR CARRE.C/CAB.DOR' : 'TRACTOR',
        'FUR.VIDRIADO C/ASIEN' : 'FURGON',
        'FAMILIAR VAN' : 'SEDAN',
        'SEMIREMOLQUE FURGON TERMICO' : 'ACOPLADO',
        'FURGON VIDRID.C/ASIE' : 'FURGON',
        'CHASIS C/C C/CAM P/AUT' : 'CHASIS CON CABINA',
        'CH. CABINA 3550.' : 'CHASIS CON CABINA',
        'CAMION C/ HIDROGRUA' : 'CAMION',
        'CHASIS C/CABINA C/CAJA MET' : 'CHASIS CON CABINA',
        'RURAL 5 PUERT' : 'RURAL',
        'AUTOMOVIL 5 PTS.' : 'SEDAN',
        'CHASIS' : 'CHASIS CON CABINA',
        'VEHICULO UTILITARIO 4X4 5PUE' : 'UTILITARIO',
        'SEDAN 4 TAS' : 'SEDAN',
        'FURGON  800' : 'FURGON',
        'CAMION CAJA CERRADA SIDER' : 'CAMION',
        'FURGON VIDRIDADO C/A' : 'FURGON',
        'ACOPLADO VOLCADOR' : 'ACOPLADO',
        'PICK-UP C/CAJA PAQUE' : 'PICK-UP',
        'BERLINA 56 PTAS.' : 'SEDAN',
        'GOL GLD' : 'SEDAN',
        'CHASIS SEMIACOPLADO' : 'CHASIS CON CABINA',
        'FURGON VIDRIA.C/ASIE' : 'FURGON',
        'SEDAN5 PTAS' : 'SEDAN',
        'FURGON VIDR.C/ASENTOS' : 'FURGON',
        'CHASIS CON CABINA C/CAJTERM' : 'CHASIS CON CABINA',
        'FURGON C/EQ FRIO' : 'FURGON',
        'FURGONETA CAJ TER EQ FRIO' : 'FURGON',
        'SEDAN 5PTS.'   : 'SEDAN',
        'TCCE (CAJA CERRADA)' : 'UTILITARIO',
        'CAMION  C/PLAT PORT VEHIC.' : 'CAMION',
        'TRACTOR C/ CAB DORMITORIO' : 'TRACTOR',
        'BERLINA 3 PUERTAS.' : 'SEDAN',
        'FAMILIAR VIDRIADA C/ASIENTOS' : 'SEDAN',
        'FURGONTERMICOC/EQUIPFRIO' : 'FURGON',
        'FURGON CON VENTANAS' : 'FURGON',
        'FURGON VID.C/ASIENTOS.' : 'FURGON',
        'AUTOMOVIL COMBI II 5 PUERTAS' : 'SEDAN',
        'CHASIS P/CAMION M BENZ COD.4' : 'CHASIS SIN CABINA',
        'FURGON TERM C/EQ DE FRIO' : 'FURGON',
        'SEDAN 4 PUETAS' : 'SEDAN',
        'CHASISC/CABC/CAJ/METALICA' : 'CHASIS CON CABINA',
        'MINIBUS 12 ASIENTOS' : 'MINIBUS',
        'RURAL 5 PTS' : 'RURAL',
        'CAMIONETA CABINA SIM' : 'PICK-UP',
        'CHASIS C/CAB CAMILLA HIDRAU' : 'CHASIS CON CABINA',
        'RURAL 4  PUERTAS' : 'RURAL',
        'FURGON VIDRIADOC/ASIENTOS' : 'FURGON',
        '348 - FOX 1.6' : 'SEDAN',
        'UTILITARO' : 'UTILITARIO',
        'FURGON VID.C ASIENTOS' : 'FURGON',
        'HATCHBACK' : 'SEDAN',
        'CAMION C/CJA TERM. Y EQ.FRIO' : 'CAMION',
        'CH C/CAB C/PLAT P/VEH' : 'CHASIS CON CABINA',
        'FURGON BALANCIN' : 'FURGON',
        'CHASIS C/CABINA CAJA ABIER.' : 'CHASIS CON CABINA',
        'SEMIRREMOLQUE BDAS. VOLC' : 'ACOPLADO',
        'SEDAN  3 PTAS' : 'SEDAN',
        'CAJA ABIERTA MUDANCERA' : 'ACOPLADO',
        'FURGON VIDDRIADO C/A' : 'FURGON',
        'FURGON VIDRIADO/C ASIENTOS.' : 'FURGON',
        '12' : 'NO DEFINIDO',
        'AUTOMOVIL COMBI 5PTAS' : 'SEDAN',
        'FAMLIAR' : 'SEDAN',
        'CHASIS C/CAB CAJA ABIERTA' : 'CHASIS CON CABINA',
        'ACOPLADO P/TOLVA O VOLCADOR' : 'ACOPLADO',
        'CHASIS C/CAB. P/CAMI' : 'CHASIS CON CABINA',
        'FURGON VIDRI.C/ASIENTOS' : 'FURGON',
        'PALIO 1.6 SPI' : 'SEDAN',
        'SEMIRREMOLQUE CARGA SECA M' : 'ACOPLADO',
        'PICK-UP.CJ.PLAY.BNDA.VOLC' : 'PICK-UP',
        'TRANSPORTE UTILITARIO' : 'UTILITARIO',
        'FURGON  600 VIDRIADO CON A/' : 'FURGON',
        'BERLINA 5PUERTAS' : 'SEDAN',
        'CHA C/ CAB C/ CAJA CERRADA' : 'CHASIS CON CABINA',
        'UTILITARIO 4X4 5 P' : 'UTILITARIO',
        'CAMION C/EQ PORTA ROLL OFF' : 'CAMION',
        'SEDAN.' : 'SEDAN',
        'FURGON TERMICO SEMIR' : 'FURGON',
        'FURGON TERMICO C/ EQ. FRIO' : 'FURGON',
        'CHASIS C/CAB. DORM.' : 'CHASIS CON CABINA',
        'FURGON/VIDRIADO' : 'FURGON',
        'CAMION TCCE CAJA CERRADA' : 'CAMION',
        'FURGON    800' : 'FURGON',
        'FURG.TERM. C/ EQ.FRIO' : 'FURGON',
        'FURGON VIDRID.C/ASIENTOS' : 'FURGON',
        'SEDAN 5PUERTAS' : 'SEDAN',
        'PICK-UP CAB.DOBLE' : 'PICK-UP',
        'FURGON VIDR. C/ASIEN.' : 'FURGON',
        'PICK UP MUDANCERO' : 'PICK-UP',
        'CH C/ CAB. C/ PORTA VOLQUETE' : 'CHASIS CON CABINA',
        'CHASIS C/CAB C/ CAJ SAIDER' : 'CHASIS CON CABINA',
        'FURGON FAMILIAR VIDR' : 'FURGON',
        'SDAN 4 PUERTAS' : 'SEDAN',
        'CAMION TRACTOR C/CAJA VOLCA' : 'CAMION',
        'FURG VIDRIA C/ASIENT' : 'FURGON',
        'FURGON VIDRIADO ASIENTOS' : 'FURGON',
        'CAMION C/CAJA CDA. SIDER' : 'CAMION',
        'CHASISC/CAB.C/EQUIPROLOFF' : 'CHASIS CON CABINA',
        'TRAN. DE CARGA' : 'CAMION',
        'VIDRIADA C/ASIENTOS' : 'SEDAN',
        'CHASIS C/CAB C/ROLL OFF' : 'CHASIS CON CABINA',
        'SEMIRREMOLQUE CISTER' : 'ACOPLADO',
        'STATION WAGON 5 PUERTAS' : 'RURAL',
        'FURGON VID. CON ASIE' : 'FURGON',
        'SEMIRREMOLQUE BARAND' : 'ACOPLADO',
        'CHASIS C/CABINA C/CAJA TERM' : 'CHASIS CON CABINA',
        'CHASIS C/CABINA C/ CAJA MET' : 'CHASIS CON CABINA',
        'FURGONETA VIDRIA. C/ASIENTOS' : 'FURGON',
        'FURGON VIDR.C/7 ASIENTOS' : 'FURGON',
        'CHASIS C/CAB.C/EQ.ROLLOFF' : 'CHASIS CON CABINA',
        'TRANSP.DE PASAJEROS' : 'UTILITARIO',
        'CHASIS C/ CAB. C/ CAJA PLAYA' : 'CHASIS CON CABINA',
        'CHASIS C/CABINA+FUR.TER' : 'CHASIS CON CABINA',
        'FOURGON C. T.600 VID C/ASI' : 'FURGON',
        'FURGON VIDRIADO CON AS/' : 'FURGON',
        'CAMION CAB. SIMPLE VOLCADOR' : 'CAMION',
        'FURON' : 'FURGON',
        'FURGON VIDRIADO AUTOPORTANTE' : 'FURGON',
        'DEPORTIVO 3 PTAS' : 'COUPE',
        'S,WAGON' : 'RURAL',
        'FAMILIAR 4P (4+1)' : 'SEDAN',
        'RENAULT BI' : 'SEDAN',
        'FURGON  C/EQUIPO DE FRIO' : 'FURGON',
        'TTE.DE CARGA' : 'CAMION',
        'TRANSPORTE DE AUTOMOTORES' : 'CAMION',
        'CAMIONETA PICK UP' : 'PICK-UP',
        'BERLINA  4 PTAS' : 'SEDAN',
        'CAMION C/CAJA P/TRANS CARGA' : 'CAMION',
        'RURAL 4  PTAS' : 'RURAL',
        'TRAC C/CAB DOR C/CAJ VOLC' : 'TRACTOR',
        'FOURG COURT TYPE 600' : 'FURGON',
        'CHAS.C/CAB.C/HIDROGRUA VOLC' : 'CHASIS CON CABINA',
        'UTILITARIO FURGON' : 'FURGON',
        'CHASIS C/EQUIPO FRIO' : 'CHASIS CON CABINA',
        'CHASIS C/CABINA C/FU' : 'CHASIS CON CABINA',
        'SEDAN 3 PUERTAS AA' : 'SEDAN',
        'AUTOMOVIL SEDAN' : 'SEDAN',
        'CHASIS C/C C/EQ.PORTA VOLQ' : 'CHASIS CON CABINA',
        'CAMIONETA 2 PUERTAS' : 'PICK-UP',
        'CAMION CON CAJA VOLCADORA' : 'CAMION',
        'CHASIS C/CABINA C/C ABIERTA' : 'CHASIS CON CABINA',
        'SEDAN KBH8' : 'SEDAN',
        'FURGON TERM.C/EQ.FRIO' : 'FURGON',
        'FURGON  VIDRIADO  C/ASIENTOS' : 'FURGON',
        'FURG VIDR C/ASIENTOS' : 'FURGON',
        'CHASIS C/C GRUA C/ PLANCHADA' : 'CHASIS CON CABINA',
        'CHASIS CON CAJA PLAYA' : 'CHASIS CON CABINA',
        'TRANS.DE CARGA' : 'CAMION',
        'SEMIRREM.BDAS.VOLC.' : 'ACOPLADO',
        'furgon vid.c/asiento' : 'FURGON',
        'SEDAN 5 PUERTA' : 'SEDAN',
        'FURGON VIDR' : 'FURGON',
        'CHASIS C/CA P/CAMION' : 'CHASIS CON CABINA',
        'CABRIOLET' : 'CABRIOLET',
        'GRUA CON PLANCHADA' : 'GRUA',
        'FURGON CON FRIO' : 'FURGON',
        'UTILITARIO 4X4 5 PUERTAS' : 'UTILITARIO',
        'SEMIRREMOLQUE 1+2 EJ' : 'ACOPLADO',
        'CHASIS C/CABINA LARG' : 'CHASIS CON CABINA',
        'CHASIS C/CAB C/CAMILLA HIDR' : 'CHASIS CON CABINA',
        'CAJA VOLCADORA C/HIDROGRUA' : 'CHASIS CON CABINA',
        'BREAK 4/5 PTAS' : 'RURAL',
        'VAN FAMILIAR' : 'SEDAN',
        'FURGON VID. C/5 ASIE' : 'FURGON',
        'CHASIS C/CAB C/ CAJA CERRADA' : 'CHASIS CON CABINA',
        'COMPACTADOR TRASERO' : 'CHASIS SIN CABINA',
        'TRACTOR CARR.P/SEMIRREMOLQUE' : 'TRACTOR',
        'CHAS.C/CAB.C/CAJ.TER' : 'CHASIS CON CABINA',
        'FOURGONCOURT TYPE600' : 'FURGON',
        'SEDAN 4PTS' : 'SEDAN',
        'FURGÓN VIDRIADO CON ASIENTOS' : 'FURGON',
        'SEDAN 4 PTAS.Y 1 TRA' : 'SEDAN',
        'FURGON VID/C/ASIENTO' : 'FURGON',
        'FURG. VID. C/ASIENTOS' : 'FURGON',
        'FURGON COURTTYPE600' : 'FURGON',
        'CHASIS C/C CON PLANCHA GRUA' : 'CHASIS CON CABINA',
        'ACOPLADO TODO PUERTA' : 'ACOPLADO',
        'CHASIS C/CAB.C/CAJ ABIERTA' : 'CHASIS CON CABINA',
        'WEEKEND 5 PUERTAS' : 'RURAL',
        'COUPE- 3 PUERTAS' : 'COUPE',
        'FURGÓN TÉRMICO' : 'FURGON',
        'CHASIS C/CAB C/EQUIP ROLOFF' : 'CHASIS CON CABINA',
        'FURG.VIDRIADO C/ASIENTO TRAS' : 'FURGON',
        'CAMION C/CABINA DORMITORIO' : 'CAMION',
        'CAJA TERM.C/EQUIP.FRIO' : 'CHASIS CON CABINA',
        'TRACTOR  C/CABINA DORMITORIO' : 'TRACTOR',
        'CHASIS C/CAB.C/CAJA AB.' : 'CHASIS CON CABINA',
        'FURGON VIDRIDO C/ ASIENTOS' : 'FURGON',
        'SEUERTAS' : 'SEDAN',
        'BREACK 4 PUERTAS' : 'RURAL',
        'FURGON TERMICO C/ EQUIP.FRIO' : 'FURGON',
        'CAMION C/CAJA TERM.Y EQ.FRIO' : 'CAMION',
        'FURGON V/ASIENTO' : 'FURGON',
        'CAMION C/PLAT.PORT.VEH.C/IZ' : 'CAMION',
        'PLAT. PORTA VEH.CON IZAJE' : 'ACOPLADO',
        'FURGON TÉRM C/ EQ. DE FRÍO' : 'FURGON',
        'CHASIS C/CAB.C/PORT.VOLQ.' : 'CHASIS CON CABINA',
        'HIDROGRUA C/CAJA PLAYA' : 'CHASIS CON CABINA',
        'FURGONETA VIDRIADO C/ASIENTO' : 'FURGON',
        'FURGON VID./ASIENTOS' : 'FURGON',
        'CAJA CERRADA ISOTERMICA C/F' : 'CHASIS CON CABINA',
        'REMOLQUE' : 'ACOPLADO',
        'CHASIS C/CAB C/CAJ ABIERTA' : 'CHASIS CON CABINA',
        'BERLINGO FURGON 1.9D' : 'FURGON',
        'GRUA' : 'GRUA',
        'CHASIS C/CAB C/TERM E. FRIO' : 'CHASIS CON CABINA',
        '2 PUERTAS' : 'SEDAN',
        'CAMION C/CAJA CARGAS GRALES' : 'CAMION',
        '3PTAS' : 'SEDAN',
        'CHASIS C/CAB.SIM.C/CAJ.ISOT' : 'CHASIS CON CABINA',
        'FURGON VID-C/ASIENTO' : 'FURGON',
        'RURAL 3P' : 'RURAL',
        'SEDAN U PUERTAS' : 'SEDAN',
        'CHASIS C/ CAB. C/CAJA PLAYA' : 'CHASIS CON CABINA',
        'COMPACTO STANDART 4P' : 'SEDAN',
        'CAMION CAMA' : 'CAMION',
        'PICK-UP CABINA DOBLE 4X2' : 'PICK-UP',
        'PICK UP - CABINA DOBLE - 4X4' : 'PICK-UP',
        'SEDAN 2 P.' : 'SEDAN',
        'CAMION C/ C MET/VOLCADORA' : 'CAMION',
        'CH. CABINA 3550' : 'CHASIS CON CABINA',
        'MINI VAN VIDRIADA' : 'SEDAN',
        'PICK-UP DOB.CAB.C.VIDC/A' : 'PICK-UP',
        'FURGON VIDR CON ASIENTOS' : 'FURGON',
        'FURGONETA CON VIDRIOS Y ASIE' : 'FURGON',
        'FURGON ISOTERMICO' : 'FURGON',
        'CHASIS C/CAB C/CAM. P/ AUX' : 'CHASIS CON CABINA',
        'CHASISC/CAJTER. Y E.DEFRIO' : 'CHASIS CON CABINA',
        'AUTOMOVIL COMBI II' : 'SEDAN',
        'RURAL 2/3 PUERTAS' : 'RURAL',
        'PICK -UP CABINA DOBL' : 'PICK-UP',
        '3ºEJE N/GRUA VEH/CAM REF' : 'ACOPLADO',
        'SEDAN 4 PUERTAS DIESEL' : 'SEDAN',
        'CHASIS C/CAB Y CAJ VOLCADORA' : 'CHASIS CON CABINA',
        'SEDAN 3PTAS' : 'SEDAN',
        'S.5PTAS' : 'SEDAN',
        'TRANPORTE DE PASAJEROS' : 'UTILITARIO',
        'FURGON VIDRADO C/ASIENTO' : 'FURGON',
        'RURAL DIESEL' : 'RURAL',
        'STATION WAGON 5 PTAS' : 'RURAL',
        'GRUA HIDRAULICA PLEG' : 'GRUA',
        'CAMION C/CAJA PALETE' : 'CAMION',
        'TRANS.PASAJEROS/COMBI' : 'UTILITARIO',
        'RURAL (STATION WAGON)' : 'RURAL',
        'CHASIS C/CAB C/CAM.HIDR.' : 'CHASIS CON CABINA',
        'SEMIRREMOLQUE VOLCADOR' : 'ACOPLADO',
        'PI' : 'NO DEFINIDO',
        'SEDAN 2PTAS' : 'SEDAN',
        'CAMION RIGIDO C/SIMP C/FRIG' : 'CAMION',
        'FURGON COURT TYPE' : 'FURGON',
        'CAMION C/HIDROGRUA Y CAJA P.' : 'CAMION',
        'FURGÓN MIXTO / UTILITARIO' : 'FURGON',
        'CAMION C/PLANCHA DE AUXILIO' : 'CAMION',
        'CAMION C/PLANCHA P/REMOLQUE' : 'CAMION',
        'TCCIEF C.CE.ISOTER/EQ FRIO' : 'CHASIS CON CABINA',
        'CHASIS C/CABINA FURGON' : 'CHASIS CON CABINA',
        'PICK-UP C/ CAJA FRIGORIFICA' : 'PICK-UP',
        'AUTOMOVIL WAGON 5 PU' : 'SEDAN',
        'PICK-UP CABINA DOBLE 4X4' : 'PICK-UP',
        'CHASIS C/CAB C/CAJ CERR' : 'CHASIS CON CABINA',
        'furg vidr con asient' : 'FURGON',
        'RURAL NAFTERA' : 'RURAL', 
        'TCA (CAJA ABIERTA)' : 'CHASIS CON CABINA',
        'CAMION C/CAJA SINDER' : 'CAMION',
        'SEDAN BERLINA DIESEL' : 'SEDAN',
        'FURGON VIDR C/ AS' : 'FURGON',
        'FURGON VIDRIADO. C/ASIENTOS' : 'FURGON',
        'CHASIS C/CAB+HIDRO+C/CGRALES' : 'CHASIS CON CABINA',
        'SEDAN 4 PEURTAS' : 'SEDAN',
        'SEDAN 5 PTUERAS' : 'SEDAN',
        'PLATAFORMA 2 PUERTAS' : 'SEDAN',
        'R 5 PUERTAS' : 'RURAL',
        'FURGON VID/ C/ ASIENTOS' : 'FURGON',
        'TRACTOR CON CABINA DORM' : 'TRACTOR',
        'CAMION TISOF CC ISO C/EQ F' : 'CAMION',
        'CHASIS C/CABINA 3550' : 'CHASIS CON CABINA',
        'S.WAGOM' : 'RURAL',
        'RURAL 4/5 PUERTAS (S.WAGON)' : 'RURAL',
        'BERLINA 3TAS AA' : 'SEDAN',
        'CAMION TRACTOR C/D PLATO' : 'CAMION',
        'PICK UP DOBLE CAB. CARROZ' : 'PICK-UP',
        'CABINA SIMPLE C/ CAJA VOL' : 'CHASIS CON CABINA',
        'CASA RODANTE AUTOPROP.' : 'CASA RODANTE',
        'CHASIS C/CABINA CAJTERMFRIO' : 'CHASIS CON CABINA',
        'FURGON VIDRI/C/ASIENTOS' : 'FURGON',
        'CHASIS C/CABINA C/EQ ROLOF' : 'CHASIS CON CABINA',
        'CAJA  MUDANCERA' : 'CHASIS CON CABINA',
        'FGON.LARGO S/D' : 'FURGON',
        'CAMION C/CAJA DE CARGA' : 'CAMION',
        'ACOPLADO BARANDA VOL' : 'ACOPLADO',
        'CAMIONETA CAJA ABIERTA' : 'PICK-UP',
        'SEDAN  4 PTAS' : 'SEDAN',
        'CH/C/CAB/C/CAJA ABIE' : 'CHASIS CON CABINA',
        'CAM BALANCIN C/CAJA TERM' : 'CAMION',
        'FURGON VIDRIANDO C/A' : 'FURGON',
        'CHASIS C/CAB.C/PLATAF.PORT' : 'CHASIS CON CABINA',
        'PICK UP - CAB. Y MED' : 'PICK-UP',
        'R 5PUERTAS' : 'RURAL',
        'CHASIS C/CAB.DORM/CARROC.' : 'CHASIS CON CABINA',
        'FURGON  VIDR. C/ASIENTOS' : 'FURGON',
        'RURAL 4PTAS' : 'RURAL',
        'CHAS.C/CAB.C/EQUIP/FRIO' : 'CHASIS CON CABINA',
        'FURGON VIDRADO C/ASIENTOS' : 'FURGON',
        'FURGON C CAMARA FRIGORIFICA' : 'FURGON',
        'FURGON VIDRIDADO C/ASIENTOS' : 'FURGON',
        'CHASIS CON CAB C/CAJA CE' : 'CHASIS CON CABINA',
        'S. 4 PUERTAS' : 'SEDAN',
        'FURGON VIDRIA.C/ASIEN.' : 'FURGON',
        'CHASIS C/CABINA SIMPL Y CAJ' : 'CHASIS CON CABINA',
        'CHASIS C/CABINA DORM' : 'CHASIS CON CABINA',
        'CHASIS C/CAJA PAQUETERA' : 'CHASIS CON CABINA',
        'TREN RODANTE' : 'TREN',
        'PICK-UP C/C TER Y EQ D FRIO' : 'PICK-UP',
        'FURGON VIDRIADO FAMILIAR' : 'FURGON',
        'TT' : 'NO DEFINIDO',
        'ACOPLADO BALANCIN' : 'ACOPLADO',
        'C/ CAB. CON PORT. VOLQUETE' : 'CHASIS CON CABINA',
        'furgon con asientos' : 'FURGON',
        'CAMION RIGIDO C/CAJ.ABIERTA' : 'CAMION',
        'SEDAN 5 PUIERTAS' : 'SEDAN',
        'FURGONETA VIDRIADA ASIENTOS' : 'FURGON',
        'FURGON VID. C/ AS.' : 'FURGON',
        'PICK-UP C/C' : 'PICK-UP',
        'TRACTOR CON C/ DORMITORIO' : 'TRACTOR',
        'CAMION C/ CAM HIDRAULICA' : 'CAMION',
        'PICK-UP -CABINA DOBLE- 4X2' : 'PICK-UP',
        'FURGON TERM C/ EQ DE' : 'FURGON',
        'CHASIS C/CABINA C/ CAM HIDR' : 'CHASIS CON CABINA',
        '4 X 4' : 'TODOTERRENO',
        'CAMION C/ CAJ PLAYA B LAT' : 'CAMION',
        'COMBI 5 PUERTAS' : 'SEDAN',
        'CHASIS C/ CABINA 3550' : 'CHASIS CON CABINA',
        'CHAS C/CAB C/CAJA FRIGORIF' : 'CHASIS CON CABINA',
        'FURGON VIDRIADO C/*ASIENTO' : 'FURGON',
        'SEDNA 4 PUERTAS' : 'SEDAN',
        'FURGONET VIDRIAD C/ ASIENTOS' : 'FURGON',
        'CHA.C/C Y PLA.PORTA VE' : 'CHASIS CON CABINA',
        'FURG' : 'FURGON',
        'CHAS/C/CABC/TRATCARRT' : 'CHASIS CON CABINA',
        'COUPE 2 P.' : 'COUPE',
        'SEMIRREMOLQUE VUELCO TRAS.' : 'ACOPLADO',
        'ACOPLADO MIXTO' : 'ACOPLADO',
        'R MEGANE RT TRIC 2.0' : 'SEDAN',
        'FURGON ISOTERM C/EQU FRIO' : 'FURGON',
        'FURGON VIDRIADO C/ASIENT.' : 'FURGON',
        'CHASIS C/CAB' : 'CHASIS CON CABINA',
        'PICK-UP CABINA S' : 'PICK-UP',
        'SEDAN 2 P' : 'SEDAN',
        'PICK-UP 2 PUERTAS' : 'PICK-UP',
        'CAMION C/CAJA PLAYA Y GRUA' : 'CAMION',
        'RECOL.COMPACTADOR' : 'CAMION',
        'CAMION CAJA AB. C/HIDROGRUA' : 'CAMION',
        'FURGON VID/ASIENTOS' : 'FURGON',
        'CAMION CAJA A. VOLCADORA' : 'CAMION',
        'CHASIS C/CAB+HIDROGRUA+CAJA' : 'CHASIS CON CABINA',
        'CHASIS C/CAB.C/EQUIPO ROLOF' : 'CHASIS CON CABINA',
        'CH C/CAB DORM, C.PL. E HID' : 'CHASIS CON CABINA',
        'FURGON VIDR C/ ASIEN' : 'FURGON',
        'BERLINA 3 PT. AA' : 'SEDAN',
        'FURGON ISOT. C/EQ FRIO' : 'FURGON',
        'C C/C + C/TRA Y TAN AUX COMB' : 'CHASIS CON CABINA',
        'C CAB CAJ ABIERTA HIDROGRUA' : 'CHASIS CON CABINA',
        'CHASIS C/CBNA C/ CAJA PLAYA' : 'CHASIS CON CABINA',
        'MINI-BUS' : 'MINIBUS',
        'CAJA ISOTERMICA P/ FRIO' : 'CHASIS CON CABINA',
        'CHASIS C/CAB.C/C.AB.C/VOLCA' : 'CHASIS CON CABINA',
        'CH.C/CAB C/CAJ.VOLCADORA' : 'CHASIS CON CABINA',
        'CAJA CERR ISOTER C/EQ. FRIO' : 'CHASIS CON CABINA',
        'SEDAN 4 PUERAS' : 'SEDAN',
        'CAMION CON CAMILLA' : 'CAMION',
        'SEDAN 5 PTAS. C/ 7 ASIENTOS' : 'SEDAN',
        'CHASIS C/CAB C/ CAJA PLAYA' : 'CHASIS CON CABINA',
        'FURGON V/CON ASIENTOS' : 'FURGON',
        'PICK UP CAB.DOB' : 'PICK-UP',
        'SEDAN 3 PUERTAS CON' : 'SEDAN',
        'CAMION C/HIDROGRUA/VOLCADOR' : 'CAMION',
        'VEHICULO UTILITARIO 4X4 5 P' : 'UTILITARIO',
        'FURGON VIDRIADO CON ASIEN' : 'FURGON',
        'PICK-UP C/TANQUE. CISTERNA' : 'PICK-UP',
        'PICK-UP CAB. SIM. C/CERRADA' : 'PICK-UP',
        'CAMION CON HIDROG C/C PLAY' : 'CAMION',
        'FURGON 8000' : 'FURGON',
        'C.ABIERTA C/BARANDA VOLCABLE' : 'CHASIS CON CABINA',
        'CHASIS C/CAB P/CAMIO' : 'CHASIS CON CABINA',
        '4 PUERTAS AUTOMATICO' : 'SEDAN',
        'RURAL 4/5 PUERT' : 'RURAL',
        'CAMIONETA TODO TERRE' : 'PICK-UP',
        'FURGON VIDRIADO C /' : 'FURGON',
        'UTILITARIO 4X4 5 PUE' : 'UTILITARIO',
        'CHASIS C/CAB C/CAJA METALIC' : 'CHASIS CON CABINA',
        'SEDAN 4 PERTAS' : 'SEDAN',
        'CAB. SIMPLE Y C. CE. SIDER' : 'CHASIS CON CABINA',
        'FURGON VID.C./AS' : 'FURGON',
        'CAM/RIG/C/TAN/CISTERNA' : 'CAMION',
        'FURGON VIDRIADO CN ASIENTOS' : 'FURGON',
        'FURGON VIDRIADOS C/ ASIENTOS' : 'FURGON',
        'FURGON CAJA CERRADA' : 'FURGON',
        'CAMIÓN' : 'CAMION',
        'SEDAN 5 PUETAS' : 'SEDAN',
        'TRANSP.ESCOLAR' : 'UTILITARIO',
        'RURAL 5 PUERTA' : 'RURAL',
        'CHASIS C/C CAMION PLANCHA' : 'CHASIS CON CABINA',
        'FURGON COURTTYPE 600' : 'FURGON',
        'BERLINA BI.' : 'SEDAN',
        'TRACTOR DE CARRETERA CON' : 'TRACTOR',
        'CAMION P. PORTAVEHICULOS' : 'CAMION',
        'FURGON C/CAJA CERRAD' : 'FURGON',
        'FURGONETA VIDRIADA C/A' : 'FURGON',
        'SEDAS 4 PUERTAS' : 'SEDAN',
        'C/CAJA VOLCADORA HIDROAGUA' : 'CHASIS CON CABINA',
        'CAMION C/CAJA TIPO SAIDER' : 'CAMION',
        '22 - FURGON VID. C/ASIENTOS' : 'FURGON',
        'CHASIS C/CABINA/CAMI' : 'CHASIS CON CABINA',
        'CAMION CAB.SIMP.FRIG.YPLAT.' : 'CAMION',
        'CAJA CERRADA ISOTERMICA' : 'CHASIS CON CABINA',
        'CAMION /CAJA VOLCAD' : 'CAMION',
        'SEMIRREMOLQUE/VOLCADOR TRASE' : 'ACOPLADO',
        'FURG. VIDR. C/ASIENTOS' : 'FURGON',
        'CHASIS C/CAB C/CAJA PLAYA' : 'CHASIS CON CABINA',
        'VIDRIADO CON ASIENTOS' : 'FURGON',
        'FURGON VIDRIA. C/ASI' : 'FURGON',
        'SEMIRREMOLQUE CARGA SECA' : 'ACOPLADO',
        'FURGON VIDR.C/ASI' : 'FURGON',
        'C C/PLATO DE ENGANCHE C/D' : 'CHASIS CON CABINA',
        'FU VID C/ASIENTOS' : 'FURGON',
        'CHASIS C-CABINA P-CA' : 'CHASIS CON CABINA',
        'S 4 PUERTAS' : 'SEDAN',
        'FURGON ISOTERMICO C/EQ FRIO' : 'FURGON',
        'TODO TERR' : 'TODOTERRENO',
        'SEDAN 3 PUERTAS.' : 'SEDAN',
        'BERLINA 5 P' : 'SEDAN',
        'SEDEAN 5 PUERTAS' : 'SEDAN',
        'CHA C/CAJ SID Y PLAT HIDR' : 'CHASIS CON CABINA',
        'CH. C/ CAB Y CAJ SIDER' : 'CHASIS CON CABINA',
        'TRACT DE CARRET C/CABDORM' : 'TRACTOR',
        'CHAS C/CAB C/EQUIP DE FRIO' : 'CHASIS CON CABINA',
        'CHASIS C/ CAB C/ CAJA MUD' : 'CHASIS CON CABINA',
        'BERLINA 3 PTAS.AA' : 'SEDAN',
        'CAMION CAB SIMP FRIGORIFICO' : 'CAMION',
        'FURGON CAJA ABIERTA' : 'FURGON',
        'TTE CARGA C/HIDROGRU' : 'CAMION',
        'CHAS.C/CAB C/CAJA CERRADA' : 'CHASIS CON CABINA',
        'FURG.VIDRIADO C/ASIENTOS.' : 'FURGON',
        'SYDER' : 'NO DEFINIDO',
        'CAMION C/PLATO C/HIDROGRUA' : 'CAMION',
        'AUTOMOVIL PLATAF.2 P' : 'SEDAN',
        'PICK-UP CAJA ABIERTA' : 'PICK-UP',
        'TRANS.DE PASAJ(USO ESCOLAR)' : 'UTILITARIO',
        'CHA C/CAB C/ CAJA SIDER' : 'CHASIS CON CABINA',
        'C C/ CAB C/ FURG ISOTERMICO' : 'CHASIS CON CABINA',
        'SEDAN 4PUERTAS' : 'SEDAN',
        'FURGON  VID C/ASIENTOS' : 'FURGON',
        'CAMION CON CAJA SIDER' : 'CAMION',
        'FURGON C/CAJA TERMIC' : 'FURGON',
        'CABINA SIMPLE FRIGORIFICO' : 'CHASIS CON CABINA',
        'SEMIRREMOLQUE FRIGORIFICO' : 'ACOPLADO',
        'CHASIS C/CAB CON C/ABIERTA' : 'CHASIS CON CABINA',
        'FURGON 3000 VID C/ ASIENTOS' : 'FURGON',
        'RURAL 2 PTAS.' : 'RURAL',
        'FURGON VID. CAJA CERRADA' : 'FURGON',
        'CHASIS C/ CAB C/ CAJ PLA' : 'CHASIS CON CABINA',
        'BERLINA 3TAS. AA' : 'SEDAN',
        'CAMION CAB. SIM. Y CAJA AB.' : 'CAMION',
        'FURGONETA C/ VIDRIOS' : 'FURGON',
        'RURAL TROOPER' : 'RURAL',
        'CHASIS C/CAB SIM C/CAJ ABI' : 'CHASIS CON CABINA',
        'CAMION PLAYO C/ HIDROG' : 'CAMION',
        'FURGON/VID/C/ASIENTOS' : 'FURGON',
        'FURGON MIXTO (5 PLAZAS)' : 'FURGON',
        'BERLINA 4  PTAS' : 'SEDAN',
        'RURAL 5' : 'RURAL',
        'FURGON VID C/ASIENT' : 'FURGON',
        'SEMI/TANQUE' : 'ACOPLADO',
        'SEDAN 5 PUERRTAS' : 'SEDAN',
        'FURGONVIDC/ASIENTOS' : 'FURGON',
        'FURGON VIDRIADO C/ASIENTO TR' : 'FURGON',
        'PICK-UP CAB SIMPLE' : 'PICK-UP',
        'FURGON  600' : 'FURGON',
        'SEDAN 5  PUERTAS' : 'SEDAN',
        'MOTORHOME' : 'MOTORHOME',
        'GRUA' : 'GRUA',
        'SEDAN  3 PUERTAS' : 'SEDAN',
        'SEDAN  4 PUERTAS' : 'SEDAN',
        'FURGON  VIDRIADO C/ASIENTOS'   : 'FURGON',
        'BERLINA  5 PUERTAS' : 'SEDAN',
        'FURGON  VIDRIADO' : 'FURGON',
        'SEDAN 4  PUERTAS' : 'SEDAN',
        'SEDAN 3  PUERTAS' : 'SEDAN',
        'BERLINA  5 PTAS' : 'SEDAN',
        'SEDAN  5 PUERTAS' : 'SEDAN',
        'FURGON  C/ ASIENTOS' : 'FURGON',
        'FURGON  3550' : 'FURGON',
        'AUTOMOVIL COMBI II' : 'SEDAN',
        'CHASIS C/CAB Y CAJ VOLCADORA' : 'CHASIS CON CABINA',
        'AUTOMOVIL 5 PUERTAS' : 'SEDAN',
        'BERLINA  4 PTAS' : 'SEDAN',
        'FURGON  600 VIDRIADO CON A/' : 'FURGON',
        'RURAL 4  PTAS' : 'RURAL',
        'FURGON VIDRIADO  C/ASIENTOS' : 'FURGON',
        'CHASIS C/CAB C/CAJA  ABIERTA' : 'CHASIS CON CABINA',
        'TRANSPORTE  DE CARGA' : 'CAMION',
        'CAMION C/CAJA VOLCAD' : 'CAMION',
        'SEDAN  2 PUERTAS' : 'SEDAN',
        'CAJA  MUDANCERA C/ LONA' : 'CHASIS CON CABINA',
        'FURGONETA  CON ASIENTOS' : 'FURGON',
        'COUPE 2 P. KF/R8' : 'COUPE',
        'CAMION A CAJA ABIERTA' : 'CAMION',
        'FURGON  800' : 'FURGON',
        'SEDAN  3 PTAS' : 'SEDAN',
        'SEDAN 2  PUERTAS' : 'SEDAN',
        'CAMION  C/PLAT PORT VEHIC.' : 'CAMION',
        'RURAL 4  PUERTAS' : 'RURAL',
        'FURGON  C/EQUIPO DE FRIO' : 'FURGON',
        'FURGON    800' : 'FURGON',
        'TRACTOR  C/CABINA DORMITORIO' : 'TRACTOR',
        'FURG VIDR CON ASIENT' : 'FURGON',
        'FURGON  VIDR. C/ASIENTOS' : 'FURGON',
        'FURGON  VIDRIADO  C/ASIENTOS' : 'FURGON',
        'CAMION TISOF CC ISO C/EQ F' : 'CAMION',
        'TREN' : 'TREN',
        'SEDAN  4 PTAS' : 'SEDAN',
        'CAJA  MUDANCERA' : 'CHASIS CON CABINA',
        'CHASIS C/CAB P/CAMIO' : 'CHASIS CON CABINA',
        'FURGON  VID C/ASIENTOS' : 'FURGON',
        'FURGON MIXTO (5 PLAZAS)' : 'FURGON',
        'BERLINA 4  PTAS' : 'SEDAN'

    }

    # Aplicar correcciones
    tipo_vehiculo_corregidos = marcas.replace(correcciones)

    return tipo_vehiculo_corregidos

# Aplicar la función y actualizar la columna
df_clean['automotor_tipo_descripcion'] = agrupar_tipo_vehiculo(df_clean, 'automotor_tipo_descripcion')


# Corrección tramite_tipo
df_clean['tramite_tipo'] = df_clean['tramite_tipo'].replace({
    'DENUNCIA DE ROBO O HURTO / RETENCION INDEBIDA': 'DENUNCIA DE ROBO O HURTO'
})


# Corrección registro_seccional_provincia
df_clean['registro_seccional_provincia'] = df_clean['registro_seccional_provincia'].replace({
    'Ciudad Autónoma de Bs.As.': 'Ciudad Autónoma de Buenos Aires'
})


# Corrección titular_domicilio_provincia
df_clean['titular_domicilio_provincia'] = df_clean['titular_domicilio_provincia'].replace({
    'C.AUTONOMA DE BS.AS': 'Ciudad Autónoma de Buenos Aires',
    'T.DEL FUEGO': 'Tierra del Fuego',
    'SGO.DEL ESTERO': 'Santiago del Estero',
    'CÓRDOBA': 'CORDOBA',
    'RÍO NEGRO': 'Río Negro',
    'CIUDAD AUTÓNOMA DE BUENOS AIRES': 'Ciudad Autónoma de Buenos Aires'
})


def limpiar_texto(texto):
    if isinstance(texto, str):
        # Eliminar tildes
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        # Poner en mayúsculas
        texto = texto.upper()
    return texto

# Aplicar a las columnas deseadas
columnas_a_normalizar = [
    'tramite_tipo',
    'registro_seccional_provincia',
    'titular_domicilio_provincia'
]

for col in columnas_a_normalizar:
    df_clean[col] = df_clean[col].apply(limpiar_texto)


# Explorar valores únicos de las columnas solicitadas
print("Tipos de trámite (tramite_tipo):")
print(df_clean['tramite_tipo'].unique())
print("\n")

print("Provincias (registro_seccional_provincia):")
print(df_clean['registro_seccional_provincia'].unique())
print("\n")

print("Provincias (titular_domicilio_provincia):")
print(df_clean['titular_domicilio_provincia'].unique())
print("\n")

print("Marcas de auto (automotor_marca_descripcion):")
print(df_clean['automotor_marca_descripcion'].unique())
print("\n")

# Mostrar todos los valores únicos completos de automotor_tipo_descripcion
print(df_clean['automotor_tipo_descripcion'].value_counts().index.tolist())
print("\n")


print("Géneros de titulares (titular_genero):")
print(df_clean['titular_genero'].unique())
print("\n")

# Lista de marcas en mayúsculas
marcas = df_clean['automotor_marca_descripcion'].dropna().str.upper().unique().tolist()

# Función para eliminar la marca solo si está al inicio
def quitar_marca_si_es_primera(row):
    modelo = str(row['automotor_modelo_descripcion'])
    palabras = modelo.split()
    if palabras and palabras[0].upper() in marcas:
        palabras = palabras[1:]  # elimina solo la primera palabra si es una marca
    return ' '.join(palabras)

# Aplica la función y guarda el modelo sin la marca
df_clean['modelo_sin_marca'] = df_clean.apply(quitar_marca_si_es_primera, axis=1)

# Ahora toma la primera palabra del modelo limpio
df_clean['automotor_modelo_simple'] = df_clean['modelo_sin_marca'].str.split().str[0]

# Contar los modelos simplificados más comunes
modelo_counts = df_clean['automotor_modelo_simple'].value_counts().head(20)  # Top 20

# Graficar los 20 modelos mas robados
plt.figure(figsize=(12, 6))
modelo_counts.plot(kind='bar')
plt.title('Top 20 Modelos de Vehículos (simplificados)')
plt.xlabel('Modelo simplificado')
plt.ylabel('Cantidad')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Contar los tipos de vehículos más comunes
tipo_vehiculo_counts = df_clean['automotor_tipo_descripcion'].value_counts()  # Contamos los tipos de vehículos

# Graficar los tipos de vehiculos mas robados
plt.figure(figsize=(12, 6))
tipo_vehiculo_counts.plot(kind='bar')
plt.title('Frecuencia de Tipos de Vehículos')
plt.xlabel('Tipo de Vehículo')
plt.ylabel('Cantidad')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Graficar cantidad de robos por año
plt.figure(figsize=(10, 6))
sns.countplot(x='tramite_anio', data=df_clean, palette='viridis')
plt.title('Cantidad de robos por año')
plt.xlabel('Año')
plt.ylabel('Cantidad de robos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Agrupamos por año y mes, y contamos cantidad de registros
robos_mensuales = df_clean.groupby(['tramite_anio', 'tramite_mes']).size().reset_index(name='cantidad_robos')

# Gráfico de líneas
plt.figure(figsize=(12, 7))
sns.lineplot(data=robos_mensuales, x='tramite_mes', y='cantidad_robos', hue='tramite_anio', palette='tab10', marker='o')

plt.title('Cantidad de robos por mes, separados por año')
plt.xlabel('Mes')
plt.ylabel('Cantidad de robos')
plt.xticks(ticks=range(1, 13), labels=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                                       'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
plt.legend(title='Año', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

#ESTA SECCION DE CODIGO DEBAJO SE UTILIZO PARA OBTENER COORDENADAS DE LAS SECCIONALES
"""
#registro_seccional_descripcion valores únicos
# Imprimir los valores únicos en líneas separadas
for value in df_clean['registro_seccional_descripcion'].value_counts().index.tolist():
    print(value)

# Cargar el archivo
with open(r"F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\raw\Seccionales\direccion_seccionales_limpias.txt", "r", encoding="utf-8") as f:
    lineas = f.readlines()

# Limpiar y separar datos
registros = []
for linea in lineas:
    linea = linea.strip()
    if not linea:
        continue
    try:
        seccional, resto = linea.split(":", 1)
        direccion_partes = resto.split(",")
        direccion = direccion_partes[0].strip()
        localidad = direccion_partes[1].strip()
        cp = direccion_partes[2].strip() if len(direccion_partes) > 2 else None
        registros.append({
            "seccional": seccional,
            "direccion": direccion,
            "localidad": localidad,
        })
    except:
        print("Línea con error:", linea)

# Convertir a DataFrame
df_seccionales = pd.DataFrame(registros)

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re

# Inicializar geolocalizador con timeout aumentado
geolocator = Nominatim(user_agent="robos-app", timeout=5)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def limpiar_direccion(direccion):
    if not isinstance(direccion, str):
        return ''

    direccion = direccion.upper()  # Uniformar en mayúsculas para los regex

    # Limpiar múltiples espacios y comas redundantes
    direccion = re.sub(r'\s{2,}', ' ', direccion)  # espacios duplicados
    direccion = re.sub(r'\s+,', ',', direccion)    # espacio antes de coma
    direccion = re.sub(r',\s+', ',', direccion)    # coma seguida de espacio

    return direccion.strip()

# Aplicar limpieza
df_seccionales["direccion_limpia"] = df_seccionales["direccion"].apply(limpiar_direccion)

# Crear nueva dirección completa con limpieza
df_seccionales["direccion_completa_limpia"] = (
    df_seccionales["direccion_limpia"] + ", " +
    df_seccionales["localidad"] + ", Argentina"
)

# Función segura para geocodificar con manejo de errores
def geocodificar_direccion(direccion):
    try:
        return geocode(direccion)
    except Exception as e:
        print(f"Error al geocodificar '{direccion}': {e}")
        return None

# Aplicar función fila por fila
df_seccionales["location"] = df_seccionales["direccion_completa_limpia"].apply(geocodificar_direccion)
df_seccionales["lat"] = df_seccionales["location"].apply(lambda loc: loc.latitude if loc else None)
df_seccionales["lon"] = df_seccionales["location"].apply(lambda loc: loc.longitude if loc else None)


# Ver algunas filas para ver si hay latitud y longitud
print(df_seccionales[['direccion_completa_limpia', 'lat', 'lon']].head(10))

# Ver cuántas filas tienen coordenadas válidas
print("Filas con coordenadas válidas:", df_seccionales[['lat', 'lon']].notnull().all(axis=1).sum())

# Ver cuántas filas no pudieron ser geocodificadas
print("Filas con errores (sin coordenadas):", df_seccionales[['lat', 'lon']].isnull().any(axis=1).sum())


df_seccionales.to_csv(r'F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\processed\seccionales_geolocalizadas.csv', index=False)

# Uniformar claves para el merge
df_clean['seccional_normalizada'] = df_clean['registro_seccional_descripcion'].str.strip().str.upper()
df_seccionales['seccional_normalizada'] = df_seccionales['seccional'].str.strip().str.upper()

df_clean = df_clean.merge(
    df_seccionales[['seccional_normalizada', 'lat', 'lon']],
    on='seccional_normalizada',
    how='left'
)

df_clean['coordenadas'] = df_clean.apply(
    lambda row: (row['lat'], row['lon']) if pd.notnull(row['lat']) and pd.notnull(row['lon']) else None,
    axis=1
)

total_con_coordenadas = df_clean['coordenadas'].notnull().sum()
total_sin_coordenadas = df_clean['coordenadas'].isnull().sum()

print("Filas con coordenadas:", total_con_coordenadas)
print("Filas sin coordenadas:", total_sin_coordenadas)

df_clean.to_csv(r'F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\processed\df_clean_con_coordenadas.csv', index=False)
"""

#Leer dataset con coordenadas
df_clean_coord = pd.read_csv(r'F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\processed\df_clean_con_coordenadas.csv',
    dtype={"titular_genero": str},low_memory=False)


gdf_departamentos = gpd.read_file(r"F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\raw\departamentos.geojson")
gdf_provincias = gpd.read_file(r"F:\Portfolio Data Science\Robos vehiculos\data-science-portfolio\data\raw\provincias.geojson")

df_clean_coord = df_clean_coord.dropna(subset=['lat', 'lon'])

import folium
from folium.plugins import MarkerCluster



# Simplificar geometrías para mejorar rendimiento (ajustá tolerance si querés)
gdf_provincias['geometry'] = gdf_provincias['geometry'].simplify(tolerance=0.01, preserve_topology=True)
gdf_departamentos['geometry'] = gdf_departamentos['geometry'].simplify(tolerance=0.005, preserve_topology=True)

# Crear mapa base centrado en Argentina
m = folium.Map(location=[-34.6, -58.4], zoom_start=5, tiles='cartodbpositron')

# Agregar provincias con polígono grueso y colores suaves + tooltip
folium.GeoJson(
    gdf_provincias,
    name='Provincias',
    style_function=lambda feature: {
        'fillColor': '#b3cde3',
        'color': '#03396c',
        'weight': 3,
        'fillOpacity': 0.2,
    },
    tooltip=folium.GeoJsonTooltip(fields=['nam'], aliases=['Provincia:'])
).add_to(m)

# Agregar departamentos con polígono más fino y tooltip con nombre
folium.GeoJson(
    gdf_departamentos,
    name='Departamentos',
    style_function=lambda feature: {
        'fillColor': '#f7f7f7',
        'color': '#6497b1',
        'weight': 1,
        'fillOpacity': 0,
    },
    tooltip=folium.GeoJsonTooltip(fields=['nam'], aliases=['Departamento:'])
).add_to(m)

# Clustering para puntos (usá tu df_clean_coord)
marker_cluster = MarkerCluster(name='Robos Vehículos').add_to(m)

for idx, row in df_clean_coord.iterrows():
    if pd.notnull(row['lat']) and pd.notnull(row['lon']):
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            popup=f"ID: {idx}"
        ).add_to(marker_cluster)

# Control de capas para activar/desactivar provincias, departamentos y puntos
folium.LayerControl().add_to(m)

# Guardar mapa
m.save("mapa_argentina_provincias_departamentos_cluster.html")













