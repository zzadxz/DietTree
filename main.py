import tkinter
import customtkinter

# systme settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("CSC111 Project")

if __name__ == '__main__':
    app.mainloop()  # start the app
