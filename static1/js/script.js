document.getElementById("height").addEventListener("input", updateBMI);
document.getElementById("weight").addEventListener("input", updateBMI);

function updateBMI() {
    const height = parseFloat(document.getElementById("height").value) / 100;
    const weight = parseFloat(document.getElementById("weight").value);

    if (height > 0 && weight > 0) {
        const bmi = (weight / (height * height)).toFixed(2);
        document.getElementById("bmi").value = bmi;
    } else {
        document.getElementById("bmi").value = "";
    }
}

document.getElementById("dietForm").onsubmit = async function (event) {
    event.preventDefault();

    // Get selected diet goal and preference
    const dietGoal = document.getElementById("diet_goal").value;
    const dietPreference = document.getElementById("diet_preference").value;

    if (!dietGoal || !dietPreference) {
        alert("⚠️ Please select a diet goal and dietary preference!");
        return;
    }

    // Show loading animation
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3 text-muted">🔄 Generating your meal plan...</p>
        </div>
    `;

    try {
        const formData = new FormData();
        formData.append("diet_goal", dietGoal);
        formData.append("diet_preference", dietPreference);

        const response = await fetch("/get-meal-plan", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        // Display the meal plan
        resultDiv.innerHTML = `
            <h3 class="text-center">Your Meal Plan (${result.diet_goal} - ${result.diet_preference})</h3>
            <ul class="list-group">
                <li class="list-group-item"><strong>Breakfast:</strong> ${result.recommended_meal_plan.breakfast}</li>
                <li class="list-group-item"><strong>Snack 1:</strong> ${result.recommended_meal_plan.snack1}</li>
                <li class="list-group-item"><strong>Lunch:</strong> ${result.recommended_meal_plan.lunch}</li>
                <li class="list-group-item"><strong>Snack 2:</strong> ${result.recommended_meal_plan.snack2}</li>
                <li class="list-group-item"><strong>Dinner:</strong> ${result.recommended_meal_plan.dinner}</li>
                <li class="list-group-item"><strong>Snack 3:</strong> ${result.recommended_meal_plan.snack3}</li>
            </ul>
        `;
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="alert alert-danger text-center" role="alert">
                ❌ Oops! ${error.message}
            </div>
        `;
    }
};
