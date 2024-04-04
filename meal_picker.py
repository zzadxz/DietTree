import tkinter as tk
from graph import WeightedGraph


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

    def __init__(self, parent, database, side_panel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.database = database
        self.side_panel = side_panel
        self.create_widgets()
        self.pack(fill='both', expand=True)
        self.selected = None
        self.not_searching = False

    def create_widgets(self):
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

    def search_meals(self):
        """Uses meal name and slider values to filter through a database of meals according to the specified ranges of
        nutritional preferences. Then displays the filtered meals and associated information.
        """
        if self.not_searching:
            self.not_searching = True
            self.search_button.config(text="Search")

        meal_name = self.meal_entry.get().lower()
        slider_values = self.side_panel.get_slider_values()

        nutrient_ranges = {
            'Calories': (lambda v: (v - 100, v + 100)),
            'Protein (g)': (lambda v: (v - 5, v + 5)),
            'Carbs (g)': (lambda v: (v - 10, v + 10)),
            'Sugars (g)': (lambda v: (v - 5, v + 5)),
            'Total Fat (g)': (lambda v: (v - 10, v + 10)),
        }
        matches = []
        target_meals = ['calories', 'protein', 'total_carb', 'sugar', 'total_fat']
        adjusted_meal = {
            'calories': 'Calories',
            'protein': 'Protein (g)',
            'total_carb': 'Carbs (g)',
            'sugar': 'Sugars (g)',
            'total_fat': 'Total Fat (g)'
        }

        def parse_value(value):
            """Returns value as a float.

            If value begins with a '<' returns 0.5
            If value cannot be converted into a float returns 0
            """
            if value.strip() == 'NA' or not value.strip():
                return 0
            elif value.startswith('<'):
                return 0.5
            else:
                try:
                    return float(value)
                except ValueError:
                    return 0

        matches = []
        for meal in self.database:
            adjusted_meal = {
                k: parse_value(v) for k, v in meal.items() if k in nutrient_ranges
            }
            if meal_name.lower() in meal['Item'].lower():
                within_range = True
                for nutrient, get_range in nutrient_ranges.items():
                    slider_value = slider_values.get(nutrient)
                    if slider_value is None or slider_value == 0:
                        continue
                    range_min, range_max = get_range(slider_values[nutrient])
                    meal_value = adjusted_meal.get(nutrient, 0)
                    if not (range_min <= meal_value <= range_max):
                        within_range = False
                        break
                if within_range:
                    matches.append(meal)

        self.results_listbox.delete(0, tk.END)
        for meal in matches:
            self.results_listbox.insert(tk.END,
                                        f"Company: {meal['Company']} | Item: {meal['Item']} | Calories: {meal['Calories']} | Protein: {meal['Protein (g)']}")

    def return_similar_meals(self):
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
        'extra-imports': ['csv', 'networkx', 'pandas'],
        'max-nested-blocks': 4,
    })
