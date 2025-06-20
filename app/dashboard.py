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
st.set_page_config(page_title="Robos de Vehículos en Argentina 2018-2025", layout="wide")
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.title("Análisis de Robos de Vehículos en Argentina")

# Cargar datos
df = load_clean_data("data/processed/df_clean_con_coordenadas.csv")
gdf_provincias = gpd.read_file("data/raw/provincias.geojson")
gdf_departamentos = gpd.read_file("data/raw/departamentos.geojson")

# Sección: Mapa
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.header("Mapa de Robos de Vehículos por Año")

    anio_seleccionado = st.selectbox(
        "Seleccionar año para el análisis", 
        sorted(df['tramite_anio'].dropna().unique()),
        index=len(sorted(df['tramite_anio'].dropna().unique())) - 1,
        key="anio_mapa"
    )

    mapa = generar_mapa_por_anio(df, gdf_provincias, gdf_departamentos, anio_seleccionado)
    components.html(mapa._repr_html_(), height=700, width=1000)


# SECCIÓN 2: Evolución temporal
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.header("Evolución Temporal de Robos")
    st.pyplot(plot_robos_por_anio(df))
    st.pyplot(plot_robos_mensuales(df))

# SECCIÓN 3: Vehículos más robados
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.header("Marcas y Modelos de Vehículos Más Robados")
    anio_filtro = st.selectbox("Seleccioná un año para filtrar (opcional)", ['Todos'] + sorted(df['tramite_anio'].dropna().unique().tolist()), key="anio_vehiculos")
    anio = None if anio_filtro == 'Todos' else anio_filtro
    st.pyplot(plot_top_marcas(df, top_n=10, anio=anio))
    st.pyplot(plot_top_modelos(df, top_n=10, anio=anio))
    st.pyplot(plot_tipos_vehiculo(df, top_n=5, anio=anio))

# SECCIÓN 4: Perfil de titulares y antigüedad
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.header("Perfil del Titular y Antigüedad del Vehículo")
    st.pyplot(plot_edad_titulares(df))
    st.pyplot(plot_anio_vehiculos(df))