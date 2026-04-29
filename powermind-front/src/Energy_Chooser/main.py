import joblib
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_text
from src.Energy_Chooser.input.dataset import generate_dataset
from src.Energy_Chooser.input.captor import DATA

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

MODEL_PATH = os.path.join(BASE_DIR, "src/Energy_Chooser", "energy_chooser.pkl")
FEATURE_ORDER = ["temp", "humidity", "co2", "pir"]

def train_model():
    df = generate_dataset()
    X = df[["temp","humidity","co2","pir"]]
    Y = df["energy"]
    model = RandomForestClassifier()
    model.fit(X,Y)
    joblib.dump(model, "energy_chooser.pkl")

def ia_energy_chooser(data):

    model = joblib.load(MODEL_PATH)
    #X_input = pd.DataFrame([DATA])
    print(type(data))
    print(data)
    X_input = pd.DataFrame([data])[FEATURE_ORDER]
    prediction = model.predict(X_input)[0]
    importances = model.feature_importances_
    weights = dict(zip(FEATURE_ORDER, importances))

    return int(prediction),weights

if __name__ == "__main__":
    train_model()
    #print(ia_energy_chooser(DATA))