"""We use Tkinter for the UI of our application. Tkinter is a Python library that is used to develop GUI applications.
It provides a powerful object-oriented interface and is easy to use.
It is a standard Python interface to the Tk GUI toolkit.
"""

import tkinter as tk
from typing import Optional


class SidePanel(tk.Frame):
    """Side panel for the application.

    Instance Attributes:
        - parent: The parent frame for the sliders
        - sliders: A mapping of nutrient names to their corresponding slider widgets.
        - slider_labels: A mapping of nutrient names to their corresponding label widgets.
        - slider_entries: A mapping of nutrient names to their corresponding entry widgets.
        - nutrients: A mapping of nutrients and their associated values.

    Representation Invariants:
        - self.sliders.keys() == self.slider_labels.keys() == self.slider_entries.keys() == self.nutrients.keys()
        - all(isinstance(nutrient, str) for nutrient in self.nutrients.keys())
        - all(isinstance(value, int) for value in self.nutrients.values())
        - all(isinstance(slider, tk.Scale) for slider in self.sliders.values())
        - all(isinstance(label, tk.Label) for label in self.slider_labels.values())
        - all(isinstance(entry, tk.Entry) for entry in self.slider_entries.values())

    """
    parent: Optional[tk.Frame]
    sliders: dict[str, tk.Scale]
    slider_labels: dict[str, tk.Label]
    slider_entries: dict[str, tk.Entry]
    nutrients: dict[str, int]
    reset_button: tk.Button

    def __init__(self, parent: Optional[tk.Frame], *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setup_sliders()

    def setup_sliders(self) -> None:
        """Set up sliders for the side panel.
        """
        self.sliders = {}
        self.slider_labels = {}
        self.slider_entries = {}

        self.nutrients = {'Protein (g)': 300, 'Carbs (g)': 500, 'Total Fat (g)': 300, 'Calories': 5000,
                          'Sugars (g)': 300}

        rownum = 0
        colnum = 0
        for nutrient in self.nutrients:
            frame = tk.Frame(self)
            if rownum == 0:
                frame.grid(row=rownum, column=colnum, padx=10, pady=(50, 0))
            frame.grid(row=rownum, column=colnum, padx=10)
            rownum = rownum + 1

            nutrient_label = (nutrient.replace("_", " ")).upper()
            label = tk.Label(frame, text=f"{nutrient_label}", font=("Roboto", "16", "bold"), width=15, justify="center")
            label.grid(row=rownum, column=colnum)
            rownum = rownum + 1

            entry = tk.Entry(frame, width=9)
            entry.grid(row=rownum, column=colnum)
            entry.bind('<Return>', lambda event, nt=nutrient: self.on_entry_update(nt))

            slider = tk.Scale(frame, from_=0, to=self.nutrients[nutrient], orient='horizontal',
                              command=lambda value, nt=nutrient: self.update_entry_from_slider(nt))

            slider.grid(row=rownum - 1, column=colnum + 1, padx=50, pady=20)
            slider.bind('<B1-Motion>', lambda event, nt=nutrient: self.update_entry_from_slider(nt))
            rownum = rownum + 1

            self.sliders[nutrient] = slider
            self.slider_entries[nutrient] = entry

            self.sliders[nutrient] = slider
            self.slider_labels[nutrient] = label
            self.slider_entries[nutrient] = entry

            self.reset_button = tk.Button(self, text="Reset Sliders", command=self.reset_sliders, width=10, height=2)
            self.reset_button.grid(row=len(self.nutrients) + 15, column=0, pady=40, padx=10, columnspan=2)

    def get_slider_values(self) -> dict:
        """Get AND return the current values of the sliders.
        """
        values = {}
        for nutrient, slider in self.sliders.items():
            entry_value = self.slider_entries[nutrient].get().strip()
            if entry_value:
                try:
                    values[nutrient] = int(entry_value)
                except ValueError:
                    values[nutrient] = slider.get()
            else:
                values[nutrient] = slider.get()
        return values

    def update_slider_value(self, nutrient: str, value: int) -> None:
        """Update the label with the current slider value.
        """

        entry = self.slider_entries[nutrient]
        if entry.get().strip() == "":
            entry.delete(0, tk.END)
            entry.insert(0, str(value))

    def on_entry_update(self, nutrient: str) -> None:
        """Update the slider position based on the manual entry value.
        """
        try:
            value = int(self.slider_entries[nutrient].get())
            self.sliders[nutrient].set(value)
            if not 0 <= value <= self.nutrients[nutrient]:
                raise ValueError
        except ValueError:
            self.slider_entries[nutrient].delete(0, tk.END)
            self.slider_entries[nutrient].insert(0, str(self.sliders[nutrient].get()))

    def update_entry_from_slider(self, nutrient: str) -> None:
        """Update the entry box value from the slider value.
        """
        value = self.sliders[nutrient].get()
        entry = self.slider_entries[nutrient]
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

    def reset_sliders(self) -> None:
        """Reset all sliders to their minimum value."""
        for slider in self.sliders.values():
            slider.set(0)
        for entry in self.slider_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, str(0))


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'networkx', 'pandas', 'typing', 'tkinter'],
        'max-nested-blocks': 4,
    })
