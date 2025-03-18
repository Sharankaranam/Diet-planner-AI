import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Sample diet dataset (condensed for visualization)
diet_data = {
    "Vegetarian": {
        "Breakfast": ["Oatmeal", "Fruit Salad", "Smoothie"],
        "Lunch": ["Grilled Cheese", "Vegetable Stir Fry"],
        "Dinner": ["Pasta Primavera", "Chickpea Curry"],
        "Snacks": ["Nuts", "Yogurt"]
    },
    "Non-Vegetarian": {
        "Breakfast": ["Egg Omelette", "Bacon & Eggs"],
        "Lunch": ["Chicken Salad", "Grilled Fish"],
        "Dinner": ["Steak", "Roast Chicken"],
        "Snacks": ["Beef Jerky", "Boiled Eggs"]
    },
    "Vegan": {
        "Breakfast": ["Avocado Toast", "Vegan Pancakes"],
        "Lunch": ["Lentil Soup", "Quinoa Salad"],
        "Dinner": ["Tofu Stir Fry", "Vegan Tacos"],
        "Snacks": ["Hummus & Veggies", "Fruit"]
    }
}

# Count number of meals per diet type
diet_counts = {diet: sum(len(meals) for meals in diet_data[diet].values()) for diet in diet_data}

# Prepare data for meal frequency
meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks"]
meal_counts = {diet: [len(diet_data[diet].get(meal, [])) for meal in meal_types] for diet in diet_data}

# Flatten all meals for ingredient analysis
all_meals = sum([sum(meals.values(), []) for meals in diet_data.values()], [])
ingredient_counts = Counter(all_meals).most_common(10)

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
colors = sns.color_palette("pastel")

# Pie chart - Diet type distribution
axes[0, 0].pie(diet_counts.values(), labels=diet_counts.keys(), autopct='%1.1f%%', colors=colors, startangle=140)
axes[0, 0].set_title("Diet Type Distribution")

# Bar chart - Meal frequency by type
x = range(len(meal_types))
for i, (diet, counts) in enumerate(meal_counts.items()):
    axes[0, 1].bar([p + i * 0.2 for p in x], counts, width=0.2, label=diet, color=colors[i])
axes[0, 1].set_xticks([p + 0.2 for p in x])
axes[0, 1].set_xticklabels(meal_types)
axes[0, 1].set_title("Meal Frequency by Type")
axes[0, 1].legend()

# Horizontal bar chart - Popular Ingredients
ingredients, counts = zip(*ingredient_counts)
axes[1, 0].barh(ingredients, counts, color=sns.color_palette("magma", len(ingredients)))
axes[1, 0].set_title("Popular Ingredients")

# Stacked bar chart - Meal type comparison
bottom_values = [0] * len(meal_types)
for i, (diet, counts) in enumerate(meal_counts.items()):
    axes[1, 1].bar(meal_types, counts, bottom=bottom_values, label=diet, color=colors[i])
    bottom_values = [bottom_values[j] + counts[j] for j in range(len(meal_types))]
axes[1, 1].set_title("Meal Type Comparison")
axes[1, 1].legend()

plt.tight_layout()
plt.show()
