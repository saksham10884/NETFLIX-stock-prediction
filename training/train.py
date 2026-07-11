import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from feature_engineering import create_features


FEATURES = [
    "Lag_1",
    "Lag_2",
    "Lag_3",
    "Lag_5",
    "Lag_10",
    "MA5",
    "MA10",
    "MA20",
    "MA50",
    "EMA10",
    "EMA20",
    "Return",
    "Volatility",
    "HL_Spread",
    "OC_Spread",
    "RSI",
    "MACD",
    "MACD_Signal",
    "BB_Upper",
    "BB_Lower"
]


df = pd.read_csv(
    "data/NFLX.csv"
)


# IMPORTANT
df = create_features(df)


# remove NaN created by indicators
df = df.dropna()


X = df[FEATURES]


# Predict next day's close
y = df["Close"].shift(-1)


# remove last empty row
X = X[:-1]
y = y[:-1]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)


model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    model,
    "models/netflix_model.pkl"
)


print("Model trained successfully!")