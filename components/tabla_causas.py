# components/tabla_causas.py

import pandas as pd
from dash import html, dash_table
from utils.data_loader import load_data

# Cargar datos
df_muertes, _ = load_data()

def obtener_top_causas(df):
    """
    Agrupa los registros por código de causa y devuelve las 10 principales causas de muerte.
    """
    # Eliminar causas vacías
    df = df[df['CODIGO'].notnull() & df['DESCRIPCION'].notnull()].copy()

    # Agrupar por código + descripción y contar
    df_grouped = (
        df.groupby(['CODIGO', 'DESCRIPCION'])
        .size()
        .reset_index(name='TOTAL')
        .sort_values(by='TOTAL', ascending=False)
        .head(10)
    )

    return df_grouped

# Preparar datos
df_top_causas = obtener_top_causas(df_muertes)

# Crear tabla interactiva
tabla = dash_table.DataTable(
    columns=[
        {'name': 'Código', 'id': 'CODIGO'},
        {'name': 'Descripción', 'id': 'DESCRIPCION'},
        {'name': 'Total de muertes', 'id': 'TOTAL'}
    ],
    data=df_top_causas.to_dict('records'),
    style_cell={'textAlign': 'left', 'padding': '8px'},
    style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
    style_table={'overflowX': 'auto'},
)

# Layout exportable
layout = html.Div([
    html.H3("10 principales causas de muerte en Colombia (2019)"),
    tabla
])
