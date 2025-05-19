import pandas as pd
import json

def load_data():
    """
    Carga, limpia y prepara los datos de defunciones no fetales,
    uniendo los códigos de muerte y ubicación con sus nombres.
    """

    df_muertes = pd.read_excel("data/Anexo1.NoFetal2019.xlsx", sheet_name="No_Fetales_2019", engine="openpyxl")
    df_codigos = pd.read_excel("data/Anexo2.CodigosDeMuerte.xlsx", sheet_name="Final", engine="openpyxl")
    df_divipola = pd.read_excel("data/Anexo3.Divipola.xlsx", sheet_name="Hoja1", engine="openpyxl")

    # Limpiar y normalizar datos
    df_muertes['SEXO'] = df_muertes['SEXO'].replace({1: "Hombre", 2: "Mujer"})
    df_muertes['RANGO_EDAD'] = df_muertes['GRUPO_EDAD1'].apply(_grupo_edad_label)

    # Preparar códigos de muerte
    df_codigos_clean = df_codigos.iloc[8:].copy()
    df_codigos_clean.columns = df_codigos.iloc[7]
    df_codigos_clean = df_codigos_clean.rename(columns={
        'Código de la CIE-10 cuatro caracteres': 'CODIGO',
        'Descripcion  de códigos mortalidad a cuatro caracteres': 'DESCRIPCION'
    })[['CODIGO', 'DESCRIPCION']].dropna()

    # Unir la descripción de la causa de muerte
    df_muertes = df_muertes.merge(df_codigos_clean, left_on='COD_MUERTE', right_on='CODIGO', how='left')

    return df_muertes, df_divipola

def _grupo_edad_label(grupo):
    """
    Convierte el código de grupo de edad en una etiqueta de rango quinquenal.
    """
    grupos = {
        1: "0-4", 2: "5-9", 3: "10-14", 4: "15-19", 5: "20-24", 6: "25-29",
        7: "30-34", 8: "35-39", 9: "40-44", 10: "45-49", 11: "50-54", 12: "55-59",
        13: "60-64", 14: "65-69", 15: "70-74", 16: "75-79", 17: "80-84", 18: "85+"
    }
    return grupos.get(grupo, "Sin dato")

def load_geojson_departamentos():
    """
    Carga el archivo GeoJSON local con los polígonos de los departamentos.
    """
    with open("data/colombia_departamentos.geojson", encoding="utf-8") as f:
        return json.load(f)