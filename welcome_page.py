import tkinter as tk


class WelcomePage(tk.Frame):
    """
    Welcome page for the application.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.welcome_label = tk.Label(self, text="Welcome to AltMeal!", font=("Roboto", 24))
        self.welcome_label.pack(pady=20)

        self.continue_button = tk.Button(self, text="Find closest meal", command=self.on_continue, font=("Roboto", 16))
        self.continue_button.pack(pady=20)

    def on_continue(self):
        """
        Actions when 'Continue' is clicked
        """
        print("Continue button clicked")
