from app.diet import Diet
from app.utils.enums import Files


if __name__ == '__main__':
    diet = Diet(Files.DIET_JSON.value)