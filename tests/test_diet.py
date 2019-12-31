from diet import Meal
from .conftest import A_MEAL, A_MEAL_INFO_JSON, A_FOOD
from unittest import mock

MOCK_FOOD_DB = 'diet.get_food_from_db'


@mock.patch(MOCK_FOOD_DB)
def test_meal_from_dict(mock_food):
    """
    GIVEN a JSON containing a meal type and a list of food
    WHEN creating a meal from a dict
    THEN a Meal object is created properly
    """
    meal_expected = A_MEAL
    mock_food.return_value = A_FOOD

    meal_actual = Meal.from_dict(A_MEAL_INFO_JSON)

    assert meal_expected == meal_actual
