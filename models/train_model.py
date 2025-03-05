import json
import numpy as np
import pennylane as qml

# Load dataset
with open("data/diet_data.json", "r") as f:
    raw_data = json.load(f)  

# Convert dataset into a flat list of dictionaries
data = []
for diet_category, meals in raw_data.items():
    for meal in meals:
        meal["recommended_diet"] = diet_category  # Add category as a key
        data.append(meal)

# Ensure each item is a dictionary
if isinstance(data, list) and all(isinstance(d, dict) for d in data):
    inputs = np.array([[d.get("BMI", 25) / 30, d.get("TDEE", 2500) / 3000] for d in data])
    labels = np.array([
        0 if d.get("recommended_diet") == "Vegetarian" 
        else 1 if d.get("recommended_diet") == "Non-Vegetarian" 
        else 2 for d in data  # Assigning Vegan as 2 instead of -1
    ])
else:
    raise ValueError("Error: diet_data.json is not formatted correctly. Ensure it's a list of dictionaries.")

# Quantum model
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def circuit(inputs, weights):
    qml.AngleEmbedding(inputs, wires=[0, 1])
    qml.StronglyEntanglingLayers(weights, wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

def cost(weights):
    loss = sum((circuit(inputs[i], weights) - labels[i]) ** 2 for i in range(len(inputs)))
    return loss / len(inputs)

def train_model():
    weights = np.random.rand(1, 2, 3)  # Initialize weights
    opt = qml.GradientDescentOptimizer(stepsize=0.1)
    epochs = 100

    for _ in range(epochs):  # Training loop
        weights = opt.step(cost, weights)

    with open("data/weights.json", "w") as f:
        json.dump(weights.tolist(), f)

    print("Training complete. Weights saved to 'data/weights.json'.")

if __name__ == "__main__":
    train_model()
