# Importar librerías
import pandas as pd
import matplotlib.pyplot as plt

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

print("Tipos de vehículo (automotor_tipo_descripcion):")
print(df_clean['automotor_tipo_descripcion'].unique())
print("\n")

print("Géneros de titulares (titular_genero):")
print(df_clean['titular_genero'].unique())


