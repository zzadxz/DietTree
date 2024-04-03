import tkinter as tk
import csv
from meal_picker import MealPicker
from welcome_page import WelcomePage
from side_panel import SidePanel


def load_meal_data(filepath):
    """
    Load meal data from a CSV file.
    """
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


database = load_meal_data('database.csv')


class MainApplication(tk.Tk):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title('Main Application')
        self.geometry(f'{screen_width}x{screen_height}')

        self.welcome_page = WelcomePage(self)
        self.welcome_page.pack(side='right', fill='both', expand=True)

        self.side_panel = SidePanel(self)
        self.side_panel.pack(side='left', fill='y')

        self.meal_picker = MealPicker(self, database, self.side_panel)
        self.meal_picker.pack(side='left', fill='y')


def main():
    """
    Main function to run the application.
    """
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()
