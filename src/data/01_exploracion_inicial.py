# Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import unicodedata

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
print(df_clean.isnull().sum())
print(f"Nuevo tamaño del dataset: {df_clean.shape}")

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

# Crear una nueva columna automotor_modelo_simple con la primera palabra del modelo
df_clean['automotor_modelo_simple'] = df_clean['automotor_modelo_descripcion'].str.split().str[0]

# Verificamos que se creo bien
#print(df_clean[['automotor_modelo_descripcion', 'automotor_modelo_simple']].head())

# Contar los modelos simplificados más comunes
#modelo_counts = df_clean['automotor_modelo_simple'].value_counts().head(20)  # Top 20
"""
# Graficar
plt.figure(figsize=(12, 6))
modelo_counts.plot(kind='bar')
plt.title('Top 20 Modelos de Vehículos (simplificados)')
plt.xlabel('Modelo simplificado')
plt.ylabel('Cantidad')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
"""

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

print("CORRECCIONES")

# Supongamos que tu DataFrame se llama df_clean
# y la columna con las marcas es 'automotor_marca_descripcion'

def corregir_marcas(df, columna):
    """
    Corrige errores de tipeo y unifica marcas en una columna de DataFrame.

    Args:
        df (pd.DataFrame): El DataFrame con la columna de marcas.
        columna (str): El nombre de la columna con las marcas.

    Returns:
        pd.Series: La columna con las marcas corregidas.
    """

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
    """
    Corrige errores de tipeo y unifica marcas en una columna de DataFrame.

    Args:
        df (pd.DataFrame): El DataFrame con la columna de marcas.
        columna (str): El nombre de la columna con las marcas.

    Returns:
        pd.Series: La columna con las marcas corregidas.
    """

    marcas = df[columna].str.upper().str.strip()  # Convertir a mayúsculas y eliminar espacios

    # Diccionario de correcciones
    correcciones = {
        '': 'SEDAN',
        '': 'RURAL',
        '': 'PICK-UP',
        '': 'FURGON',
        '': 'COUPE',
        '': 'TODOTERRENO',
        '': 'CHASIS CON CABINA',
        '': 'TRACTOR',
        '': 'MINIBUS',
        '': 'UTILITARIO',
        '': 'OMNIBUS',
        '': 'LIMUSINA',
        '': 'CAMION',
        '': 'CASA RODANTE',
        '': 'ACOPLADO',
        '': 'GRUA',
        '': 'NO DEFINIDO',
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
        #HASTA TRANSP. DE PASAJEROS


    }

    # Aplicar correcciones
    tipo_vehiculo_corregidos = marcas.replace(correcciones)

    return tipo_vehiculo_corregidos

# Aplicar la función y actualizar la columna
df_clean['automotor_tipo_descripcion'] = agrupar_tipo_vehiculo(df_clean, 'automotor_tipo_descripcion')


# Imprimir las marcas corregidas
print("Marcas de auto corregidas (automotor_marca_descripcion):")
print(df_clean['automotor_marca_descripcion'].unique())
print("\n")

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


for col in columnas_a_normalizar:
    print(f"Valores únicos en {col}:")
    print(df_clean[col].unique())
    print("\n")



