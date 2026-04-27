import random
from src.Energy_Chooser.input.captor import DATA
from src.Energy_Chooser.input.threshold import threshold_captor
from src.Energy_Chooser.input.efficiency import cop, gaz_capacity
from src.Energy_Chooser.input import price
from src.Energy_Chooser.constant import constraint,path
from src.Energy_Chooser.function import normalize, csv
import pandas as pd

def energy_cost(temp,humidity,co2,pir):
    energy = threshold_captor(DATA)
    if energy:
        print("value critical found")
        return energy
    t_norm = normalize.normalize_temp(temp)
    pir_norm = normalize.normalize_pir(pir)
    humidity_norm = normalize.normalize_humidity(humidity)
    co2_norm = normalize.normalize_co2(co2)

    score_elec = 0
    score_gaz = 0

    score_gaz += 0.5 * (1 - t_norm) / gaz_capacity()
    score_elec += 0.5 * t_norm / cop()

    score_elec += 0.3 * co2_norm / cop()
    score_gaz += 0.2 * humidity_norm / gaz_capacity()
    score_elec += 0.2 * pir_norm / cop()    
    
    return 1 if score_elec < score_gaz else 0
    
def generate_sample():

    temp = random.uniform(10, 26)        
    humidity = random.uniform(20, 80)    
    co2 = random.uniform(400, 2000)      
    pir = random.choice([0, 1])

    return temp, humidity, co2, pir

def generate_dataset():
    data = []
    for _ in range(1000):
        temp, humidity, co2, pir = generate_sample()
        energy = energy_cost(temp,humidity,co2,pir)
        data.append([temp,humidity,co2,pir,energy])

    df = pd.DataFrame(data, columns=[
        "temp", 
        "humidity",
        "co2",
        "pir",
        "energy"
    ])

    print(df["energy"].value_counts())
    return df

    
