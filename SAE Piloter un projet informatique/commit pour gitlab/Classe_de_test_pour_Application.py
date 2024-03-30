import tkinter as tk
from tkinter import messagebox
import requests
import mysql.connector

class Appli(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Météo")
        self.geometry("400x400")

        self.create_widgets()

if __name__ == "__main__":
    app = Appli()
    app.mainloop()

