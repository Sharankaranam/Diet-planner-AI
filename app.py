from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import pennylane as qml

app = Flask(__name__)

# Load diet dataset
with open("data/diet_data.json", "r") as f:
    diet_data = json.load(f)

# Quantum model setup
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def circuit(inputs, weights):
    qml.AngleEmbedding(inputs, wires=[0, 1])
    qml.StronglyEntanglingLayers(weights, wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bmi = float(request.form["bmi"])
        tdee = float(request.form["tdee"])
        diet_preference = request.form["diet_type"]  # Get user's choice

        # Validate selection
        if diet_preference not in diet_data:
            return jsonify({"error": "Invalid diet preference."})

        # Select a random meal plan from chosen diet type
        selected_meal = np.random.choice(diet_data[diet_preference])

        # Prepare JSON response
        response_data = {
            "bmi": bmi,
            "tdee": tdee,
            "diet_type": diet_preference,
            "recommended_meal_plan": selected_meal
        }

        return jsonify(response_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
