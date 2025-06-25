# 🚘 Análisis de Robos de Vehículos en Argentina (2018-2025)

Este proyecto analiza los robos de vehículos registrados por la DNRPA en Argentina. Se utiliza Python, Streamlit y visualizaciones interactivas para detectar patrones temporales, geográficos y de tipo de vehículo.

## Estructura del proyecto
```
data-science-portfolio/
├── app/
│   └── dashboard.py               # App principal de Streamlit
│
├── data/
│   ├── raw/                       # Dataset original (CSV, GeoJSON, etc.)
│   └── processed/                 # Archivos ya limpios y con coordenadas
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py              # Funciones para cargar y guardar datos
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── cleaning.py            # Funciones para limpiar y normalizar
│   │   └── validation.py          # Validaciones de columnas, nulos, tipos
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── general.py             # Gráficos generales de evolución
│   │   ├── mapa.py                # Gráficos y mapas con folium
│   │   ├── titulares.py           # Edad de titulares y antigüedad de autos
│   │   └── vehiculos.py           # Marcas, modelos y tipos de vehículos
│
├── tools/
│   └── geocoding.py               # Script que genera lat/lon con geopy
│
├── main.py                        # Script que ejecuta todo el ETL
├── requirements.txt               # Librerías y sus versiones
├── README.md                      # Descripción del proyecto, cómo correrlo
├── .gitignore                     # Archivos a excluir del repositorio
├── .gitattributes                 # Config Git opcional (normalización EOL)
└── LICENCE                        # Tipo de licencia 
```

## Tecnologías utilizadas

- Python 3.x
- Pandas, Geopandas, NumPy
- Folium
- Matplotlib, Seaborn
- Streamlit

## ¿Qué incluye?

- Mapa interactivo de robos por año
- Evolución de robos por año y mes
- Top 10 marcas y modelos más robados
- Tipos de vehículos más robados
- Edad de los titulares
- Año de fabricación de los vehículos

## Cómo comenzar

1. Clona este repositorio.

git clone https://github.com/angelo-gallici/data-science-portfolio.git
cd data-science-portfolio

2. Crea y activa un entorno virtual:
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate # Windows

## Crear un entorno virtual:

python -m venv venv

## Activar el entorno virtual:

Windows: .\venv\Scripts\activate
Linux/Mac: source venv/bin/activate

## Instala las dependencias:

pip install -r requirements.txt

## Procesar los datos (solo una vez)

python -m src.main

## Ejecutar el dashboard

streamlit run app/dashboard.py

## Licencia

Este proyecto está bajo la licencia MIT.

