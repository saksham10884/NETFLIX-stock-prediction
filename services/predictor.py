import json
import joblib
import pandas as pd
import numpy as np

from feature_engineering import create_features


# -----------------------------
# Load Model
# -----------------------------

MODEL = joblib.load("models/netflix_model.pkl")

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


# -----------------------------
# Load Feature Importance
# -----------------------------

try:
    with open("models/importance.json", "r") as f:
        FEATURE_IMPORTANCE = json.load(f)
except:
    FEATURE_IMPORTANCE = {}


def estimate_confidence(model, X):

    if not hasattr(model, "estimators_"):
        return None

    tree_predictions = np.array(
        [tree.predict(X)[0] for tree in model.estimators_]
    )

    std = np.std(tree_predictions)

    mean = np.mean(tree_predictions)

    if mean == 0:
        return None

    coefficient_variation = std / abs(mean)

    confidence = max(
        0,
        min(
            100,
            100 - coefficient_variation * 100
        )
    )

    return round(confidence, 2)
# -----------------------------
# Recommendation Logic
# -----------------------------

def recommendation(change):

    if change >= 2:
        return "BUY"

    elif change <= -2:
        return "DON'T BUY"

    return "HOLD"


# -----------------------------
# Top Feature Explanation
# -----------------------------
def market_explanation(latest_row):

    explanation = []

    if latest_row["MA5"] > latest_row["MA20"]:
        explanation.append(
            "Short-term moving average is above the 20-day average, indicating positive momentum."
        )
    else:
        explanation.append(
            "Short-term moving average is below the 20-day average, indicating weaker momentum."
        )

    if latest_row["RSI"] > 70:
        explanation.append(
            "RSI suggests the stock is overbought."
        )

    elif latest_row["RSI"] < 30:
        explanation.append(
            "RSI suggests the stock is oversold."
        )

    else:
        explanation.append(
            "RSI is in the neutral range."
        )

    if latest_row["MACD"] > latest_row["MACD_Signal"]:
        explanation.append(
            "MACD is above its signal line, indicating bullish momentum."
        )
    else:
        explanation.append(
            "MACD is below its signal line, indicating bearish momentum."
        )

    if latest_row["Return"] > 0:
        explanation.append(
            "The most recent daily return was positive."
        )
    else:
        explanation.append(
            "The most recent daily return was negative."
        )

    return explanation


# -----------------------------
# Tomorrow Prediction
# -----------------------------

def predict_next_day(csv_path):

    df = pd.read_csv(csv_path)

    df = create_features(df)

    latest = df.iloc[-1]

    X = latest[FEATURES].to_frame().T

    prediction = float(MODEL.predict(X)[0])

    current = float(latest["Close"])

    change = ((prediction - current) / current) * 100

    confidence = estimate_confidence(MODEL, X)

    why = market_explanation(latest)

    result = {

    "current_price": round(current,2),

    "prediction": round(prediction,2),

    "change_percent": round(change,2),

    "signal": recommendation(change),

    "confidence": confidence,

    "why": why

    }

    return result


# -----------------------------
# 7-Day Forecast
# -----------------------------

def predict_week(csv_path):

    df = pd.read_csv(csv_path)

    forecasts = []

    temp = df.copy()

    for i in range(7):

        engineered = create_features(temp)

        latest = engineered.iloc[-1]

        X = latest[FEATURES].to_frame().T

        pred = float(MODEL.predict(X)[0])

        forecasts.append(round(pred, 2))

        # Append a synthetic next day
        new_row = temp.iloc[-1].copy()

        new_row["Close"] = pred
        new_row["Open"] = pred
        new_row["High"] = pred
        new_row["Low"] = pred

        # Keep volume unchanged
        temp.loc[len(temp)] = new_row

    return forecasts


# -----------------------------
# Metrics
# -----------------------------

def metrics():

    with open("models/metrics.json", "r") as f:
        return json.load(f)


# -----------------------------
# Feature Importance
# -----------------------------

def feature_importance():

    return FEATURE_IMPORTANCE

df = pd.read_csv("data/NFLX.csv")

# -----------------------------
# Multi Day Forecast
# -----------------------------

def forecast_days(days=7):

    df = pd.read_csv("data/NFLX.csv")

    predictions = []

    temp = df.copy()


    for i in range(days):

        # Generate same features used during training
        engineered = create_features(temp)

        engineered = engineered.dropna()


        latest = engineered.iloc[-1]


        X = latest[FEATURES].to_frame().T


        prediction = float(
            MODEL.predict(X)[0]
        )


        predictions.append(
            {
                "day": i + 1,
                "price": round(prediction,2)
            }
        )


        # Create next synthetic day
        new_row = temp.iloc[-1].copy()


        new_row["Close"] = prediction
        new_row["Open"] = prediction
        new_row["High"] = prediction
        new_row["Low"] = prediction


        temp.loc[len(temp)] = new_row


    return predictions