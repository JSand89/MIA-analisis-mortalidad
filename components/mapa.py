# components/mapa.py

import pandas as pd
import plotly.express as px
from dash import html, dcc
from utils.data_loader import load_data, load_geojson_departamentos

# Cargar datos y geojson
df_muertes, df_divipola = load_data()
geojson = load_geojson_departamentos()

def preparar_datos_mapa(df, df_divipola):
    """
    Agrupa el total de muertes por departamento y une con nombres y códigos DANE.
    Retorna un DataFrame con COD_DEP_STR y TOTAL.
    """
    # Agrupar por código de departamento
    df_grouped = df.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL')

    # Unir con nombres desde DIVIPOLA
    df_nombres = df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates()
    df_grouped = df_grouped.merge(df_nombres, on='COD_DEPARTAMENTO', how='left')

    # Codificar como string de 2 dígitos
    df_grouped['COD_DEP_STR'] = df_grouped['COD_DEPARTAMENTO'].astype(str).str.zfill(2)

    return df_grouped

# Preparar datos
df_mapa = preparar_datos_mapa(df_muertes, df_divipola)

# Crear gráfico coroplético
fig = px.choropleth(
    df_mapa,
    geojson=geojson,
    locations='COD_DEP_STR',
    color='TOTAL',
    hover_name='DEPARTAMENTO',
    featureidkey="properties.DPTO_CCDGO",  # ← asegurado desde tu geojson
    projection="mercator",
    color_continuous_scale="Reds"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title="Total de muertes por departamento (2019)",
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

# Layout para insertar en la app
layout = html.Div([
    html.H3("Distribución de muertes por departamento"),
    dcc.Graph(figure=fig)
])
