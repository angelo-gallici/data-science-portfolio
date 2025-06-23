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

    print("Limpiando y normalizando datos...")
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