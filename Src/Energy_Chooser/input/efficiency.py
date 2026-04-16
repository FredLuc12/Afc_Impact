from input.weather import get_weather


def cop():
    current_weather = get_weather()
    if current_weather > 10:
        return 4
    elif 0 <= current_weather  <= 10:
        return 3
    else:
        return 2.5
    
def gaz_capacity():
    current_weather = get_weather()
    if current_weather > 10:
        return 0.98
    elif current_weather > 0:
        return 0.95
    else:
        return 0.92