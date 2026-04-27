from src.Energy_Chooser.constant import constraint,path
from src.Energy_Chooser.function import csv


def normalize_temp(T):
    #we limit the value with max and min 
    #we substract the temp with min temp to have a ref at 0 if temp = min temp
    #we substract max temp with min temps to have a ref at 1 if temp = maw temp
    return max(0, min(1,(T - constraint.MIN_TEMPERATURE[0]) / (constraint.MAX_TEMPERATURE[0] - constraint.MIN_TEMPERATURE[0])))

def normalize_pir(PIR):
    return 1 if PIR else 0

def normalize_price(P,df):
    min_price = csv.get_min_dataframe("price",df)
    max_price = csv.get_max_dataframe("price",df)
    return max(0, min(1,(P - min_price) / (max_price - min_price)))

def normalize_cop(C):
    return max(0,max(1,( C - constraint.MIN_COP[0]) / (constraint.MAX_COP[0] - constraint.MIN_COP[0])))

def normalize_co2(C):
    return max(0,max(1,( C - constraint.MIN_CO2[0]) / (constraint.MAX_CO2[0] - constraint.MIN_CO2[0])))

def normalize_humidity(H):
    return max(0,max(1,( H - constraint.MIN_HUMIDITY[0]) / (constraint.MAX_HUMIDITY[0] - constraint.MIN_HUMIDITY[0])))
