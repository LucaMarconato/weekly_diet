from enum import Enum
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent


class UiThemes(Enum):
    DAY = f'{FILE_PATH}/ui/day.ui'
    GUI = f'{FILE_PATH}/ui/gui.ui'


class MealType(Enum):
    BREAKFAST = 0,
    MID_MORNING = 1,
    LUNCH = 2,
    MID_AFTERNOON = 3,
    LATE_AFTERNOON = 4,
    DINNER = 5

    @staticmethod
    def from_string(meal_type):
        meal_type = meal_type.lower()
        if 'breakfast' in meal_type:
            return MealType.BREAKFAST
        elif all([x in meal_type for x in ['mid', 'morning']]):
            return MealType.MID_MORNING
        elif 'lunch' in meal_type:
            return MealType.LUNCH
        elif all([x in meal_type for x in ['mid', 'afternoon']]):
            return MealType.MID_AFTERNOON
        elif all([x in meal_type for x in ['late', 'afternoon']]):
            return MealType.LATE_AFTERNOON
        elif 'dinner' in meal_type:
            return MealType.DINNER
        else:
            raise NotImplementedError
