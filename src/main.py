from pathlib import Path
import pandas as pd
from src.data.loader import load_raw_data, save_clean_data
from src.processing.cleaning import limpiar_datos
from src.processing.validation import validar_datos

# Definir directorio base: dos niveles arriba del script main.py
BASE_DIR = Path(__file__).resolve().parent.parent  # Esto apunta a la carpeta raíz del proyecto

# Construir rutas absolutas a los archivos
RAW_PATH = BASE_DIR / "data" / "raw" / "Dataset Historico" / "dnrpa-robos-recuperos-autos-historico.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "df_clean_con_coordenadas.csv"
COORDS_PATH = BASE_DIR / "data" / "processed" / "seccionales_geolocalizadas.csv"

def main():
    print("Cargando datos...")
    # pandas acepta Path directamente en versiones recientes, si no usa str()
    df = load_raw_data(RAW_PATH)

    print("🧹 Limpiando y normalizando datos...")
    df_clean = limpiar_datos(df)

    print("Validando datos...")
    validar_datos(df_clean)

    print("Agregando coordenadas geográficas...")
    if not COORDS_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo de coordenadas: {COORDS_PATH}. Ejecutá primero el script de geocodificación.")

    df_coords = pd.read_csv(COORDS_PATH)
    df_clean['seccional_normalizada'] = df_clean['registro_seccional_descripcion'].str.strip().str.upper()
    df_coords['seccional_normalizada'] = df_coords['seccional'].str.strip().str.upper()

    df_clean = df_clean.merge(df_coords, on='seccional_normalizada', how='left')

    df_clean['coordenadas'] = df_clean.apply(
        lambda row: (row['lat'], row['lon']) if pd.notnull(row['lat']) and pd.notnull(row['lon']) else None,
        axis=1
    )

    print("Guardando datos procesados con coordenadas...")
    save_clean_data(df_clean, PROCESSED_PATH)
    print(f"Datos finales guardados en {PROCESSED_PATH}")

if __name__ == "__main__":
    main()





















"""
#ESTA SECCION DE CODIGO DEBAJO SE UTILIZO PARA OBTENER COORDENADAS DE LAS SECCIONALES

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