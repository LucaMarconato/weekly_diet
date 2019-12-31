from diet import Meal, MealType
from foods import Food, FoodType, FoodUnit

A_FOOD_NAME = 'Cabbage'
A_FOOD = Food(A_FOOD_NAME, FoodType['dolce'], FoodUnit['item'], 1337, 10, 20, 400)

A_MEAL_INFO_JSON = {'meal_type': 'dinner', 'foods': [{'name': A_FOOD_NAME, 'quantity': 5}]}
A_MEAL = Meal()
A_MEAL.meal_type = MealType.DINNER
A_MEAL.foods = [A_FOOD]
