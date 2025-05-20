import os
import dash
from dash import html, dcc, Output, Input

import components.inicio as inicio
import components.mapa as mapa
import components.lineas as lineas
import components.eda_tab as eda_tab
import components.barra_violencia as barras_violencia
import components.pie_baja_mortalidad as pie_baja_mortalidad
import components.tabla_causas as tabla_causas
import components.histograma_edades as histograma_edades
import components.barras_sexo as barras_sexo

# Inicializar app Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Para despliegue

# Layout principal con Tabs y espacio para renderizar contenido dinámico
app.layout = html.Div([
    html.H1("Mortalidad en Colombia - 2019"),
    dcc.Tabs(
        id="tabs", 
        value="inicio", 
        children=[
            dcc.Tab(label="Inicio", value="inicio"),
            dcc.Tab(label='Mapa por Departamento', value='mapa'),
            dcc.Tab(label='Muertes por Mes', value='lineas'),
            dcc.Tab(label='Exploración de Datos', value='eda_tab'),
            dcc.Tab(label='Violencia por Ciudad', value='barra_violencia'),
            dcc.Tab(label='Ciudades con menor mortalidad', value='pie_baja_mortalidad'),
            dcc.Tab(label='Causas de Muerte', value='tabla_causas'),
            dcc.Tab(label='Muertes por Edad', value='histograma_edades'),
            dcc.Tab(label='Muertes por Sexo y Departamento', value='barras_sexo'),
        ]
    ),
    html.Div(id="content")
])

# Callback para renderizar cada layout bajo demanda
@app.callback(Output("content", "children"), Input("tabs", "value"))
def render_tab(tab_name):
    print(f"🌀 Tab seleccionada: {tab_name}")  # debug
    try:
        if tab_name == "inicio":
            return inicio.get_layout()
        elif tab_name == "mapa":
            return mapa.get_layout()
        elif tab_name == "lineas":
            return lineas.get_layout()
        elif tab_name == "eda_tab":
            return eda_tab.get_layout()
        elif tab_name == "barra_violencia":
            return barras_violencia.get_layout()
        elif tab_name == "pie_baja_mortalidad":
            return pie_baja_mortalidad.get_layout()
        elif tab_name == "tabla_causas":
            return tabla_causas.get_layout()
        elif tab_name == "histograma_edades":
            return histograma_edades.get_layout()
        elif tab_name == "barras_sexo":
            return barras_sexo.get_layout()
    except Exception as e:
        print(f"❌ Error al cargar la pestaña {tab_name}: {e}")
        return html.Div(f"Error al cargar la pestaña: {tab_name}")

# Ejecución principal
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    print(f"🚀 Iniciando app en puerto {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
