from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the Trained Model
model_path = "Traffic_XGB_Model.pkl"
scaler_path = "Scaler.pkl"

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    print("Error: Model or scaler file not found.")
    exit()


# Function to Convert Predicted Value back to its Original Scale
def inverse_transform_prediction(prediction):
    return np.expm1(prediction)  # Inverse Transformation of log1p


@app.route("/")
def home():
    return render_template("Index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user Input from Form
        weekday = int(request.form["Weekday"])
        hour = int(request.form["Hour"])
        temp = float(request.form["Temp"])

        # Preprocess User Input
        input_data = np.array([[temp,weekday,hour]])
        input_data_scaled = scaler.transform(input_data)

        # Make Prediction
        prediction = model.predict(input_data_scaled)

        # Convert Prediction back to Original Scale and Remove Decimals
        original_prediction = int(round(inverse_transform_prediction(prediction)[0]))

        # Return Prediction
        return render_template("Result.html", prediction=original_prediction)
    except Exception as e:
        print("Prediction error:", e)
        return "An error occurred during prediction."


if __name__ == "__main__":
    app.run(debug=True)
