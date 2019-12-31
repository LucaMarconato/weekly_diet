import sqlite3

import pandas as pd

df = pd.read_csv('foods.csv')

connection = sqlite3.connect('../foods.db')
cursor = connection.cursor()
for row in df.iterrows():
    name = row[1][0]
    meal_type = row[1][1]
    food_type = row[1][2]
    calories = row[1][3]
    carbs = row[1][4]
    prots = row[1][5]
    fats = row[1][6]
    cursor.execute('INSERT OR REPLACE INTO foods VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (name, meal_type, food_type, calories, carbs, prots, fats))
    print(f'inserted {name}')
connection.commit()
connection.close()
