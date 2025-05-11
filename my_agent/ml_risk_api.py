import pickle
from flask import Flask, request, jsonify
import numpy as np

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Start Flask web server
app = Flask(__name__)
# Create an endpoint
@app.route('/predict', methods=['POST'])
def predict():
  # Process incoming JSON
    data = request.get_json()
    loc = data['loc']
    complexity = data['complexity']
    
    # Prepare input
    features = np.array([[loc, complexity]])
    
    # Feed data into the model and do prediction
    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0][pred]

    # Return the result as JSON
    return jsonify({
        'risk': int(pred),
        'confidence': round(float(proba), 2)
    })

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
