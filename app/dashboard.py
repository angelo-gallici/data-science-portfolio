import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import pandas as pd
import geopandas as gpd
import streamlit.components.v1 as components

from src.data.loader import load_clean_data
from src.visualization.general import plot_robos_por_anio, plot_robos_mensuales
from src.visualization.vehiculos import plot_top_marcas, plot_top_modelos, plot_tipos_vehiculo
from src.visualization.titulares import plot_edad_titulares, plot_anio_vehiculos
from src.visualization.mapa import generar_mapa_por_anio


# Configuración general
st.set_page_config(page_title="Análisis de Robos de Vehículos", layout="wide")
st.title("Análisis de Robos de Vehículos en Argentina")

# Cargar datos
df = load_clean_data("data/processed/df_clean_con_coordenadas.csv")
gdf_provincias = gpd.read_file("data/raw/provincias.geojson")
gdf_departamentos = gpd.read_file("data/raw/departamentos.geojson")

# Sidebar
st.sidebar.title("Opciones de Visualización")
anio_seleccionado = st.sidebar.selectbox(
    "Seleccionar año para análisis", 
    sorted(df['tramite_anio'].dropna().unique()),
    index=len(sorted(df['tramite_anio'].dropna().unique())) - 1
)

st.sidebar.markdown("---")
st.sidebar.write("Hecho por Angelo Gallici")
st.sidebar.markdown("Proyecto de Data Science")


# Sección 1: Gráficos generales
st.header("Evolución Temporal de Robos")
col1, col2 = st.columns(2)

with col1:
    st.pyplot(plot_robos_por_anio(df))

with col2:
    st.pyplot(plot_robos_mensuales(df))


# Sección 2: Vehículos más robados
st.header("Vehículos Más Robados")
col3, col4 = st.columns(2)

with col3:
    st.pyplot(plot_top_marcas(df, top_n=10))

with col4:
    st.pyplot(plot_top_modelos(df, top_n=10))

# Tipos de vehículo
st.pyplot(plot_tipos_vehiculo(df))


# Sección 3: Edad y año del auto
st.header("Perfil del Titular y Antigüedad del Vehículo")
col5, col6 = st.columns(2)

with col5:
    st.pyplot(plot_edad_titulares(df))

with col6:
    st.pyplot(plot_anio_vehiculos(df))


# Sección 4: Mapa
st.header("Mapa de Robos por Año")

mapa = generar_mapa_por_anio(df, gdf_provincias, gdf_departamentos, anio_seleccionado)
components.html(mapa._repr_html_(), height=700, width=1000)
