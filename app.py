from flask import Flask, render_template, request
import pickle
import json
import pandas as pd

app = Flask(__name__)

# Test route to check if Flask is running
@app.route('/test')
def test():
    return "Test route working!"

# # Load label encoders
# try:
#     with open('label_encoders.pkl', 'rb') as file:
#         label_encoders = pickle.load(file)
# except FileNotFoundError:
#     print("Error: label_encoders.pkl not found.")

# # Load trained model
# try:
#     with open('random_forest_model.pkl', 'rb') as file:
#         model = pickle.load(file)
# except FileNotFoundError:
#     print("Error: random_forest_model.pkl not found.")

# Load dropdown options from JSON file
def load_options():
    try:
        with open('options.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: options.json not found.")
        return {}

options = load_options()

@app.route('/')
def home():
    print("Home route accessed")
    return render_template('index.html', options=options)

@app.route('/predict', methods=['POST'])
def prediction():
    try:
        # Collect form inputs
        data = {
            'Manufacturer': request.form['Manufacturer'],
            'Model': request.form['Model'],
            'Prod_year': int(request.form['Prod_year']),
            'Category': request.form['Category'],
            'Leather_interior': request.form['Leather_interior'],
            'Fuel_type': request.form['Fuel_type'],
            'Engine_volume': request.form['Engine_volume'],
            'Mileage': int(request.form['Mileage']),
            'Cylinders': float(request.form['Cylinders']),
            'Gear_box_type': request.form['Gear_box_type'],
            'Drive_wheels': request.form['Drive_wheels'],
            'Wheel': request.form['Wheel'],
            'Color': request.form['Color'],
            'Levy': int(request.form['Levy']),
            'Airbags': int(request.form['Airbags']),
            'car_age': int(request.form['car_age'])
        }

        print("Form data received:", data)

        # Convert input to DataFrame
        input_df = pd.DataFrame([data])

        # Ensure columns are in the correct order for the model
        column_order = ['Manufacturer', 'Model', 'Category', 'Leather_interior', 'Fuel_type', 
                        'Engine_volume', 'Gear_box_type', 'Drive_wheels', 'Wheel', 'Color', 
                        'Levy', 'Prod_year', 'Mileage', 'Cylinders', 'Airbags', 'car_age']
        input_df = input_df[column_order]


        # Encode categorical variables using label encoders
        for col, encoder in label_encoders.items():
            if col in input_df.columns:
                try:
                    input_df[col] = encoder.transform(input_df[col])
                except ValueError:
                    input_df[col] = -1  # Assign -1 for unseen labels

        # Make prediction
        prediction = model.predict(input_df)[0]
        predicted_price = round(prediction, 2)

        return render_template('car_index.html', options=options, prediction=f"Predicted Price: ${predicted_price}")

    except Exception as e:
        print(f"Prediction error: {e}")
        return render_template('car_index.html', options=options, error="An error occurred during prediction.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)