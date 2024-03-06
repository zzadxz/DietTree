import tkinter as tk


class SidePanel(tk.Frame):
    """
    Side panel for the application.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setup_sliders()

    def setup_sliders(self):
        """
        Set up sliders for the side panel.
        """
        self.sliders = {}
        self.slider_labels = {}
        self.slider_entries = {}

        nutrients = {'Protein': 300, 'Carb': 500, 'Fat': 300, 'Calories': 5000, 'Sugar': 300}
        for nutrient in nutrients:
            frame = tk.Frame(self)
            frame.pack(padx=10, pady=10, fill='x')

            label = tk.Label(frame, text=f"{nutrient}:")
            label.pack(side='left')

            entry = tk.Entry(frame, width=5)
            entry.pack(side='left', padx=(0, 5))
            entry.bind('<Return>', lambda event, nt=nutrient: self.on_entry_update(nt))

            slider = tk.Scale(frame, from_=0, to=nutrients[nutrient], orient='horizontal',
                              command=lambda value, nt=nutrient: self.update_entry_from_slider(nt))
            slider.pack(side='left', fill='x', expand=True)
            slider.bind('<B1-Motion>', lambda event, nt=nutrient: self.update_entry_from_slider(nt))
            self.sliders[nutrient] = slider
            self.slider_entries[nutrient] = entry

            self.sliders[nutrient] = slider
            self.slider_labels[nutrient] = label
            self.slider_entries[nutrient] = entry

    def get_slider_values(self) -> dict:
        """
        Get AND return the current values of the sliders.
        """
        values = {}
        for nutrient, slider in self.sliders.items():
            entry_value = self.slider_entries[nutrient].get().strip()
            if entry_value:
                try:
                    values[nutrient.lower()] = int(entry_value)
                except ValueError:
                    values[nutrient.lower()] = slider.get()
            else:
                values[nutrient.lower()] = slider.get()
        return values

    def update_slider_value(self, nutrient, value):
        """
        Update the label with the current slider value.
        """
        label = self.slider_labels[nutrient]

        entry = self.slider_entries[nutrient]
        if entry.get().strip() == "":
            entry.delete(0, tk.END)
            entry.insert(0, str(value))

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
