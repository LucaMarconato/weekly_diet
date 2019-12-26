from diet import Diet
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict


def generate_shopping_list(diet: Diet) -> Dict[str, int]:
    shopping_list = dict()
    for day in diet.days:
        for meal in day.meals:
            for food in meal.foods:
                key = f'{food.name} ({food.unit.name})'
                if key not in shopping_list:
                    shopping_list[key] = 0
                shopping_list[key] += food.quantity
    return shopping_list


def generate_daily_intake_information(diet: Diet) -> pd.DataFrame:
    df = pd.DataFrame()
    df['calories'] = None
    df['carbohydrates'] = None
    df['proteins'] = None
    df['fats'] = None
    for day in diet.days:
        total_calories = 0
        total_carbohydrates = 0
        total_proteins = 0
        total_fats = 0
        for meal in day.meals:
            for food in meal.foods:
                calories = food.calories_per_unit * food.quantity
                carbohydrates = food.carbohydrates_per_unit * food.quantity
                proteins = food.proteins_per_unit * food.quantity
                fats = food.fats_per_unit * food.quantity
                total_calories += calories
                total_carbohydrates += carbohydrates
                total_proteins += proteins
                total_fats += fats
        df.loc[day.day_name] = [total_calories, total_carbohydrates, total_proteins, total_fats]
    return df


def plot_nutrients_fragmentation(diet: Diet):
    df = generate_daily_intake_information(diet)
    df['day'] = df.index

    fig, (ax0, ax1) = plt.subplots(2, 1, constrained_layout=True)
    sns.barplot(x='day', y='calories', data=df, ax=ax0, color='red')
    ax0.set_xlabel('')

    x = np.arange(7)
    width = 0.5
    p_carbs = plt.bar(x, df['carbohydrates'], width)
    p_prots = plt.bar(x, df['proteins'], width, bottom=df['carbohydrates'])
    p_fats = plt.bar(x, df['fats'], width, bottom=df['carbohydrates'] + df['proteins'])
    plt.ylabel('nutrients (gr)')
    fig.suptitle('nutrients fragmentation')
    ax1.set_xticks(x)
    ax1.set_xticklabels(list(df.index))
    ax1.legend((p_carbs[0], p_prots[0], p_fats[0]), ('carbohydrates', 'proteins', 'fats'), bbox_to_anchor=(0.5, -0.2), loc='center', ncol=3)
    plt.show()



if __name__ == '__main__':
    diet = Diet('diet.json')
    shopping_list = generate_shopping_list(diet)
    print('\nshopping list:')
    for k, v in sorted(shopping_list.items()):
        print(f'{k}: {v}')

    print('')
    df = generate_daily_intake_information(diet)
    for row in df.iterrows():
        print(row[0])
        for k, v in row[1].items():
            print(' ' * 4, end='')
            print(f'{k}: {round(v)}')

    plot_nutrients_fragmentation(diet)
