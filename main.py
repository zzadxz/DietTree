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
        self.title('DietTree Project')
        self.geometry(f'{screen_width}x{screen_height}')

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
