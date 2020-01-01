import json
import pytest
from app.diet import Meal, MealType, Day
from foods import Food, FoodType, FoodUnit

A_FOOD_NAME = 'Dried Super Mushrooms'
A_FOOD_QUANTITY = 1

A_MEAL_INFO_JSON = {'meal_type': 'dinner', 'foods': [{'name': A_FOOD_NAME, 'quantity': 5}]}
A_DAY_JSON = {'day': 'saturday', 'meals': [A_MEAL_INFO_JSON]}


@pytest.fixture(scope='function')
def a_food():
    food = Food(A_FOOD_NAME, FoodType['dolce'], FoodUnit['item'], 1337, 10, 20, 400)
    food.quantity = A_FOOD_QUANTITY
    return food


@pytest.fixture(scope='function')
def a_meal(a_food):
    meal = Meal()
    meal.type = MealType.DINNER
    meal.foods = [a_food]
    return meal


@pytest.fixture(scope='function')
def a_day(a_meal):
    day = Day()
    day.name = 'saturday'
    day.meals = [a_meal]
    return day


@pytest.fixture(scope='function')
def other_day(a_meal):
    day = Day()
    day.name = 'sunday'
    day.meals = [a_meal]
    return day


@pytest.fixture(scope='function')
def days_json_file(tmpdir_factory, a_day, other_day):
    file_path = tmpdir_factory.mktemp('data').join('days.json')
    with open(file_path, 'w') as f:
        data = dict(days=[a_day.to_dict(), other_day.to_dict()])
        f.write(json.dumps(data))
    return file_path
