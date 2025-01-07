from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Base URLs
BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"
DETAILS_URL = "https://www.themealdb.com/api/json/v1/1/lookup.php"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        search_query = request.form.get("query")
        response = requests.get(BASE_URL, params={"s": search_query})
        recipes = response.json().get("meals", [])
        return render_template("back.html", recipes=recipes)
    return render_template("front.html")


@app.route('/meal/<meal_id>')
def meal_detail(meal_id):
    try:
        # Fetch meal data from API
        response = requests.get(DETAILS_URL, params={"i": meal_id})

        if response.status_code == 200:
            data = response.json()
            if data.get('meals') and len(data['meals']) > 0:
                # Process valid data
                meal = data['meals'][0]

                # Extract general details
                name = meal.get('strMeal', 'Unknown Dish')
                category = meal.get('strCategory', 'Unknown Category')
                area = meal.get('strArea', 'Unknown Origin')
                image_url = meal.get('strMealThumb', '')
                
                # Extract nutritional information
                calories = meal.get('strCalories', 'N/A')  # Fetch if exists
                fat = meal.get('strFat', 'N/A')
                protein = meal.get('strProtein', 'N/A')
                carbs = meal.get('strCarbs', 'N/A')
                
                summary = (
                    f"{name} is a traditional {category} dish from {area}. This dish is renowned for its rich flavors, "
                    f"unique preparation method, and cultural significance in its respective region. "
                    f"{name} has become a beloved choice for those who enjoy exploring diverse culinary traditions."
                )
                
                # Additional details for ratings and reviews if available
                rating = meal.get('strRating', 'N/A')  # Example placeholder
                review = meal.get('strReview', 'N/A')  # Example placeholder
                
            else:
                # Handle case if no meal is found
                meal = {'strMeal': 'Unknown Meal', 'strMealThumb': ''}
                summary = "No data available about this dish."
                rating = "N/A"
                review = "N/A"
        else:
            # Handle bad response code
            meal = {'strMeal': 'Unknown Meal', 'strMealThumb': ''}
            summary = 'Unable to fetch dish information.'
            rating = "N/A"
            review = "N/A"

        # Debug logs
        print("Meal Data (Before Sending to Template):", meal)
        print("Summary Data (Before Sending to Template):", summary)
        print("Nutritional Information - Calories:", calories)
        print("Rating:", rating, "Review:", review)

        # Pass data to the template
        return render_template(
            "detail.html",
            meal=meal,
            summary=summary,
            calories=calories,
            fat=fat,
            protein=protein,
            carbs=carbs,
            rating=rating,
            review=review
        )

    except Exception as e:
        # Log exception details
        print("Error during render_template:", e)
        return f"An error occurred: {e}"


if __name__ == "__main__":
    app.run(debug=True)
