# import joblib

# # Assuming `model` is your trained model
# joblib.dump(rf, 'model.pkl')
# # pip install flask
from flask import Flask, request, jsonify, render_template_string
import joblib

app = Flask(__name__)
model = joblib.load('modelxgb.pkl')  # Load your trained model

# HTML template with form and JavaScript
html_template = """
<!doctype html>
<html lang="en">
  <head>
    <title>Health Insurance Cross-Sell Prediction</title>
    <script>
      function submitForm() {
        var features = [
          parseFloat(document.getElementById('gender').value),
          parseFloat(document.getElementById('age').value),
          parseFloat(document.getElementById('driving_license').value),
          parseFloat(document.getElementById('region_code').value),
          parseFloat(document.getElementById('previously_insured').value),
          parseFloat(document.getElementById('vehicle_age').value),
          parseFloat(document.getElementById('vehicle_damage').value)
        ];
        fetch('/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ features: features })
        })
        .then(response => response.json())
        .then(data => {
          document.getElementById('result').textContent = 'Prediction: ' + data.prediction;
        })
        .catch(error => console.error('Error:', error));
      }
    </script>
  </head>
  <body>
    <h1>Health Insurance Cross-Sell Prediction</h1>
    <form onsubmit="event.preventDefault(); submitForm();">
      <label for="gender">Gender (1 for Male, 0 for Female):</label><br>
      <input type="number" id="gender" name="gender"><br><br>
      <label for="age">Age:</label><br>
      <input type="number" id="age" name="age"><br><br>
      <label for="driving_license">Driving License (1 for Yes, 0 for No):</label><br>
      <input type="number" id="driving_license" name="driving_license"><br><br>
      <label for="region_code">Region Code:</label><br>
      <input type="number" id="region_code" name="region_code"><br><br>
      <label for="previously_insured">Previously Insured (1 for Yes, 0 for No):</label><br>
      <input type="number" id="previously_insured" name="previously_insured"><br><br>
      <label for="vehicle_age">Vehicle Age (0 for < 1 Year, 1 for 1-2 Year, 2 for > 2 Years):</label><br>
      <input type="number" id="vehicle_age" name="vehicle_age"><br><br>
      <label for="vehicle_damage">Vehicle Damage (1 for Yes, 0 for No):</label><br>
      <input type="number" id="vehicle_damage" name="vehicle_damage"><br><br>
      <input type="submit" value="Submit">
    </form>
    <p id="result"></p>
  </body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([data['features']])
    # Convert prediction to standard Python int
    prediction_result = int(prediction[0])
    return jsonify({'prediction': prediction_result})

if __name__ == '__main__':
    app.run(debug=True)
