import json

from app.diet import Meal, Day, Diet
from app.utils.enums import Files
from .conftest import A_MEAL_INFO_JSON, A_DAY_JSON
from unittest import mock

MOCK_FOOD_DB = 'app.diet.get_food_from_db'


@mock.patch(MOCK_FOOD_DB)
def test_meal_from_dict(mock_db, a_food, a_meal):
    """
    GIVEN a JSON containing a meal type and a list of food
    WHEN creating a meal from a dict
    THEN a Meal object is created properly
    """
    mock_db.return_value = a_food

    meal_actual = Meal.from_dict(A_MEAL_INFO_JSON)

    assert meal_actual == a_meal


@mock.patch(MOCK_FOOD_DB)
def test_day_from_string(mock_db, a_food, a_day):
    """
    GIVEN a JSON containing a meal type and a list of food
    WHEN creating a day from a list of meals
    THEN a Day object with a list of meals is created properly
    """
    mock_db.return_value = a_food

    day_actual = Day.from_dict(A_DAY_JSON)

    assert day_actual == a_day


@mock.patch(MOCK_FOOD_DB)
def test_diet_load_days_from_json_file(mock_db, days_json_file, a_food, a_day, other_day):
    """
    WHEN creating a Diet from a JSON file containing days
    THEN the data from the file is stored in the object
    """
    mock_db.return_value = a_food

    diet = Diet(days_json_file)

    assert diet.days == [a_day, other_day]


@mock.patch(MOCK_FOOD_DB)
def test_diet_save_json_to_file(mock_db, a_food, days_json_file):
    """
    GIVEN a diet loaded with days
    WHEN saving the object
    THEN a JSON file containing the object's data is created properly
    """
    mock_db.return_value = a_food
    diet = Diet(days_json_file)
    with open(days_json_file) as f:
        diet_expected = json.load(f)

    diet.save(outfile=days_json_file)
    with open(days_json_file) as f:
        diet_actual = json.load(f)

    assert diet_actual == diet_expected
