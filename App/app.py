from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

app = Flask(__name__)

# Load and preprocess the data
data = pd.read_csv(r"App/Product Demand Prediction with Machine Learning.csv")
data = data.dropna()
X = data[["Total Price", "Base Price"]]
y = data["Units Sold"]
xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeRegressor()
model.fit(xtrain, ytrain)

@app.route('/')
def index():
    # The main page can provide a simple form to input Total Price and Base Price
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    TP = float(request.form['total_price'])
    BP = float(request.form['base_price'])
    features = np.array([[TP, BP]])
    prediction = model.predict(features)
    return jsonify({"prediction": prediction[0]})

@app.route('/result')
def show_result():
    prediction = request.args.get('prediction')
    return render_template('result.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
