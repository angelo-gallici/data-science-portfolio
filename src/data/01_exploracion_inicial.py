# Importar librerías
import pandas as pd

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


