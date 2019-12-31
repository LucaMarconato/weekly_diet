import json
from typing import Dict
from app.utils.enums import MealType
from foods import get_food_from_db


class Meal:

    def __init__(self):
        self.meal_type = None
        self.foods = list()

    @classmethod
    def from_dict(cls, meal_info: Dict):
        meal = cls()
        meal.meal_type = MealType.from_string(meal_info['meal_type'])
        meal.foods = [get_food_from_db(food['name'], food['quantity']) for food in meal_info['foods']]
        return meal

    def __eq__(self, other):
        return (self.meal_type == other.meal_type and
                all([x == y for x, y in zip(self.foods, other.foods)]))


class Day:
    def __init__(self):
        self.day_name = None
        self.meals = list()

    def from_dict(self, j: Dict):
        self.day_name = j['day']
        self.meals = [Meal.from_dict(x) for x in j['meals']]


class Diet:
    def __init__(self, json_filename: str):
        self.days = list()
        with open(json_filename) as infile:
            j = json.load(infile)
        for j_day in j['days']:
            day = Day()
            day.from_dict(j_day)
            self.days.append(day)

    def save(self):
        j = dict()
        j['days'] = list()
        for day in self.days:
            j_day = dict()
            j['days'].append(j_day)
            j_day['day'] = day.day_name
            j_day['meals'] = list()
            for meal in day.meals:
                j_meal = dict()
                j_day['meals'].append(j_meal)
                j_meal['meal_type'] = meal.meal_type.name
                j_meal['foods'] = list()
                for food in meal.foods:
                    j_food = dict()
                    j_meal['foods'].append(j_food)
                    j_food['name'] = food.name
                    j_food['quantity'] = food.quantity
        with open('diet.json', 'w') as outfile:
            json.dump(j, outfile, indent=2)


if __name__ == '__main__':
    diet = Diet('diet.json')
