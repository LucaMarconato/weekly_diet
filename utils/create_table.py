import sqlite3

connection = sqlite3.connect('../foods.db')
cursor = connection.cursor()
cursor.execute('''\
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR,
    food_type VARCHAR,
    unit VARCHAR,
    calories_per_unit FLOAT,
    carbohydrates_per_unit FLOAT,
    proteins_per_unit FLOAT,
    fats_per_unit FLOAT
);
''')
connection.close()
