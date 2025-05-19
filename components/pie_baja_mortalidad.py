# components/pie_baja_mortalidad.py

import pandas as pd
import plotly.express as px
from dash import html, dcc
from utils.data_loader import load_data

# Cargar datos
df_muertes, df_divipola = load_data()

def ciudades_con_menos_muertes(df_muertes, df_divipola):
    """
    Agrupa por municipio (COD_DANE) y devuelve las 10 con menor número de muertes,
    excluyendo municipios sin nombre.
    """
    df_grouped = df_muertes.groupby('COD_DANE').size().reset_index(name='TOTAL')
    municipios_unicos = df_divipola[['COD_DANE', 'MUNICIPIO']].drop_duplicates('COD_DANE')
    df_grouped = df_grouped.merge(municipios_unicos, on='COD_DANE', how='left')

    # Eliminar municipios sin nombre y filtrar top 10
    df_top10 = (
        df_grouped[df_grouped['TOTAL'] > 0]
        .dropna(subset=['MUNICIPIO'])
        .sort_values(by='TOTAL')
        .head(10)
    )

    return df_top10


# Preparar datos
df_pie = ciudades_con_menos_muertes(df_muertes, df_divipola)

# Crear gráfico
fig = px.pie(
    df_pie,
    values='TOTAL',
    names='MUNICIPIO',
    title='10 ciudades con menor número de muertes en 2019'
)

# Layout
layout = html.Div([
    html.H3("Ciudades con menor mortalidad"),
    dcc.Graph(figure=fig)
])
