from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Load diet dataset
with open("data/meal_plan_dataset.json", "r") as f:
    diet_data = json.load(f)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/get-meal-plan", methods=["POST"])
def get_meal_plan():
    try:
        diet_goal = request.form["diet_goal"]
        diet_preference = request.form["diet_preference"]

        # Validate inputs
        if diet_goal not in diet_data:
            return jsonify({"error": f"No meal plan found for {diet_goal}."}), 404
        
        if diet_preference not in diet_data[diet_goal]:
            return jsonify({"error": f"No meal plan found for {diet_goal} - {diet_preference}."}), 404
        
        # Randomly select a meal plan
        selected_meal = random.choice(diet_data[diet_goal][diet_preference])

        return jsonify({
            "diet_goal": diet_goal,
            "diet_preference": diet_preference,
            "recommended_meal_plan": selected_meal
        })
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
