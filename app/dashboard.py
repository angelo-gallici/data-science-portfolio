import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import geopandas as gpd
from src.visualization.mapa import generar_mapa_por_anio
from src.visualization.general import plot_robos_por_anio, plot_robos_mensuales
from src.visualization.vehiculos import plot_top_modelos, plot_tipos_vehiculo

# Cargar datos
df = pd.read_csv("data/processed/df_clean_con_coordenadas.csv")

st.title("Análisis de Robos de Vehículos")

if st.checkbox("Ver robos por año"):
    st.pyplot(plot_robos_por_anio(df))

if st.checkbox("Ver robos mensuales"):
    st.pyplot(plot_robos_mensuales(df))

if st.checkbox("Top 10 modelos más robados"):
    st.pyplot(plot_top_modelos(df, top_n=10))

if st.checkbox("Tipos de vehículos más robados"):
    st.pyplot(plot_tipos_vehiculo(df))


st.set_page_config(layout="wide")

st.title("Mapa de Robos de Vehículos en Argentina")

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

import streamlit as st
from src.visualization.titulares import plot_edad_titulares, plot_anio_vehiculos

with st.expander("Edad de los titulares"):
    fig1 = plot_edad_titulares(df)
    st.pyplot(fig1)

with st.expander("Año de los vehículos más robados"):
    fig2 = plot_anio_vehiculos(df)
    st.pyplot(fig2)

