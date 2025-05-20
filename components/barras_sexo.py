# components/barras_sexo.py

import pandas as pd
import plotly.express as px
from dash import html, dcc
from utils.data_loader import load_data

def preparar_datos_por_sexo(df_muertes, df_divipola):
    """
    Agrupa los datos por departamento y sexo, y los convierte en un DataFrame para gráfico apilado.
    """
    df_grouped = (
        df_muertes
        .dropna(subset=['SEXO', 'COD_DEPARTAMENTO'])
        .groupby(['COD_DEPARTAMENTO', 'SEXO'])
        .size()
        .reset_index(name='TOTAL')
    )

    departamentos = df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates('COD_DEPARTAMENTO')
    df_grouped = df_grouped.merge(departamentos, on='COD_DEPARTAMENTO', how='left')

    return df_grouped

def get_layout():
    """
    Carga los datos y retorna el layout con los gráficos de barras por sexo.
    """
    df_muertes, df_divipola = load_data()
    df_barras = preparar_datos_por_sexo(df_muertes, df_divipola)

    # Separar según total de muertes
    df_mas_10k = df_barras.groupby('DEPARTAMENTO')['TOTAL'].sum().reset_index()
    departamentos_mas_10k = df_mas_10k[df_mas_10k['TOTAL'] > 10000]['DEPARTAMENTO']

    df_mayores = df_barras[df_barras['DEPARTAMENTO'].isin(departamentos_mas_10k)]
    df_menores = df_barras[~df_barras['DEPARTAMENTO'].isin(departamentos_mas_10k)]

    fig_mayores = px.bar(
        df_mayores,
        x='DEPARTAMENTO',
        y='TOTAL',
        color='SEXO',
        title='Departamentos con más de 10.000 muertes',
        labels={'DEPARTAMENTO': 'Departamento', 'TOTAL': 'Muertes'},
        barmode='stack'
    )

    fig_menores = px.bar(
        df_menores,
        x='DEPARTAMENTO',
        y='TOTAL',
        color='SEXO',
        title='Departamentos con menos de 10.000 muertes',
        labels={'DEPARTAMENTO': 'Departamento', 'TOTAL': 'Muertes'},
        barmode='stack'
    )

    return html.Div([
        html.H3("Comparación de muertes por sexo y departamento"),
        html.H4("Departamentos con más de 10.000 muertes"),
        dcc.Graph(figure=fig_mayores),
        html.H4("Departamentos con menos de 10.000 muertes"),
        dcc.Graph(figure=fig_menores)
    ])
