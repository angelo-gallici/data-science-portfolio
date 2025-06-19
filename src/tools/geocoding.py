import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def limpiar_direccion(direccion):
    if not isinstance(direccion, str):
        return ''
    direccion = direccion.upper()
    direccion = re.sub(r'\s{2,}', ' ', direccion)
    direccion = re.sub(r'\s+,', ',', direccion)
    direccion = re.sub(r',\s+', ',', direccion)
    return direccion.strip()

def geocodificar_seccionales(txt_path, output_csv):
    with open(txt_path, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    registros = []
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        try:
            seccional, resto = linea.split(":", 1)
            partes = resto.split(",")
            direccion = partes[0].strip()
            localidad = partes[1].strip()
            registros.append({
                "seccional": seccional.strip(),
                "direccion": direccion,
                "localidad": localidad,
            })
        except Exception as e:
            print(f"Error en línea: {linea}")

    df = pd.DataFrame(registros)
    df["direccion_limpia"] = df["direccion"].apply(limpiar_direccion)
    df["direccion_completa_limpia"] = df["direccion_limpia"] + ", " + df["localidad"] + ", Argentina"

    print("Geocodificando...")
    geolocator = Nominatim(user_agent="robos-app", timeout=5)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    df["location"] = df["direccion_completa_limpia"].apply(lambda x: geocode(x))
    df["lat"] = df["location"].apply(lambda loc: loc.latitude if loc else None)
    df["lon"] = df["location"].apply(lambda loc: loc.longitude if loc else None)
    df["seccional_normalizada"] = df["seccional"].str.strip().str.upper()

    df[['seccional_normalizada', 'lat', 'lon']].to_csv(output_csv, index=False)
    print(f"Coordenadas guardadas en {output_csv}")

if __name__ == "__main__":
    TXT_INPUT = "data/raw/Seccionales/direccion_seccionales_limpias.txt"
    OUTPUT_CSV = "data/processed/seccionales_geolocalizadas.csv"
    geocodificar_seccionales(TXT_INPUT, OUTPUT_CSV)
