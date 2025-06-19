import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_edad_titulares(df):
    df = df.copy()
    # Convertir 'titular_anio_nacimiento' a numérico, forzando NaN en errores
    df['titular_anio_nacimiento'] = pd.to_numeric(df['titular_anio_nacimiento'], errors='coerce')

    # Calcular edad
    df['edad'] = df['tramite_anio'] - df['titular_anio_nacimiento']

    # Filtrar edades razonables
    df = df[(df['edad'] > 0) & (df['edad'] < 100)]

    plt.figure(figsize=(10, 6))
    sns.histplot(df['edad'], bins=30, kde=True, color='skyblue')
    plt.title('Distribución de Edad de los Titulares')
    plt.xlabel('Edad')
    plt.ylabel('Cantidad')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return plt

def plot_anio_vehiculos(df):
    df = df.copy()
    df = df[df['automotor_anio_modelo'].notna()]
    df['automotor_anio_modelo'] = df['automotor_anio_modelo'].astype(int)
    
    top_años = df['automotor_anio_modelo'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_años.index, y=top_años.values, color='coral')
    plt.title('Cantidad de Robos por Año de Fabricación del Vehículo')
    plt.xlabel('Año del Modelo')
    plt.ylabel('Cantidad de Robos')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return plt
