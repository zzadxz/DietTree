"""YOUR DOCSTRING HERE"""

import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional
from graph import load_graph
from vertex import WeightedVertex


class WelcomePage(tk.Frame):
    """Welcome page for the application.

    Instance Attributes:
    - parent: The parent object or container.
    - welcome_label: The label widget displaying a message.
    - continue_button: The button widget for continuing.
    - selected_item: The currently selected item.
    - first_click: True if it's the first click.
    """

    parent: Any
    welcome_label: tk.Label
    continue_button: tk.Button
    selected_item: Optional[Any] = None
    first_click: bool = True
    main_graph: Optional[Any] = None
    nutritional_info: Optional[Any] = None
    in_click: bool = False
    sliders: dict[str, Any]
    slider_labels: dict[str, Any]
    slider_entries: dict[str, Any]

    def __init__(self, parent: Any, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.welcome_label = tk.Label(self, text="Welcome to AltMeal!", font=("Roboto", 28, "bold"))
        self.welcome_label.grid(row=0, column=0, pady=(50, 10), padx=50)

        self.continue_button = tk.Button(self,
                                         text="Find closest meal",
                                         command=self.on_continue,
                                         font=("Roboto", 18),
                                         width=25,
                                         height=2,
                                         activebackground='gray')
        self.continue_button.grid(row=1, column=0)
        self.select_weightings()
        self.selected_item = None
        self.first_click = True
        self.main_graph = None
        self.nutritional_info = None
        self.in_click = False

    def on_continue(self):
        """Actions when 'Continue' is clicked
        """
        if not self.in_click:
            self.in_click = True
            self.parent.meal_picker.not_searching = True

        if self.first_click:
            categories_increments = {'Calories': 100, 'Protein (g)': 10, 'Carbs (g)': 10, 'Sugars (g)': 5,
                                     'Total Fat (g)': 5}
            output = load_graph('data.csv', categories_increments)
            self.main_graph, self.nutritional_info = output
            self.first_click = False

        assert self.main_graph is not None and self.nutritional_info is not None

        self.selected_item = self.parent.meal_picker.return_similar_meals()
        _, food_name, _, _ = self.selected_item.split(" | ")
        _, self.selected_item = food_name.split(": ")

        slider_entries, _ = self.return_slider_entries()
        slider_entries = parse_tkinter_slider_entries(slider_entries)
        num_of_recs = slider_entries.pop('NUM RECS', None)
        if num_of_recs < 5:
            num_of_recs = 5

        selected_food = self.main_graph.get_vertex(self.selected_item)

        food_messages = []
        if selected_food is not None:
            recommended_meals = self.main_graph.recommend_meal(food=self.selected_item,
                                                               limit=num_of_recs,
                                                               weighting=slider_entries)
            for food in recommended_meals:
                food_messages.append(concatenate_meal_name(food, self.nutritional_info))

        if self.in_click:
            self.parent.meal_picker.results_listbox.delete(0, tk.END)
            if food_messages != []:
                for meal_name in food_messages:
                    self.parent.meal_picker.results_listbox.insert(tk.END, meal_name)
            else:
                self.parent.meal_picker.results_listbox.insert(tk.END, 'No available recommendations!')
            self.parent.meal_picker.search_button.config(text="Reset")

    def on_help(self) -> None:
        """
        Actions when 'Help' is pressed on the display console.
        """

        help_message = ("1. Find your base food item. \n"
                        "   a. Adjust sliders or type in the boxes on the left panel to set nutritional values, or\n"
                        "   b. Directly search for a meal by typing in the text box above the search button. \n"
                        "\n"
                        "2. Press \"Search\" and select a meal with either similar nutritional values or a similar \n"
                        "   name as the one you specified. \n"
                        "\n"
                        "3. (Optional) Adjust sliders or type in the boxes on the right panel to set the weights for "
                        "   each nutritional value. The higher the number, the more importance that value will hold.\n"
                        "\n"
                        "4. Press \"Find closest meal\" to get a list of meals that are similar! \n"
                        "\n"
                        "5. Adjust the \"NUM RECS slider\" to retreive a certain number of meal recommendations. \n"
                        "\n"
                        "6. The top of the returned list will be the meal that is the most similar to your selected "
                        "meal. The similarity decreases as you go down the list. \n"
                        "\n"
                        "\n"
                        "Reset Buttion: To reset values on the left panel to 0, press the \"Reset Sliders\" button.")

        messagebox.showinfo("Help Me!", help_message)

    def select_weightings(self) -> None:
        """
        Displays the sliders required for the user to input the weightings for each of the nutrition categories in
        their recomendations.

        If the user does not touch/input response in weightings, the default will be a weighting of 1 for each
        nutrient (that means each nutrient is weighted equally). The default number of recommendations is 5, unless
        user changes it.

        The help button displays a message on how to use the application when it is clicked.
        """

        self.sliders = {}
        self.slider_labels = {}
        self.slider_entries = {}

        nutrients = ['Protein (g)', 'Carbs (g)', 'Total Fat (g)', 'Calories', 'Sugars (g)']

        rownum = 2
        colnum = 0
        frame = tk.Frame(self)
        for nutrient in nutrients:
            if rownum == 0:
                frame.grid(row=rownum, column=colnum, padx=10, pady=(50, 0))
            frame.grid(row=rownum, column=colnum, padx=10)
            rownum = rownum + 1

            nutrient_label = (nutrient.replace("_", " ")).upper()
            label = tk.Label(frame,
                             text=f"{nutrient_label}",
                             font=("Roboto", "16", "bold"),
                             width=15,
                             justify="center")
            label.grid(row=rownum, column=colnum)
            rownum = rownum + 1

            entry = tk.Entry(frame, width=9)
            entry.grid(row=rownum, column=colnum)
            entry.bind('<Return>', lambda _, nt=nutrient: self.on_entry_update(nt))

            slider = tk.Scale(frame, from_=0, to=10, orient='horizontal',
                              command=lambda _, nt=nutrient: self.update_entry_from_slider(nt))

            slider.grid(row=rownum - 1, column=colnum + 1, padx=50, pady=15)
            slider.bind('<B1-Motion>', lambda _, nt=nutrient: self.update_entry_from_slider(nt))
            rownum = rownum + 1

            self.sliders[nutrient] = slider
            self.slider_entries[nutrient] = entry
            self.slider_labels[nutrient] = label

        num_rec_label = tk.Label(frame,
                                 text="NUM RECS",
                                 font=("Roboto", "16", "bold"),
                                 width=15,
                                 justify="center")
        num_rec_label.grid(row=rownum, column=colnum)
        rownum = rownum + 1

        num_rec_entry = tk.Entry(frame, width=9)
        num_rec_entry.grid(row=rownum, column=colnum)
        num_rec_entry.bind('<Return>', lambda _, nt='NUM RECS': self.on_entry_update(nt))

        num_rec_slider = tk.Scale(frame, from_=5, to=150, orient='horizontal',
                                  command=lambda _, nt='NUM RECS': self.update_entry_from_slider(nt))

        num_rec_slider.grid(row=rownum - 1, column=colnum + 1, padx=50, pady=15)
        num_rec_entry.bind('<B1-Motion>', lambda _, nt='NUMRECS': self.update_entry_from_slider(nt))

        help_me = tk.Button(self, text="Help me!", command=self.on_help, height=2, width=10, activebackground='gray')
        help_me.grid(row=rownum, column=0, pady='30')

        self.sliders['NUM RECS'] = num_rec_slider
        self.slider_entries['NUM RECS'] = num_rec_entry
        self.slider_labels['NUM RECS'] = num_rec_label


    def on_entry_update(self, nutrient):
        """Update the slider position based on the manual entry value.
        """
        try:
            value = int(self.slider_entries[nutrient].get())
            self.sliders[nutrient].set(value)
            # Checks if value is in range
            if not 0 <= value <= 10:
                raise ValueError
        except ValueError:
            self.slider_entries[nutrient].delete(0, tk.END)
            self.slider_entries[nutrient].insert(0, str(self.sliders[nutrient].get()))


    def update_entry_from_slider(self, nutrient):
        """Update the entry box value from the slider value.
        """
        value = self.sliders[nutrient].get()
        entry = self.slider_entries[nutrient]
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

    def return_slider_entries(self) -> tuple[dict[str, tk.Entry], dict[str, tk.Label]]:
        """Returns the entry that was entered for the weighting of nutrients.

        Returns in the order: slider_entries, slider_labels
        """
        return self.slider_entries, self.slider_labels


def concatenate_meal_name(food: WeightedVertex, nutritional_info: dict[str, dict[str, Any]]) -> str:
    """Returns the restaurant, food, calories, protein in the order.
    """
    current_food = nutritional_info[food.item]
    company_name, meal_name, calories, protein = current_food['Company'], current_food['Item'], \
        current_food['Calories'], current_food['Protein (g)']

    # print(f'{company_name} | {meal_name} | Calories: {calories} | Protein: {protein}')
    return f'{company_name} | {meal_name} | Calories: {calories} | Protein: {protein}'



def parse_tkinter_slider_entries(widget_entries) -> dict[str, int]:
    """Parses tkinter.Entry objects into regular integers.
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


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'networkx', 'pandas', "math", "tkinter", "graph", "vertex"],
        'max-nested-blocks': 4,
    })
