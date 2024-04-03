import tkinter as tk
from graph import WeightedGraph


class MealPicker(tk.Frame):
    """
    Meal picker for the application.
    """

    def __init__(self, parent, database, side_panel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.database = database
        self.side_panel = side_panel
        self.create_widgets()
        self.pack(fill='both', expand=True)
        self.selected = None

    def create_widgets(self):
        """
        Create widgets for the meal picker.
        """

        bg = tk.PhotoImage(file="fancy_tree.png")
        canvas1 = tk.Label(self, image=bg)
        canvas1.place(x=0, y=0, relwidth=1, relheight=1)

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
        """
        TODO
        """
        meal_name = self.meal_entry.get().lower()
        slider_values = self.side_panel.get_slider_values()

        nutrient_ranges = {
            'calories': (lambda v: (v - 100, v + 100)),
            'protein': (lambda v: (v - 5, v + 5)),
            'total_carb': (lambda v: (v - 10, v + 10)),
            'sugar': (lambda v: (v - 5, v + 5)),
            'total_fat': (lambda v: (v - 10, v + 10)),
        }
        # (abs.(500/700) * 10) + (abs.(10/5) * 5)  = 10
        # add_edge(big_mac, whopper, 10)

        # calories1 = 200_300
        # calories2 = 300_400
        # sugar1 = 5-10
        # ...
        # food1 = big_mac
        # f2 = whopper
        matches = []
        target_meals = ['calories', 'protein', 'total_carb', 'sugar', 'total_fat']

        for meal in self.database:
            adjusted_meal = {k: int(v) if v != 'NA' else v for k, v in meal.items() if k in target_meals}
            if meal_name.lower() in meal['item'].lower():
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
                    else:
                        within_range = False
                        break
                if within_range:
                    matches.append(meal)

        self.results_listbox.delete(0, tk.END)
        for meal in matches:
            self.results_listbox.insert(tk.END,
                                        f"Restaurant: {meal['restaurant']} | {meal['item']} | Calories: {meal['calories']} | Protein: {meal['protein']}")

    def return_similar_meals(self):
        """
        TODO
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
