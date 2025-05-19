# components/eda_tab.py

import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table
from utils.data_loader import load_data

# Cargar datos
df_muertes, _ = load_data()

# Tabla: primeras filas
preview_table = dash_table.DataTable(
    data=df_muertes.head(10).to_dict('records'),
    columns=[{"name": col, "id": col} for col in df_muertes.columns],
    style_table={'overflowX': 'auto'},
    style_cell={'textAlign': 'left', 'minWidth': '100px', 'whiteSpace': 'normal'}
)

# Lista de columnas
column_list = html.Ul([html.Li(col) for col in df_muertes.columns])

# Conteo de nulos
nulos = df_muertes.isnull().sum().reset_index()
nulos.columns = ['Columna', 'Valores Nulos']
nulos_table = dash_table.DataTable(
    data=nulos.to_dict('records'),
    columns=[{"name": i, "id": i} for i in nulos.columns],
    style_table={'overflowX': 'auto'},
    style_cell={'textAlign': 'left'}
)

# Gráfico: muertes por sexo
df_sexo = df_muertes['SEXO'].value_counts().reset_index()
df_sexo.columns = ['Sexo', 'Total']
sexo_fig = px.bar(df_sexo, x='Sexo', y='Total', title='Distribución por sexo')

# Layout exportable
layout = html.Div([
    html.H3("Exploración de Datos - Mortalidad 2019"),
    
    html.H4("Primeras filas de los datos"),
    preview_table,
    
    html.H4("Columnas disponibles"),
    column_list,
    
    html.H4("Conteo de valores nulos por columna"),
    nulos_table,

    html.H4("Distribución de muertes por sexo"),
    dcc.Graph(figure=sexo_fig)
])
