import pandas as pd
from sqlalchemy import create_engine, text

def bd_llamada_ocr(query, params_tuple):
    server_ocr = 'yurestazure.database.windows.net'
    database_ocr = 'yuBDazure'
    username_ocr = 'CloudSA19f38018'
    password_ocr = '65gh_34ddf'  # Debes proporcionar el password

    connection_string_ocr = f'mssql+pyodbc://{username_ocr}:{password_ocr}@{server_ocr}/{database_ocr}?driver=ODBC+Driver+17+for+SQL+Server'
    engine_ocr = create_engine(connection_string_ocr)

    # Ejecutar la consulta y obtener un DataFrame de pandas
    df = pd.read_sql_query(text(query), engine_ocr, params=params_tuple)
    return df