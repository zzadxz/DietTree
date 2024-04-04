"""Main module for the Meal Picker application."""
import tkinter as tk
import csv
from meal_picker import MealPicker
from welcome_page import WelcomePage
from side_panel import SidePanel


def load_meal_data(filepath: str) -> list[dict[str, str]]:
    """Load meal data from a CSV file.
    """
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


class MainApplication(tk.Tk):
    """
    Main application window.
    """
    welcome_page: WelcomePage
    side_panel: SidePanel
    meal_picker: MealPicker

    def __init__(self) -> None:
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        database = load_meal_data('data.csv')
        self.title('Main Application')
        self.geometry(f'{screen_width}x{screen_height}')

        # self.background_image = tk.PhotoImage(file='fancy_tree.png')
        # self.background_label = tk.Label(self, image=self.background_image)
        # self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.welcome_page = WelcomePage(self)
        self.welcome_page.pack(side='right', fill='both', expand=True)

        self.side_panel = SidePanel(self)
        self.side_panel.pack(side='left', fill='y')

        self.meal_picker = MealPicker(self, database, self.side_panel)
        self.meal_picker.pack(side='left', fill='y')


def main() -> None:
    """Main function to run the application.
    """
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'allowed-io': ['load_meal_data'],
        'extra-imports': ['csv', 'networkx', 'pandas', 'tkinter', 'meal_picker', 'welcome_page', 'side_panel'],
        'max-nested-blocks': 4,
    })
    main()
