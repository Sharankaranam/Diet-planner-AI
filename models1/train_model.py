import json
import numpy as np
import pennylane as qml

# Load dataset
with open("data/meal_plan_dataset.json", "r") as f:
    raw_data = json.load(f)  

# Flatten dataset into a structured list
data = []
diet_categories = ["Low Carb", "High Fat", "Low Fat", "High Protein", "Normal"]
diet_types = ["Vegetarian", "Non-Vegetarian", "Vegan"]

for diet_category in diet_categories:
    for diet_type in diet_types:
        for meal in raw_data[diet_category][diet_type]:
            meal["category"] = diet_category
            meal["diet_type"] = diet_type
            data.append(meal)

# Ensure correct format
if not (isinstance(data, list) and all(isinstance(d, dict) for d in data)):
    raise ValueError("Error: Dataset is not formatted correctly. Ensure it's a list of dictionaries.")

# Feature Extraction: Normalize BMI and TDEE values
inputs = np.array([[d.get("BMI", 25) / 30, d.get("TDEE", 2500) / 3000] for d in data])

# Assign labels based on diet categories (0: Low Carb, 1: High Fat, ..., 4: Normal)
category_map = {cat: i for i, cat in enumerate(diet_categories)}
labels = np.array([category_map[d["category"]] for d in data])

# Define quantum model
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def circuit(x, weights):
    qml.AngleEmbedding(x, wires=[0, 1])
    qml.StronglyEntanglingLayers(weights, wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

def cost(weights):
    loss = sum((circuit(inputs[i], weights) - labels[i]) ** 2 for i in range(len(inputs)))
    return loss / len(inputs)

def train_model():
    weights = np.random.rand(1, 2, 3)  # Initialize weights
    opt = qml.AdamOptimizer(stepsize=0.05)  # Use Adam optimizer
    epochs = 200

    for epoch in range(epochs):
        weights = opt.step(cost, weights)
        if epoch % 20 == 0:
            print(f"Epoch {epoch}: Loss = {cost(weights)}")

    # Save trained weights
    with open("trained_weights.json", "w") as f:
        json.dump(weights.tolist(), f)

    print("Training complete. Weights saved to 'trained_weights.json'.")

if __name__ == "__main__":
    train_model()
