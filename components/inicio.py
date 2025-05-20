# components/inicio.py

from dash import html

def get_layout():
    return html.Div([
        html.H2("Análisis de Mortalidad en Colombia - 2019"),
        html.P("Bienvenido al dashboard interactivo que analiza los datos de mortalidad en Colombia durante el año 2019."),
        html.P("Utiliza las pestañas superiores para navegar por los diferentes gráficos y análisis."),
        html.Ul([
            html.Li("📍 Mapa por Departamento"),
            html.Li("📈 Muertes por Mes"),
            html.Li("📊 Exploración de Datos"),
            html.Li("🔫 Ciudades más violentas"),
            html.Li("🧘 Ciudades con menor mortalidad"),
            html.Li("📋 Principales causas de muerte"),
            html.Li("📊 Histograma por edad"),
            html.Li("🚻 Comparación por sexo y departamento")
        ]),
        html.P("Este sitio está desarrollado con Python y Dash.")
    ])
