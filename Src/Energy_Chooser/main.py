import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_text
from input.dataset import generate_dataset
from input.captor import DATA


def train_model():
    df = generate_dataset()
    X = df[["temp","humidity","co2","pir"]]
    Y = df["energy"]
    model = RandomForestClassifier()
    model.fit(X,Y)
    joblib.dump(model, "energy_chooser.pkl")

def ia_energy_chooser():

    model = joblib.load("energy_chooser.pkl")
    X_input = pd.DataFrame([DATA])
    prediction = model.predict(X_input)[0]
    return int(prediction)

if __name__ == "__main__":
    train_model()
    #print(ia_energy_chooser(DATA))