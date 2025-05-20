# components/lineas.py

import pandas as pd
import plotly.express as px
from dash import html, dcc
from utils.data_loader import load_data

def preparar_datos_por_mes(df):
    """
    Agrupa el total de muertes por mes.
    Devuelve un DataFrame con columnas: MES, TOTAL.
    """
    df_mes = df.groupby('MES').size().reset_index(name='TOTAL')
    df_mes = df_mes.sort_values(by='MES')
    return df_mes

def get_layout():
    """
    Carga los datos y retorna el layout con el gráfico de líneas.
    """
    df_muertes, _ = load_data()
    df_lineas = preparar_datos_por_mes(df_muertes)

    fig = px.line(
        df_lineas,
        x='MES',
        y='TOTAL',
        markers=True,
        labels={'MES': 'Mes', 'TOTAL': 'Número de muertes'},
        title="Total de muertes por mes en 2019"
    )

    return html.Div([
        html.H3("Muertes por mes en Colombia (2019)"),
        dcc.Graph(figure=fig)
    ])
