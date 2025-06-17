import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import geopandas as gpd
from src.visualization.mapa import generar_mapa_por_anio

st.set_page_config(layout="wide")

st.title("🚗 Mapa de Robos de Vehículos en Argentina")

# Cargar datos
df_coord = pd.read_csv("data/processed/df_clean_con_coordenadas.csv", dtype={"titular_genero": str}, low_memory=False)
df_coord = df_coord.dropna(subset=['lat', 'lon'])
df_coord['tramite_anio'] = df_coord['tramite_anio'].astype(int)

gdf_provincias = gpd.read_file("data/raw/provincias.geojson")
gdf_departamentos = gpd.read_file("data/raw/departamentos.geojson")

# Año seleccionable
anios_disponibles = sorted(df_coord['tramite_anio'].dropna().unique())
anio_seleccionado = st.selectbox("Seleccioná un año", anios_disponibles, index=len(anios_disponibles)-1)

# Generar mapa
mapa = generar_mapa_por_anio(df_coord, gdf_provincias, gdf_departamentos, anio_seleccionado)

# Mostrar mapa
components.html(mapa._repr_html_(), height=700, width=1000)
