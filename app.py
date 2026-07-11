from flask import Flask, render_template, jsonify
from services.predictor import (
    predict_next_day,
    forecast_days,
    metrics,
    feature_importance
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/predict")
def predict():

    try:

        result = predict_next_day(
            "data/NFLX.csv"
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e),
            "type": str(type(e))
        }),500


@app.route("/forecast")
def forecast():

    result = forecast_days(7)

    return jsonify({
        "forecast": result
    })


@app.route("/metrics")
def get_metrics():

    return jsonify(metrics())


@app.route("/importance")
def importance():

    return jsonify(feature_importance())


@app.route("/history")
def history():

    import pandas as pd

    df = pd.read_csv("data/NFLX.csv")

    return jsonify({

        "dates": df["Date"].tolist(),

        "close": df["Close"].tolist(),

        "volume": df["Volume"].tolist()

    })


if __name__ == "__main__":
    app.run(debug=True)