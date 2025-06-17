import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

def generar_mapa_por_anio(df_coord, gdf_provincias, gdf_departamentos, anio):
    # Filtrar por año
    df_anio = df_coord[df_coord['tramite_anio'] == anio]

    # Crear mapa base
    m = folium.Map(location=[-34.6, -58.4], zoom_start=5, tiles='cartodbpositron')

    # Simplificar geometrías
    gdf_provincias['geometry'] = gdf_provincias['geometry'].simplify(tolerance=0.01, preserve_topology=True)
    gdf_departamentos['geometry'] = gdf_departamentos['geometry'].simplify(tolerance=0.005, preserve_topology=True)

    # Provincias
    folium.GeoJson(
        gdf_provincias,
        name='Provincias',
        style_function=lambda feature: {
            'fillColor': '#b3cde3',
            'color': '#03396c',
            'weight': 3,
            'fillOpacity': 0.2,
        },
        tooltip=folium.GeoJsonTooltip(fields=['nam'], aliases=['Provincia:'])
    ).add_to(m)

    # Departamentos
    folium.GeoJson(
        gdf_departamentos,
        name='Departamentos',
        style_function=lambda feature: {
            'fillColor': '#f7f7f7',
            'color': '#6497b1',
            'weight': 1,
            'fillOpacity': 0,
        },
        tooltip=folium.GeoJsonTooltip(fields=['nam'], aliases=['Departamento:'])
    ).add_to(m)

    # Marcadores
    marker_cluster = MarkerCluster(name='Robos Vehículos').add_to(m)

    for _, row in df_anio.iterrows():
        if pd.notnull(row['lat']) and pd.notnull(row['lon']):
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=3,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.7,
                popup=f"{row['automotor_marca_descripcion']} - {row['automotor_modelo_descripcion']}"
            ).add_to(marker_cluster)

    folium.LayerControl().add_to(m)

    return m
