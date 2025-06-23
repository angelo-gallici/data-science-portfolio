def check_nulls_all_columns(df):

    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()

    if total_nulls == 0:
        print("No hay valores nulos en ninguna columna.")
    else:
        print("Valores nulos encontrados:")
        print(null_counts[null_counts > 0])

def check_data_types(df):

    #print("\nTipos de datos por columna:")
    #print(df.dtypes)

    print("\nChequeando columnas no numéricas que podrían ser numéricas")
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col].astype(float)
                print(f"La columna '{col}' es object pero puede convertirse a numérico.")
            except ValueError:
                continue

def validar_datos(df):
    check_nulls_all_columns(df)
    check_data_types(df)

