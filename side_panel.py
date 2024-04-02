"""We use Tkinter for the UI of our application. Tkinter is a Python library that is used to develop GUI applications.
It provides a powerful object-oriented interface and is easy to use.
It is a standard Python interface to the Tk GUI toolkit.
"""

import tkinter as tk
from typing import Optional


class SidePanel(tk.Frame):
    """
    Side panel for the application.
    """
    parent: Optional[tk.Frame]
    sliders: dict[str, tk.Scale]
    slider_labels: dict[str, tk.Label]
    slider_entries: dict[str, tk.Entry]

    def __init__(self, parent: Optional[tk.Frame], *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setup_sliders()

    def setup_sliders(self) -> None:
        """
        Set up sliders for the side panel.
        """
        self.sliders = {}
        self.slider_labels = {}
        self.slider_entries = {}

        nutrients = {'protein': 300, 'total_carb': 500, 'total_fat': 300, 'calories': 5000, 'sugar': 300}
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

    def update_slider_value(self, nutrient: str, value: int) -> None:
        """
        Update the label with the current slider value.
        """
        # label = self.slider_labels[nutrient]

        entry = self.slider_entries[nutrient]
        if entry.get().strip() == "":
            entry.delete(0, tk.END)
            entry.insert(0, str(value))

    def on_entry_update(self, nutrient: str) -> None:
        """
        Update the slider position based on the manual entry value.
        """
        try:
            value = int(self.slider_entries[nutrient].get())
            self.sliders[nutrient].set(value)
        except ValueError:
            self.slider_entries[nutrient].delete(0, tk.END)
            self.slider_entries[nutrient].insert(0, str(self.sliders[nutrient].get()))

    def update_entry_from_slider(self, nutrient: str) -> None:
        """
        Update the entry box value from the slider value.
        """
        value = self.sliders[nutrient].get()
        entry = self.slider_entries[nutrient]
        entry.delete(0, tk.END)
        entry.insert(0, str(value))


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'networkx', 'pandas'],
        'max-nested-blocks': 4,
    })
