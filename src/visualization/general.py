import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_robos_por_anio(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='tramite_anio', data=df, palette='viridis', ax=ax)
    ax.set_title('Cantidad de robos por año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Cantidad de robos')
    ax.tick_params(axis='x', rotation=45)
    return fig

def plot_robos_mensuales(df):
    robos_mensuales = df.groupby(['tramite_anio', 'tramite_mes']).size().reset_index(name='cantidad_robos')

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.lineplot(data=robos_mensuales, x='tramite_mes', y='cantidad_robos',
                 hue='tramite_anio', palette='tab10', marker='o', ax=ax)
    
    ax.set_title('Cantidad de robos por mes, separados por año')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad de robos')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    ax.legend(title='Año', bbox_to_anchor=(1.05, 1), loc='upper left')
    return fig
