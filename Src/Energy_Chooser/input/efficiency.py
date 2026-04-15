from input.weather import get_weather

CURRENT_WEATHER = int(get_weather())

def cop():
    if CURRENT_WEATHER > 10:
        return 4
    elif 0 <= CURRENT_WEATHER  <= 10:
        return 3
    else:
        return 2.5
    
def gaz_capacity():
    if CURRENT_WEATHER > 10:
        return 0.98
    elif CURRENT_WEATHER > 0:
        return 0.95
    else:
        return 0.92