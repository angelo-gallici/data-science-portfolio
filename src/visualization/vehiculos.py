import matplotlib.pyplot as plt

def plot_top_marcas(df, top_n=10, anio=None):
    df_filtrado = df.copy()
    if anio is not None:
        df_filtrado = df_filtrado[df_filtrado['tramite_anio'] == anio]

    marca_counts = df_filtrado['automotor_marca_descripcion'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(12, 7))
    marca_counts.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title(f'Top {top_n} Marcas Más Robadas' + (f' en {anio}' if anio else ''))
    ax.set_xlabel('Cantidad')
    ax.set_ylabel('Marca')
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    return fig

def plot_top_modelos(df, top_n=10, anio=None):
    df_filtrado = df.copy()
    if anio is not None:
        df_filtrado = df_filtrado[df_filtrado['tramite_anio'] == anio]

    modelo_counts = df_filtrado['automotor_modelo_simple'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(12, 7))
    modelo_counts.plot(kind='bar', ax=ax, color='steelblue')
    ax.set_title(f'Top {top_n} Modelos mas robados' + (f' en {anio}' if anio else ''))
    ax.set_xlabel('Modelo')
    ax.set_ylabel('Cantidad')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig

def plot_tipos_vehiculo(df, top_n=5, anio=None):
    df_filtrado = df.copy()
    if anio is not None:
        df_filtrado = df_filtrado[df_filtrado['tramite_anio'] == anio]

    tipo_counts = df_filtrado['automotor_tipo_descripcion'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(8, 4))
    tipo_counts.plot(kind='bar', ax=ax, color='steelblue')
    ax.set_title(f'Top {top_n} Tipos de Vehículos Más Robados' + (f' en {anio}' if anio else ''))
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Cantidad')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig




"""
import matplotlib.pyplot as plt

def plot_top_marcas(df, top_n=10):
    marca_counts = df['automotor_marca_descripcion'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(12, 7))
    marca_counts.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title(f'Top {top_n} Marcas Más Robadas')
    ax.set_xlabel('Cantidad')
    ax.set_ylabel('Marca')
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    return fig

def plot_top_modelos(df, top_n=10):
    modelo_counts = df['automotor_modelo_simple'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(12, 7))
    modelo_counts.plot(kind='bar', ax=ax)
    ax.set_title(f'Top {top_n} Modelos de Vehículos (simplificados)')
    ax.set_xlabel('Modelo')
    ax.set_ylabel('Cantidad')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig

def plot_tipos_vehiculo(df):
    tipo_counts = df['automotor_tipo_descripcion'].value_counts()

    fig, ax = plt.subplots(figsize=(12, 7))
    tipo_counts.plot(kind='bar', ax=ax)
    ax.set_title('Frecuencia de Tipos de Vehículos')
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Cantidad')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig
"""