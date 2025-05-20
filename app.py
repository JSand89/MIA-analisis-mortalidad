import os
import dash
from dash import html, dcc
import components.mapa as mapa
import components.lineas as lineas
import components.eda_tab as eda_tab
import components.barra_violencia as barras_violencia
import components.pie_baja_mortalidad as pie_baja_mortalidad
import components.tabla_causas as tabla_causas
import components.histograma_edades as histograma_edades
import components.barras_sexo as barras_sexo

# Importar los demás componentes...

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Para despliegue

app.layout = html.Div([
    html.H1("Mortalidad en Colombia - 2019"),
    dcc.Tabs([
        dcc.Tab(label='Mapa por Departamento', children=[mapa.layout]),
        dcc.Tab(label='Muertes por Mes', children=[lineas.layout]),
        dcc.Tab(label='Exploración de Datos', children=[eda_tab.layout]),
        dcc.Tab(label='Violencia por Ciudad', children=[barras_violencia.layout]),
        dcc.Tab(label='Ciudades con menor mortalidad', children=[pie_baja_mortalidad.layout]),
        dcc.Tab(label='Causas de Muerte', children=[tabla_causas.layout]),
        dcc.Tab(label='Muertes por Edad', children=[histograma_edades.layout]),
        dcc.Tab(label='Muertes por Sexo y Departamento', children=[barras_sexo.layout]),
    ])
])
print("✅ Layout cargado correctamente")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    print(f"🚀 Iniciando app en puerto {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)