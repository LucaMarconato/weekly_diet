from enum import IntEnum, Enum, auto
from typing import List, Dict
from foods import Food, FoodType, FoodUnit, get_food_from_db
import json

MealType = Enum('MealType', 'breakfast lunch dinner mid_morning mid_afternoon late_afternoon')


class Meal:
    def from_dict(self, j: Dict):
        self.meal_type = MealType[j['meal_type']]
        self.foods = list()
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
        self.meals = list()
        with open(json_filename) as infile:
            j = json.load(infile)
        for j_day in j['days']:
            day = Day()
            day.from_dict(j_day)
            self.days.append(day)


if __name__ == '__main__':
    diet = Diet('diet.json')
