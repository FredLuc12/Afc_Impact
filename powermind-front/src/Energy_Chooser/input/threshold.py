from src.Energy_Chooser.constant import constraint

def threshold_captor(captor):
    if captor["co2"] > constraint.MAX_CO2[0]:
        print("co2 is too high")
        return constraint.MAX_CO2[0]
    elif captor["temp"] < constraint.MIN_TEMPERATURE[0]:
        print("temp is too low")
        return constraint.MIN_TEMPERATURE[1]
    elif captor["temp"] > constraint.MAX_TEMPERATURE[0]:
        print("temp is too high")
        return constraint.MAX_TEMPERATURE[1]
    else:
        return None

