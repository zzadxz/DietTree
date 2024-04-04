import tkinter as tk
from typing import Any, Dict

from graph import WeightedGraph
# from graph import load_graph
from meal_picker import MealPicker
from side_panel import SidePanel
from vertex import WeightedVertex
from tkinter import messagebox


class WelcomePage(tk.Frame):
    """
    Welcome page for the application.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.welcome_label = tk.Label(self, text="Welcome to AltMeal!", font=("Roboto", 28, "bold"))
        self.welcome_label.grid(row=0, column=0, pady=(50, 10), padx=50)

        self.continue_button = tk.Button(self,
                                         text="Find closest meal",
                                         command=self.on_continue,
                                         font=("Roboto", 18),
                                         width=25,
                                         height=2)
        self.continue_button.grid(row=1, column=0)
        self.select_weightings()
        self.selected_item = None
        self.first_click = True

    def on_continue(self):
        """
        Actions when 'Continue' is clicked
        """
        main_graph = None
        nutritional_info = None
        if self.first_click:
            categories_increments = {'Calories': 100, 'Protein (g)': 10, 'Carbs (g)': 10, 'Sugars (g)': 5,
                                     'Total Fat (g)': 5, 'Sodium (mg)': 50}
            output = load_graph('data.csv', categories_increments)
            main_graph, nutritional_info = output
            print(nutritional_info)
            self.first_click = False

        assert main_graph is not None and nutritional_info is not None

        self.selected_item = self.parent.meal_picker.return_similar_meals()
        _, food_name, _, _ = self.selected_item.split(" | ")
        print(self.selected_item)
        self.selected_item = food_name
        print(food_name)

        slider_entries, _ = self.return_slider_entries()
        slider_entries = parse_tkinter_slider_entries(slider_entries)
        print(slider_entries)  # WORKS!!!

        selected_food = main_graph.vertices[food_name]
        recommended_meals = main_graph.recommend_meal(food=selected_food,
                                                      limit=10,
                                                      weighting=slider_entries)
        print(recommended_meals)
        food_messages = []
        for food in recommended_meals:
            food_messages.append(concatenate_meal_name(food, nutritional_info))

        # print(set(main_graph.vertices.keys()))
        # print(main_graph.get_all_vertices("food"))
        # print(main_graph.get_all_vertices("dessert"))
        # print(main_graph.get_all_vertices("drink"))

    def on_help(self):
        """
        Actions when 'Help' is pressed on the display console.
        """

        help_message = ("This is a long paragraph that contains multiple lines of text. It serves as an example \n to "
                        "demonstrate how to display a lengthy message in a Tkinter messagebox. You can include \n as "
                        "much text as you need in this paragraph. \n"
                        "- Note 1: Remember to include all relevant details. \n"
                        "- Note 2: Keep the message clear and concise. \n"
                        "- Note 3: Consider the readability of the text. \n"
                        "Feel free to customize this paragraph and add your own content. \n")

        messagebox.showinfo("Long Paragraph and Notes", help_message)

    def select_weightings(self):
        """
        TODO
        """

        self.sliders = {}
        self.slider_labels = {}
        self.slider_entries = {}

        nutrients = {'protein', 'total_carb', 'total_fat', 'calories', 'sugar'}

        rownum = 2
        colnum = 0
        for nutrient in nutrients:
            frame = tk.Frame(self)
            if rownum == 0:
                frame.grid(row=rownum, column=colnum, padx=10, pady=(50, 0))
            frame.grid(row=rownum, column=colnum, padx=10)
            rownum, colnum = rownum + 1, colnum

            nutrient_label = (nutrient.replace("_", " ")).upper()
            label = tk.Label(frame,
                             text=f"{nutrient_label}",
                             font=("Roboto", "16", "bold"),
                             width=15,
                             justify="center")
            label.grid(row=rownum, column=colnum)
            rownum, colnum = rownum + 1, colnum

            entry = tk.Entry(frame, width=9)
            entry.grid(row=rownum, column=colnum)
            entry.bind('<Return>', lambda event, nt=nutrient: self.on_entry_update(nt))

            slider = tk.Scale(frame, from_=0, to=10, orient='horizontal',
                              command=lambda value, nt=nutrient: self.update_entry_from_slider(nt))

            slider.grid(row=rownum - 1, column=colnum + 1, padx=50, pady=20)
            slider.bind('<B1-Motion>', lambda event, nt=nutrient: self.update_entry_from_slider(nt))
            rownum, colnum = rownum + 1, colnum

            self.sliders[nutrient] = slider
            self.slider_entries[nutrient] = entry

            self.sliders[nutrient] = slider
            self.slider_labels[nutrient] = label
            self.slider_entries[nutrient] = entry
        help_me = tk.Button(self, text="Click Me", command=self.on_help, height=2, width=10)
        help_me.grid(row=rownum, column=0, pady='50')

    def on_entry_update(self, nutrient):
        """
        Update the slider position based on the manual entry value.
        """
        try:
            value = int(self.slider_entries[nutrient].get())
            self.sliders[nutrient].set(value)
            # Checks if value is in range
            if not (0 <= value <= 10):
                raise ValueError
        except ValueError:
            self.slider_entries[nutrient].delete(0, tk.END)
            self.slider_entries[nutrient].insert(0, str(self.sliders[nutrient].get()))

    def update_entry_from_slider(self, nutrient):
        """
        Update the entry box value from the slider value.
        """
        value = self.sliders[nutrient].get()
        entry = self.slider_entries[nutrient]
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

    def return_slider_entries(self) -> tuple[dict[str, tk.Entry], dict[str, tk.Label]]:
        """
        Returns the entry that was entered for the weighting of nutrients.

        Returns in the order: slider_entries, slider_labels
        """
        return self.slider_entries, self.slider_labels


def concatenate_meal_name(food: WeightedVertex, nutritional_info: dict[str, dict[str, Any]]) -> str:
    """
    Returns the restaurant, food, calories, protein in the order.
    """
    current_food = nutritional_info[food.item]
    company_name, meal_name, calories, protein = current_food['Company'], current_food['Item'], \
        current_food['Calories'], current_food['Protein']

    return f'{company_name} | {meal_name} | Calories: {calories} | Protein: {protein}'


def parse_tkinter_slider_entries(widget_entries) -> dict[str, int]:
    """
    Parses tkinter.Entry objects into regular integers.
    """

    widget_dict = {}

    for key, entry_widget in widget_entries.items():
        potential_weight = entry_widget.get()
        if potential_weight == '':
            widget_dict[key] = 1
        else:
            try:
                widget_dict[key] = int(potential_weight)
            except ValueError:
                widget_dict[key] = 1  # Give a default weighting

    return widget_dict
