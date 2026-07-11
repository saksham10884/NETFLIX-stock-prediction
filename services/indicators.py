import pandas as pd


def moving_average(df, window):
    return df["Close"].rolling(window).mean()


def exponential_moving_average(df, window):
    return df["Close"].ewm(span=window, adjust=False).mean()


def daily_return(df):
    return df["Close"].pct_change()


def volatility(df, window=10):
    return df["Close"].rolling(window).std()


def high_low_spread(df):
    return df["High"] - df["Low"]


def open_close_spread(df):
    return df["Open"] - df["Close"]


def rsi(df, period=14):

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def macd(df):

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()

    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26

    signal = macd.ewm(span=9, adjust=False).mean()

    return macd, signal


def bollinger(df, window=20):

    ma = df["Close"].rolling(window).mean()

    std = df["Close"].rolling(window).std()

    upper = ma + 2 * std

    lower = ma - 2 * std

    return upper, lower