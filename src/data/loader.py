import pandas as pd

def load_raw_data(path):
    return pd.read_csv(path, sep=',', low_memory=False)

def load_clean_data(path):
    return pd.read_csv(path)

def save_clean_data(df, path):
    df.to_csv(path, index=False)

    