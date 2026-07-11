import pandas as pd

from services.indicators import *


def create_features(df):

    df = df.copy()

    df = df.sort_values("Date")

    df = df.drop(columns=["Adj Close"])

    # Lag Features
    for lag in [1, 2, 3, 5, 10]:

        df[f"Lag_{lag}"] = df["Close"].shift(lag)

    # Moving Averages
    df["MA5"] = moving_average(df, 5)
    df["MA10"] = moving_average(df, 10)
    df["MA20"] = moving_average(df, 20)
    df["MA50"] = moving_average(df, 50)

    # EMA
    df["EMA10"] = exponential_moving_average(df, 10)
    df["EMA20"] = exponential_moving_average(df, 20)

    # Returns
    df["Return"] = daily_return(df)

    # Volatility
    df["Volatility"] = volatility(df)

    # Price spreads
    df["HL_Spread"] = high_low_spread(df)
    df["OC_Spread"] = open_close_spread(df)

    # RSI
    df["RSI"] = rsi(df)

    # MACD
    macd_line, signal = macd(df)

    df["MACD"] = macd_line
    df["MACD_Signal"] = signal

    # Bollinger
    upper, lower = bollinger(df)

    df["BB_Upper"] = upper
    df["BB_Lower"] = lower

    # Target
    df["Target"] = df["Close"].shift(-1)

    df.dropna(inplace=True)

    return df