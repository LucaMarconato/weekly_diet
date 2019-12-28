from enum import IntEnum, Enum, auto
from typing import List, Dict
from foods import Food, FoodType, FoodUnit, get_food_from_db
import json

MealType = Enum('MealType', 'breakfast mid_morning lunch mid_afternoon late_afternoon dinner')


class Meal:
    def __init__(self):
        self.meal_type = None
        self.foods = list()

    def from_dict(self, j: Dict):
        self.meal_type = MealType[j['meal_type']]
        for food_j in j['foods']:
            food_name = food_j['name']
            quantity = food_j['quantity']
            food = get_food_from_db(food_name)
            food.quantity = quantity
            self.foods.append(food)


class Day:
    def __init__(self):
        self.day_name = None
        self.meals = list()

    def from_dict(self, j: Dict):
        self.day_name = j['day']
        for meal_j in j['meals']:
            meal = Meal()
            meal.from_dict(meal_j)
            self.meals.append(meal)


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
