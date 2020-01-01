import json
from typing import Dict
from app.utils.enums import MealType, Files
from foods import get_food_from_db


class Meal:

    def __init__(self):
        self.type = None
        self.foods = list()

    @classmethod
    def from_dict(cls, meal_info: Dict):
        meal = cls()
        meal.type = MealType.from_string(meal_info['meal_type'])
        meal.foods = [get_food_from_db(food['name'], food['quantity']) for food in meal_info['foods']]
        return meal

    def to_dict(self) -> Dict:
        return dict(meal_type=self.type.value, foods=[food.to_dict() for food in self.foods])

    def __eq__(self, other):
        return self.type == other.type and self.foods == other.foods


class Day:

    def __init__(self):
        self.name = None
        self.meals = list()

    @classmethod
    def from_dict(cls, j: Dict):
        day = cls()
        day.name = j['day']
        day.meals = [Meal.from_dict(x) for x in j['meals']]
        return day

    def to_dict(self) -> Dict:
        return dict(day=self.name, meals=[meal.to_dict() for meal in self.meals])

    def __eq__(self, other):
        return self.name == other.name and self.meals == other.meals


class Diet:

    def __init__(self, json_filename: str):
        with open(json_filename) as infile:
            days = json.load(infile)['days']
        self.days = [Day.from_dict(x) for x in days]

    def save(self, outfile=Files.DIET_JSON.value):
        days_json = {'days': [day.to_dict() for day in self.days]}
        with open(outfile, 'w') as outfile:
            json.dump(days_json, outfile, indent=2)
