document.getElementById("dietForm").onsubmit = async function(event) {
    event.preventDefault();

    // Get input values
    const height = parseFloat(document.getElementById("height").value) / 100; // cm to meters
    const weight = parseFloat(document.getElementById("weight").value);
    const tdee = parseInt(document.getElementById("tdee").value);
    const dietType = document.getElementById("diet_type").value;

    // Validate inputs
    if (!height || !weight || !tdee || !dietType) {
        alert("Please fill in all fields!");
        return;
    }

    // Calculate BMI
    const bmi = (weight / (height * height)).toFixed(2);

    // Prepare data
    const formData = new FormData();
    formData.append("bmi", bmi);
    formData.append("tdee", tdee);
    formData.append("diet_type", dietType);

    // Show loading state
    const resultDiv = document.getElementById("result");
    const resultContainer = document.getElementById("resultContainer");
    resultDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3 text-muted">Crafting your perfect plan...</p>
        </div>
    `;
    resultContainer.classList.add("show");

    try {
        // Fetch data
        const response = await fetch("/", {
            method: "POST",
            body: formData
        });
        const result = await response.json();

        // Display 6-meal plan
        resultDiv.innerHTML = `
            <div class="alert alert-light text-center shadow-sm" role="alert">
                <strong>BMI: ${bmi}</strong> | <strong>TDEE: ${tdee} kcal</strong>
            </div>
            <div class="accordion" id="mealPlanAccordion">
                <div class="accordion-item mb-2">
                    <h2 class="accordion-header" id="headingBreakfast">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseBreakfast">
                            Breakfast 🍽️
                        </button>
                    </h2>
                    <div id="collapseBreakfast" class="accordion-collapse collapse show" data-bs-parent="#mealPlanAccordion">
                        <div class="accordion-body">${result.recommended_meal_plan.breakfast}</div>
                    </div>
                </div>
                <div class="accordion-item mb-2">
                    <h2 class="accordion-header" id="headingSnack1">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSnack1">
                            Snack 1 🥜
                        </button>
                    </h2>
                    <div id="collapseSnack1" class="accordion-collapse collapse" data-bs-parent="#mealPlanAccordion">
                        <div class="accordion-body">${result.recommended_meal_plan.snack1}</div>
                    </div>
                </div>
                <div class="accordion-item mb-2">
                    <h2 class="accordion-header" id="headingLunch">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseLunch">
                            Lunch 🍛
                        </button>
                    </h2>
                    <div id="collapseLunch" class="accordion-collapse collapse" data-bs-parent="#mealPlanAccordion">
                        <div class="accordion-body">${result.recommended_meal_plan.lunch}</div>
                    </div>
                </div>
                <div class="accordion-item mb-2">
                    <h2 class="accordion-header" id="headingSnack2">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSnack2">
                            Snack 2 🍎
                        </button>
                    </h2>
                    <div id="collapseSnack2" class="accordion-collapse collapse" data-bs-parent="#mealPlanAccordion">
                        <div class="accordion-body">${result.recommended_meal_plan.snack2}</div>
                    </div>
                </div>
                <div class="accordion-item mb-2">
                    <h2 class="accordion-header" id="headingSnack3">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSnack3">
                            Snack 3 🍌
                        </button>
                    </h2>
                    <div id="collapseSnack3" class="accordion-collapse collapse" data-bs-parent="#mealPlanAccordion">
                        <div class="accordion-body">${result.recommended_meal_plan.snack3}</div>
                    </div>
                </div>
                <div class="accordion-item mb-2">
                    <h2 class="accordion-header" id="headingDinner">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDinner">
                            Dinner 🍽️
                        </button>
                    </h2>
                    <div id="collapseDinner" class="accordion-collapse collapse" data-bs-parent="#mealPlanAccordion">
                        <div class="accordion-body">${result.recommended_meal_plan.dinner}</div>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="alert alert-danger text-center" role="alert">
                Oops! Something went wrong. Please try again.
            </div>
        `;
    }

    // Scroll to results
    resultContainer.scrollIntoView({ behavior: "smooth" });
};