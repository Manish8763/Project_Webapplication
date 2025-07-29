from flask import Flask, jsonify, render_template_string
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# -------------------------
# Machine Learning Function
# -------------------------
def prepare_data(df, forecast_col, forecast_out, test_size):
    label = df[forecast_col].shift(-forecast_out)
    X = np.array(df[[forecast_col]])
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]
    label.dropna(inplace=True)
    y = np.array(label)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    return X_train, X_test, y_train, y_test, X_lately

def predict_prices():
    df = pd.read_csv("prices.csv")  # Make sure this file exists in the same folder
    df = df[df.symbol == "GOOG"]
    forecast_col = 'close'
    forecast_out = 5
    test_size = 0.2

    X_train, X_test, y_train, y_test, X_lately = prepare_data(df, forecast_col, forecast_out, test_size)
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test) * 100
    forecast = model.predict(X_lately)
    return score, forecast

# -------------------------
# Flask Routes
# -------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Stock Price Predictor</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        button { padding: 10px 20px; font-size: 16px; }
        #result { margin-top: 30px; }
    </style>
    <script>
        async function getPrediction() {
            const response = await fetch('/predict');
            const data = await response.json();
            if (data.error) {
                document.getElementById('result').innerHTML = `<p style="color:red;">${data.error}</p>`;
                return;
            }
            document.getElementById('result').innerHTML =
                `<h3>Accuracy: ${data.accuracy}%</h3>
                 <h4>Next 5-Day Forecast:</h4>
                 <ul>${data.forecast.map(p => `<li>$${p}</li>`).join('')}</ul>`;
        }
    </script>
</head>
<body>
    <h1>📈 Stock Price Predictor</h1>
    <p>Click the button to predict GOOG stock price for the next 5 days:</p>
    <button onclick="getPrediction()">Predict</button>
    <div id="result"></div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/predict')
def predict():
    try:
        score, forecast = predict_prices()
        return jsonify({
            'accuracy': round(score, 2),
            'forecast': [round(p, 2) for p in forecast]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# -------------------------
# Run the App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
