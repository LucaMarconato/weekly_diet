from diet import Diet
from foods import derived_foods
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict


def generate_shopping_list(diet: Diet) -> Dict[str, int]:
    shopping_list = dict()
    def add_to_shopping_list(food):
        key = f'{food.name} ({food.unit.name})'
        if key not in shopping_list:
            shopping_list[key] = 0
        shopping_list[key] += food.quantity

    for day in diet.days:
        for meal in day.meals:
            for food in meal.foods:
                if food.name in [food.name for food in derived_foods]:
                    for ingredient in food.ingredients:
                        add_to_shopping_list(ingredient)
                else:
                    add_to_shopping_list(food)
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
                total_calories += food.calories()
                total_carbohydrates += food.carbohydrates()
                total_proteins += food.proteins()
                total_fats += food.fats()
        df.loc[day.day_name] = [total_calories, total_carbohydrates, total_proteins, total_fats]
    return df


def plot_into_axes(diet, ax0, ax1, legend_background_color=None):
    df = generate_daily_intake_information(diet)
    df['day'] = df.index
    sns.barplot(x='day', y='calories', data=df, color='red', ax=ax0)
    ax0.set_xlabel('')
    ax0.set_ylabel('kcal')
    ax0.axhline(3000, ls='--', color='red')

    df_melted = df.copy()
    df_melted.drop(['calories'], axis=1, inplace=True)
    df_melted = df_melted.melt(id_vars=['day'], value_vars=['carbohydrates', 'proteins', 'fats'])
    sns.barplot(x='day', y='value', hue='variable', data=df_melted, palette='deep', ax=ax1)
    ax1.set_xlabel('')
    legend = ax1.legend(ncol=3, bbox_to_anchor=(0.5, -0.3), loc='center')
    legend_colors = [x._facecolor for x in legend.legendHandles]
    if legend_background_color is not None:
        legend.get_frame().set_color(legend_background_color)
    ax1.axhline(400, ls='--', color=legend_colors[0])
    ax1.axhline(150, ls='--', color=legend_colors[1])
    ax1.axhline(80, ls='--', color=legend_colors[2])


def plot_nutrients_fragmentation(diet: Diet):
    fig, (ax0, ax1) = plt.subplots(2, 1, constrained_layout=True, figsize=(12, 5))
    plot_into_axes(diet, ax0, ax1)
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
