# components/barras_violencia.py

import pandas as pd
import plotly.express as px
from dash import html, dcc
from utils.data_loader import load_data

# Cargar datos
df_muertes, df_divipola = load_data()

def filtrar_homicidios_armas(df_muertes, df_divipola):
    """
    Filtra homicidios por armas de fuego (X93, X94, X95), agrupa por COD_DANE, 
    une con nombre del municipio y retorna el top 5.
    """

    # Filtrar homicidios con arma de fuego
    df = df_muertes[df_muertes['COD_MUERTE'].notnull()].copy()
    df['COD_MUERTE'] = df['COD_MUERTE'].astype(str).str.strip()
    homicidios = df[df['COD_MUERTE'].str.startswith(('X93', 'X94', 'X95'))]

    # Agrupar por COD_DANE (clave única nacional del municipio)
    df_grouped = homicidios.groupby('COD_DANE').size().reset_index(name='TOTAL')

    # Unir con nombre del municipio
    municipios_unicos = df_divipola[['COD_DANE', 'MUNICIPIO']].drop_duplicates('COD_DANE')
    df_grouped = df_grouped.merge(municipios_unicos, on='COD_DANE', how='left')

    # Ordenar y tomar top 5
    df_top5 = df_grouped.sort_values(by='TOTAL', ascending=False).head(5)

    return df_top5



# Preparar datos
df_violencia = filtrar_homicidios_armas(df_muertes, df_divipola)

# Crear gráfico
fig = px.bar(
    df_violencia,
    x='MUNICIPIO',
    y='TOTAL',
    title='Top 5 ciudades con más homicidios por armas de fuego (X93–X95)',
    labels={'MUNICIPIO': 'Ciudad', 'TOTAL': 'Número de homicidios'}
)

# Layout
layout = html.Div([
    html.H3("Ciudades más violentas por homicidio con armas de fuego"),
    dcc.Graph(figure=fig)
])
