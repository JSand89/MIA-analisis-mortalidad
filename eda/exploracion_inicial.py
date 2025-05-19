import pandas as pd

def explorar_estructura():
    """
    Carga los datos sin procesar y realiza un análisis exploratorio inicial:
    - muestra las primeras filas,
    - imprime nombres de columnas,
    - muestra tipos de datos y valores nulos.
    """
    df = pd.read_excel("data/Anexo1.NoFetal2019.xlsx", sheet_name="No_Fetales_2019", engine="openpyxl")

    print("Primeras 5 filas:")
    print(df.head(5))

    print("\nColumnas:")
    print(df.columns.tolist())

    print("\nResumen de tipos de datos:")
    print(df.dtypes)

    print("\nConteo de valores nulos:")
    print(df.isnull().sum())

    return df
