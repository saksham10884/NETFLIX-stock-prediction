import pandas as pd

from feature_engineering import create_features
from predictor import MODEL, FEATURES


def forecast_days(csv_path, days=7):

    original = pd.read_csv(csv_path)

    forecast = []

    temp = original.copy()

    for day in range(days):

        engineered = create_features(temp)

        latest = engineered.iloc[-1]

        X = latest[FEATURES].to_frame().T

        prediction = float(MODEL.predict(X)[0])

        forecast.append(prediction)

        new = temp.iloc[-1].copy()

        new["Close"] = prediction

        # Better estimates
        new["Open"] = temp.iloc[-1]["Close"]

        new["High"] = max(
            prediction,
            new["Open"]
        )

        new["Low"] = min(
            prediction,
            new["Open"]
        )

        new["Date"] = pd.to_datetime(
            new["Date"]
        ) + pd.Timedelta(days=1)

        temp.loc[len(temp)] = new

    return forecast