from pathlib import Path
from src.Energy_Chooser.constant.path import CSV_PATH
from datetime import datetime
from src.Energy_Chooser.function import csv
import pandas as pd

folder = Path(CSV_PATH)

data_elec = [

    ["00h–01h", 45],
    ["01h–02h", 42],
    ["02h–03h", 40],
    ["03h–04h", 38],
    ["04h–05h", 40],
    ["05h–06h", 45],
    ["06h–07h", 60],
    ["07h–08h", 75],
    ["08h–09h", 85],
    ["09h–10h", 80],
    ["10h–11h", 70],
    ["11h–12h", 65],
    ["12h–13h", 60],
    ["13h–14h", 65],
    ["14h–15h", 70],
    ["15h–16h", 75],
    ["16h–17h", 85],
    ["17h–18h", 110],
    ["18h–19h", 140],
    ["19h–20h", 150],
    ["20h–21h", 120],
    ["21h–22h", 90],
    ["22h–23h", 70],
    ["23h–00h", 55],
]

data_gaz = [

    ["00h–01h", 51.2],
    ["01h–02h", 50.8],
    ["02h–03h", 50.5],
    ["03h–04h", 50.3],
    ["04h–05h", 50.1],
    ["05h–06h", 50.4],
    ["06h–07h", 51.0],
    ["07h–08h", 52.3],
    ["08h–09h", 53.1],
    ["09h–10h", 53.8],
    ["10h–11h", 54.2],
    ["11h–12h", 54.0],
    ["12h–13h", 53.6],
    ["13h–14h", 53.9],
    ["14h–15h", 54.5],
    ["15h–16h", 55.1],
    ["16h–17h", 55.4],
    ["17h–18h", 55.0],
    ["18h–19h", 54.6],
    ["19h–20h", 54.2],
    ["20h–21h", 53.7],
    ["21h–22h", 53.3],
    ["22h–23h", 52.8],
    ["23h–00h", 52.4],
]

def df_energy():
    if not any(folder.glob("*.csv")):
        df = pd.DataFrame(data_elec, columns=["hour", "price"])
        df.to_csv("price_elec.csv", index=False)

        df = pd.DataFrame(data_gaz, columns=["hour", "price"])
        df.to_csv("price_gaz.csv", index=False)
    else:
        print("csv present")

def get_price_energy(df):
    heure = datetime.now().hour
    df["current_hour"] = df["hour"].str.split("h").str[0].astype(int)
    current_price = df.loc[df["current_hour"] == heure, "price"].values[0]
    return current_price

#if __name__ == "__main__":
#   df_energy()
