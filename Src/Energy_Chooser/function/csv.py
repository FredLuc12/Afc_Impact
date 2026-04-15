import pandas as pd
import os


def csv_to_dataframe(path_csv, file_csv):
    path_csv_file = os.path.join(path_csv, file_csv)
    df = pd.read_csv(path_csv_file)
    return df

def get_max_dataframe(name_column, df):
    return df[name_column].max()

def get_min_dataframe(name_column, df):
    return df[name_column].min()
