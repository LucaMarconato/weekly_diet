import sqlite3
from enum import Enum

FoodType = Enum('FoodType', 'dolce primo secondo contorno placeholder')
FoodUnit = Enum('FoodUnit', 'item gr ml spoon')


class Food:
    def __init__(self, name: str, food_type: FoodType, unit: FoodUnit, calories_per_unit: float,
                 carbohydrates_per_unit: float, proteins_per_unit: float, fats_per_unit: float):
        self.name = name
        self.food_type = food_type
        self.unit = unit
        self.calories_per_unit = calories_per_unit
        self.carbohydrates_per_unit = carbohydrates_per_unit
        self.proteins_per_unit = proteins_per_unit
        self.fats_per_unit = fats_per_unit
        self.quantity = None


def get_food_from_db(name: str) -> Food:
    connection = sqlite3.connect('foods.db')
    cursor = connection.cursor()
    rows = cursor.execute('SELECT * FROM foods WHERE name = (?)', (name, )).fetchall()
    connection.close()
    assert len(rows) == 1
    row = rows[0]
    food = Food(name=row[0],
                food_type=FoodType[row[1]],
                unit=FoodUnit[row[2]],
                calories_per_unit=row[3],
                carbohydrates_per_unit=row[4],
                proteins_per_unit=row[5],
                fats_per_unit=row[6])
    return food
