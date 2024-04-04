"""Meal Picker module for the application."""
import tkinter as tk
from typing import Any, Optional


class MealPicker(tk.Frame):
    """Meal picker for the application.

    Instance Attributes:
        - parent: The parent object or container.
        - database: The database containing meal data.
        - side_panel: The side panel object for nutritional preferences.
        - selected: The currently selected item.
    Representation Invariants:
        - TODO
    """
    parent: tk.Widget
    database: Any
    side_panel: tk.Widget
    selected: Optional[Any]
    not_searching: bool
    meal_label: tk.Label
    meal_entry: tk.Entry
    search_button: tk.Button
    results_listbox: tk.Listbox

    def __init__(self, parent: tk.Widget, database: Any, side_panel: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.database = database
        self.side_panel = side_panel
        self.create_widgets()
        self.pack(fill='both', expand=True)
        self.selected = None
        self.not_searching = False

    def create_widgets(self) -> None:
        """Create widgets for the meal picker.
        """
        self.meal_label = tk.Label(self, text="Enter meal name:")
        self.meal_label.pack(padx=10, pady=(10, 0))

        self.meal_entry = tk.Entry(self)
        self.meal_entry.pack(padx=200, pady=(0, 10), fill='x')

        self.search_button = tk.Button(self, text="Search", command=self.search_meals, width=10, height=2)
        self.search_button.pack(pady=(0, 20))

        self.results_listbox = tk.Listbox(self, width=100, height=500)
        self.results_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(self, orient='vertical', command=self.results_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_listbox.config(yscrollcommand=scrollbar.set)

    def parse_value(self, value: str) -> float:
        """Parse a string value into a float."""
        if value.strip() == 'NA' or not value.strip():
            return 0
        elif value.startswith('<'):
            return 0.5
        else:
            try:
                return float(value)
            except ValueError:
                return 0

    def meal_fits_criteria(self, meal: dict, nutrient_ranges: dict, slider_values: dict) -> bool:
        """Determines if a meal fits within the specified nutrient ranges based on slider values."""
        for nutrient, get_range in nutrient_ranges.items():
            slider_value = slider_values.get(nutrient)
            if slider_value is None or slider_value == 0:
                continue
            range_min, range_max = get_range(slider_value)
            meal_value = self.parse_value(meal.get(nutrient, '0'))
            if not range_min <= meal_value <= range_max:
                return False
        return True

    def search_meals(self) -> None:
        """Filter through a database of meals based on nutritional preferences."""
        if self.not_searching:
            self.search_button.config(text="Search")

        meal_name = self.meal_entry.get().lower()
        slider_values = self.side_panel.get_slider_values()

        matches = [
            db_meal for db_meal in self.database
            if meal_name.lower() in db_meal['Item'].lower()
               and self.meal_fits_criteria(db_meal, self.define_nutrient_ranges(), slider_values)
        ]

        self.results_listbox.delete(0, tk.END)
        for meal in matches:
            self.results_listbox.insert(tk.END, self.format_meal_description(meal))

    def define_nutrient_ranges(self) -> dict:
        """Defines the nutrient ranges for filtering meals."""
        return {
            'Calories': lambda v: (v - 100, v + 100),
            'Protein (g)': lambda v: (v - 5, v + 5),
            'Carbs (g)': lambda v: (v - 10, v + 10),
            'Sugars (g)': lambda v: (v - 5, v + 5),
            'Total Fat (g)': lambda v: (v - 10, v + 10),
        }

    def format_meal_description(self, meal: dict) -> str:
        """Formats the meal description for display."""
        return (
            f"Company: {meal['Company']} | Item: {meal['Item']}"
            f" | Calories: {meal['Calories']} | Protein: {meal['Protein (g)']}"
        )

    def return_similar_meals(self) -> Optional[str]:
        """Returns the currently selected food item if available.
        If not, returns None.
        """
        try:
            return self.results_listbox.get(self.results_listbox.curselection())
        except AttributeError:
            return None


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # # increases the running time of the functions/methods.
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'allowed-import-modules': ['doctest', 'python_ta', 'tkinter', 'graph', 'python_ta.contracts'],
        'extra-imports': ['csv', 'networkx', 'pandas', 'typing'],
        'max-nested-blocks': 4,
    })
