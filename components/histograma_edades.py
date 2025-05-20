# components/histograma_edades.py

import pandas as pd
import plotly.express as px
from dash import html, dcc
from utils.data_loader import load_data

def preparar_histograma(df):
    """
    Agrupa los datos por rango de edad y retorna un DataFrame con total de muertes por grupo.
    """
    df_grouped = (
        df[df['RANGO_EDAD'].notnull()]
        .groupby('RANGO_EDAD')
        .size()
        .reset_index(name='TOTAL')
    )
    return df_grouped

def get_layout():
    """
    Carga los datos y retorna el layout con el histograma de muertes por edad.
    """
    df_muertes, _ = load_data()
    df_histograma = preparar_histograma(df_muertes)

    orden_quinquenal = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
        "75-79", "80-84", "85+"
    ]

    df_histograma['RANGO_EDAD'] = pd.Categorical(
        df_histograma['RANGO_EDAD'], categories=orden_quinquenal, ordered=True
    )
    df_histograma = df_histograma.sort_values('RANGO_EDAD')

    fig = px.bar(
        df_histograma,
        x='RANGO_EDAD',
        y='TOTAL',
        labels={'RANGO_EDAD': 'Rango de edad', 'TOTAL': 'Número de muertes'},
        title='Distribución de muertes por rango de edad quinquenal'
    )

    fig.update_layout(
        yaxis=dict(range=[0, 10000])
    )

    return html.Div([
        html.H3("Distribución de muertes por edades (quinquenal)"),
        dcc.Graph(figure=fig)
    ])
