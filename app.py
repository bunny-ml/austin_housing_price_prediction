from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load models
with open('models/Knn.pickle', 'rb') as f:
    knn_model = pickle.load(f)

with open('models/linear_model.pickle', 'rb') as f:
    linear_model = pickle.load(f)

with open('models/random_model.pickle', 'rb') as f:
    random_forest_model = pickle.load(f)

# Render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    bedrooms = int(data.get('bedrooms', 0))
    stories = int(data.get('stories', 0))
    spa = 1 if data.get('spa', '').lower() == 'yes' else 0
    view = 1 if data.get('view', '').lower() == 'yes' else 0
    garage = 1 if data.get('garage', '').lower() == 'yes' else 0

    input_features = np.array([[bedrooms, stories, spa, view, garage]])

    predictions = {
        "KNN Prediction": knn_model.predict(input_features)[0],
        "Linear Regression Prediction": linear_model.predict(input_features)[0],
        "Random Forest Prediction": random_forest_model.predict(input_features)[0]
    }
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
