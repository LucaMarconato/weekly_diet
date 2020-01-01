import re
from threading import Lock
from typing import Dict

import PyQt5.uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication

from app.utils.enums import MealType, UiThemes
from app.diet import Diet, Day, Meal
from foods import Food, FoodType, FoodUnit, derived_foods, get_all_foods_from_db, get_food_from_db
from mpl_plot_widget import MyMplCanvas


class DraggableListWidget(QtWidgets.QListWidget):
    diet_changed = PyQt5.QtCore.pyqtSignal()

    def __init__(self, rows_are_deletable=True):
        super().__init__()
        self.rows_are_deletable = rows_are_deletable
        self.backspace_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Backspace),
                                                      self, context=PyQt5.QtCore.Qt.WidgetWithChildrenShortcut)
        self.refresh_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+R'),
                                                    self, context=PyQt5.QtCore.Qt.WidgetWithChildrenShortcut)
        if self.rows_are_deletable:
            self.backspace_shortcut.activated.connect(self.delete_selected_item)
            self.refresh_shortcut.activated.connect(self.on_refresh_pressed)
        list_model = self.model()
        list_model.dataChanged.connect(self.on_data_changed)
        list_model.rowsRemoved.connect(self.on_rows_removed)
        list_model.rowsMoved.connect(self.on_rows_moved)

    @PyQt5.QtCore.pyqtSlot()
    def on_refresh_pressed(self):
        self.diet_changed.emit()

    # moved two rows within the same meal widget (e.g. from monday lunch to monday lunch)
    @PyQt5.QtCore.pyqtSlot()
    def on_rows_moved(self):
        self.diet_changed.emit()

    @PyQt5.QtCore.pyqtSlot()
    def on_data_changed(self):
        # I am having this problem: https://www.qtcentre.org/threads/63027-QListWidget-access-to-index-and-item-after
        # -drag-and-drop-event, that is I cannot distinguish between this signal being called because of a move
        # operation between, say, monday lunch and monday tuesday, and copy operations between the menu and, say,
        # monday lunch. The following is very very ugly but it fixes the problem and the performance is good. One
        # could use the same idea of this hack but implement it in a more performant way by checking if "something
        # which is called something like app.focusWidget()" is among the list of menu widgets. This should be faster
        # than accessing each widget and checking if they have focus
        gui = self.parent().parent()
        if hasattr(gui, 'menu_categories_widgets'):
            the_focus_is_in_one_of_the_menu_widgets = False
            for widget in gui.menu_categories_widgets.values():
                if widget.hasFocus():
                    the_focus_is_in_one_of_the_menu_widgets = True
            # copied of one row from a menu widget to a meal widget (e.g. from desserts to monday lunch)
            if the_focus_is_in_one_of_the_menu_widgets:
                self.diet_changed.emit()

    @PyQt5.QtCore.pyqtSlot()
    def on_rows_removed(self):
        # moved one row from a meal widgt to a different meal widget (e.g. from monday breakfast to tuesday lunch)
        self.diet_changed.emit()

    def focusOutEvent(self, QFocusEvent):
        self.clearSelection()

    @PyQt5.QtCore.pyqtSlot()
    def delete_selected_item(self):
        selected = self.selectedItems()
        if len(selected) == 1:
            self.takeItem(self.row(selected[0]))


class DayGui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        PyQt5.uic.loadUi(UiThemes.DAY.value, self)
        self.day_name = self.layout().itemAt(0).widget()
        self.meal_widgets: Dict[MealType, DraggableListWidget] = dict()
        for i, meal_type in zip(range(2, 19, 3), MealType):
            widget_to_remove = self.layout().itemAt(i).widget()
            self.layout().removeWidget(widget_to_remove)
            self.meal_widgets[meal_type] = DraggableListWidget()
            self.meal_widgets[meal_type].setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
            self.meal_widgets[meal_type].setDefaultDropAction(PyQt5.QtCore.Qt.MoveAction)
            self.layout().insertWidget(i, self.meal_widgets[meal_type])

    def set_day(self, name: str):
        self.day_name.setText(name)

    def add_food_to_meal(self, food: Food, meal_type: MealType):
        unit = food.unit.name if food.unit.name != 'item' else 'x'
        s = f'{food.quantity} {unit} {food.name}'
        item = QtWidgets.QListWidgetItem(s)
        item.setFlags(item.flags() | PyQt5.QtCore.Qt.ItemIsEditable)
        self.meal_widgets[meal_type].addItem(item)


class Gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        PyQt5.uic.loadUi(UiThemes.GUI.value, self)
        self.canvas = MyMplCanvas()
        self.canvas.setMaximumHeight(500)
        self.canvas.setMinimumHeight(400)
        self.vbox_layout = self.layout().itemAt(0)
        placeholder_widget = self.vbox_layout.itemAt(1).widget()
        self.vbox_layout.removeWidget(placeholder_widget)
        self.vbox_layout.insertWidget(1, self.canvas)
        self.hbox_layout = self.vbox_layout.itemAt(0)
        self.day_guis = list()
        self.update_diet_lock = Lock()

        self.diet = Diet('diet.json')

        for day in self.diet.days:
            day_gui = DayGui()
            self.day_guis.append(day_gui)
            self.hbox_layout.addWidget(day_gui)
            day_gui.set_day(day.name)
            for meal in day.meals:
                for food in meal.foods:
                    day_gui.add_food_to_meal(food, meal.type)

        self.menu_widget = self.layout().itemAt(1).widget()
        self.menu_categories_widgets: Dict[FoodType, DraggableListWidget] = dict()
        for i, food_type in zip(range(1, 14, 3), FoodType):
            widget_to_remove = self.menu_widget.layout().itemAt(i).widget()
            self.menu_widget.layout().removeWidget(widget_to_remove)
            self.menu_categories_widgets[food_type] = DraggableListWidget(rows_are_deletable=False)
            self.menu_categories_widgets[food_type].setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragOnly)
            self.menu_widget.layout().insertWidget(i, self.menu_categories_widgets[food_type])
        self.menu_categories_widgets[FoodType.placeholder].setMaximumHeight(60)

        all_edible_foods = [food for food in get_all_foods_from_db() if food.unit == FoodUnit.item]
        all_edible_foods.extend(derived_foods)
        all_edible_foods = sorted(all_edible_foods, key=lambda x: x.name)
        for food in all_edible_foods:
            item = QtWidgets.QListWidgetItem(f'1 x {food.name}')
            self.menu_categories_widgets[food.food_type].addItem(item)

        for day_gui in self.day_guis:
            for widget in day_gui.meal_widgets.values():
                widget.diet_changed.connect(self.on_diet_changed)

    # the widget has been modified by the user, so we want to recreate the diet class to reflect the user changes
    def update_diet_from_widgets(self):
        self.update_diet_lock.acquire()
        self.diet.days = list()
        for day_gui in self.day_guis:
            day = Day()
            self.diet.days.append(day)
            day.name = day_gui.day_name.text()
            # print(day.day_name)
            for meal_type, meal_widget in day_gui.meal_widgets.items():
                old_state = meal_widget.blockSignals(True)
                meal = Meal()
                day.meals.append(meal)
                meal.type = meal_type
                # print(meal.meal_type.name)
                model = meal_widget.model()
                i = 0
                while i < model.rowCount():
                    item_data = model.itemData(model.index(i))
                    if len(item_data) == 1:
                        s = item_data[0]
                        regexp = re.compile(r'([0-9]+) [a-zA-Z]+ ([a-zA-Z0-9 ]+)')
                        match = re.match(regexp, s)
                        groups = match.groups()
                        assert len(groups) == 2
                        quantity = int(groups[0])
                        food_name = groups[1]
                        food = get_food_from_db(food_name)
                        # if the food is derived we add its ingredient to the diet, instead of the food itself,
                        # this is to make explicit what a derived food is made of, and also to allow for the
                        # customization of its ingredients
                        if food.name in [food.name for food in derived_foods]:
                            assert quantity == 1
                            for component in food.ingredients:
                                meal.foods.append(component)
                                unit = component.unit.name if component.unit.name != 'item' else 'x'
                                s = f'{component.quantity} {unit} {component.name}'
                                item = QtWidgets.QListWidgetItem(s)
                                meal_widget.insertItem(i + 1, item)
                                i += 1
                                pass
                        else:
                            food.quantity = quantity
                            meal.foods.append(food)
                        # print(food.name)
                    i += 1

                i = 0
                while i < model.rowCount():
                    item_data = model.itemData(model.index(i))
                    if len(item_data) == 1:
                        s = item_data[0]
                        regexp = re.compile(r'([0-9]+) [a-zA-Z]+ ([a-zA-Z0-9 ]+)')
                        match = re.match(regexp, s)
                        groups = match.groups()
                        assert len(groups) == 2
                        quantity = int(groups[0])
                        food_name = groups[1]
                        if food_name in [food.name for food in derived_foods]:
                            assert quantity == 1
                            meal_widget.takeItem(i)
                            break
                    i += 1

                # old_state = meal_widget.blockSignals(True)
                for i in range(meal_widget.count()):
                    row = meal_widget.item(i)
                    row.setFlags(row.flags() | PyQt5.QtCore.Qt.ItemIsEditable)
                meal_widget.blockSignals(old_state)
        self.update_diet_lock.release()

    @PyQt5.QtCore.pyqtSlot()
    def on_diet_changed(self):
        self.update_diet_from_widgets()
        self.diet.save()
        self.canvas.update_figure(self.diet)


if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QApplication([])
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())
