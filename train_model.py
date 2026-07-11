import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from feature_engineering import create_features


# Load Dataset
df = pd.read_csv("data/NFLX.csv")

# Create Features
df = create_features(df)

features = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "MA5",
    "MA10",
    "MA20",
    "MA50",
    "Return",
    "HL_Diff",
    "OC_Diff"
]

X = df[features]
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    shuffle=False,
    test_size=0.2
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("MAE :", mean_absolute_error(y_test, predictions))
print("RMSE:", mean_squared_error(y_test, predictions)**0.5)
print("R2  :", r2_score(y_test, predictions))

joblib.dump(model, "models/random_forest.pkl")

print("Model Saved Successfully")