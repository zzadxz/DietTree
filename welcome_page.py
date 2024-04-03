import tkinter as tk
from graph import WeightedGraph
from graph import load_weighted_review_graph
from meal_picker import MealPicker


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

    def on_continue(self):
        """
        Actions when 'Continue' is clicked
        """

        self.selected_item = self.parent.meal_picker.return_similar_meals()
        print(self.selected_item)
        _, food_name, _, _ = self.selected_item.split(" - ")
        self.selected_item = food_name
        print(food_name)



        # main_graph = load_weighted_review_graph(food_file="database.csv",
        #                                         categories={'protein': 1, 'total_carb': 1, 'total_fat': 1,
        #                                                     'calories': 1, 'sugar': 1},
        #                                         weights={})

        # MealPicker.return_similar_meals()
        # main_graph.get_similarity_score()

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

    def on_entry_update(self, nutrient):
        """
        Update the slider position based on the manual entry value.
        """
        try:
            value = int(self.slider_entries[nutrient].get())
            self.sliders[nutrient].set(value)
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
