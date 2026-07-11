import os
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import RandomizedSearchCV

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor
)

from sklearn.linear_model import LinearRegression

from feature_engineering import create_features


# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("data/NFLX.csv")

df = create_features(df)

# -----------------------------
# Feature Columns
# -----------------------------

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

X = df[FEATURES]

y = df["Target"]

# -----------------------------
# Time Series Split
# -----------------------------

tscv = TimeSeriesSplit(n_splits=5)

# -----------------------------
# Candidate Models
# -----------------------------

models = {

    "Linear Regression":
        LinearRegression(),

    "Random Forest":
        RandomForestRegressor(random_state=42),

    "Extra Trees":
        ExtraTreesRegressor(random_state=42),

    "Gradient Boosting":
        GradientBoostingRegressor(random_state=42)

}

# -----------------------------
# Evaluate Models
# -----------------------------

results = {}

best_name = None

best_score = -999999

best_model = None

for name, model in models.items():

    scores = []

    for train, test in tscv.split(X):

        X_train = X.iloc[train]

        X_test = X.iloc[test]

        y_train = y.iloc[train]

        y_test = y.iloc[test]

        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        score = r2_score(y_test, pred)

        scores.append(score)

    avg = np.mean(scores)

    results[name] = avg

    print(name, avg)

    if avg > best_score:

        best_score = avg

        best_name = name

        best_model = model

print("\nBest Model:", best_name)

# -----------------------------
# Hyperparameter Tuning
# -----------------------------

if best_name in ["Random Forest", "Extra Trees"]:

    params = {

        "n_estimators":[100,200,300,500],

        "max_depth":[5,10,20,None],

        "min_samples_split":[2,5,10],

        "min_samples_leaf":[1,2,4]

    }

    search = RandomizedSearchCV(

        best_model,

        params,

        n_iter=15,

        cv=tscv,

        scoring="r2",

        random_state=42,

        n_jobs=-1

    )

    search.fit(X,y)

    best_model = search.best_estimator_

# -----------------------------
# Final Training
# -----------------------------

best_model.fit(X,y)

# -----------------------------
# Save Model
# -----------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(best_model,
            "models/netflix_model.pkl")

# -----------------------------
# Metrics
# -----------------------------

pred = best_model.predict(X)

metrics = {

    "Model":best_name,

    "MAE":float(mean_absolute_error(y,pred)),

    "RMSE":float(np.sqrt(mean_squared_error(y,pred))),

    "R2":float(r2_score(y,pred))

}

with open("models/metrics.json","w") as f:

    json.dump(metrics,f,indent=4)

print(metrics)

# -----------------------------
# Feature Importance
# -----------------------------

if hasattr(best_model,
           "feature_importances_"):

    importance = dict(

        zip(

            FEATURES,

            best_model.feature_importances_

        )

    )

    with open("models/importance.json","w") as f:

        json.dump(importance,f,indent=4)

print("Training Complete.")

with open("models/features.json", "w") as f:
    json.dump(FEATURES, f, indent=4)