import tkinter as tk


class MealPicker(tk.Frame):
    """
    Meal picker for the application.
    """

    def __init__(self, parent, database, side_panel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.database = database
        self.side_panel = side_panel
        self.create_widgets()
        self.pack(fill='both', expand=True)

    def create_widgets(self):
        """
        Create widgets for the meal picker.
        """
        self.meal_label = tk.Label(self, text="Enter meal name:")
        self.meal_label.pack(padx=10, pady=(10, 0))

        self.meal_entry = tk.Entry(self)
        self.meal_entry.pack(padx=200, pady=(0, 10), fill='x')

        self.search_button = tk.Button(self, text="Search", command=self.search_meals)
        self.search_button.pack(pady=(0, 20))

        self.results_listbox = tk.Listbox(self)
        self.results_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(self, orient='vertical', command=self.results_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_listbox.config(yscrollcommand=scrollbar.set)

    def search_meals(self):
        meal_name = self.meal_entry.get().lower()
        slider_values = self.side_panel.get_slider_values()

        nutrient_ranges = {
            'calories': (lambda v: (v - 100, v + 100)),
            'protein': (lambda v: (v - 5, v + 5)),
            'total_carb': (lambda v: (v - 10, v + 10)),
            'sugar': (lambda v: (v - 5, v + 5)),
            'total_fat': (lambda v: (v - 10, v + 10)),
        }

        matches = []
        for meal in self.database:
            if meal_name in meal['item'].lower():
                within_range = True
                for nutrient, get_range in nutrient_ranges.items():
                    slider_value = slider_values.get(nutrient)
                    if slider_value is None or slider_value == 0:
                        continue
                    range_min, range_max = get_range(slider_values[nutrient])
                    if meal[nutrient] != 'NA':
                        meal_value = int(meal[nutrient])
                    if not (range_min <= meal_value <= range_max):
                        within_range = False
                        break
                if within_range:
                    matches.append(meal)

        self.results_listbox.delete(0, tk.END)
        for meal in matches:
            self.results_listbox.insert(tk.END, f"Restaurant: {meal['restaurant']} - {meal['item']} - Calories: {meal['calories']} - Protein: {meal['protein']}")
