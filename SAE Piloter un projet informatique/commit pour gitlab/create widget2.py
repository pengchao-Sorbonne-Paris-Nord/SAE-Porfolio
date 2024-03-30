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

    def create_widgets(self):
        # Cadre principal
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10)

        # Titre
        title_label = tk.Label(main_frame, text="Application Météo", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Cadre pour entrer le nom de la ville
        entry_frame = tk.Frame(main_frame)
        entry_frame.pack()

        ville_label = tk.Label(entry_frame, text="Ville:")
        ville_label.pack(side=tk.LEFT)

        self.texte = tk.Entry(entry_frame)
        self.texte.pack(side=tk.LEFT)

        # Boutons pour différentes actions
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        meteo_courante_btn = tk.Button(button_frame, text="Météo courante", command=self.meteo_courante)
        meteo_courante_btn.pack(side=tk.LEFT, padx=5)

        meteo_precedente_btn = tk.Button(button_frame, text="Météo précédente", command=self.meteo_precedente)
        meteo_precedente_btn.pack(side=tk.LEFT, padx=5)

        meteo_demain_btn = tk.Button(button_frame, text="Météo demain", command=self.meteo_demain)
        meteo_demain_btn.pack(side=tk.LEFT, padx=5)

        # Labels et champs pour afficher les résultats
        result_frame = tk.Frame(main_frame)
        result_frame.pack()

        self.temperature_label = tk.Label(result_frame, text="Température:", font=("Helvetica", 12))
        self.temperature_label.pack()

        self.temp = tk.Label(result_frame, text="")
        self.temp.pack()

        self.humidity_label = tk.Label(result_frame, text="Humidité:", font=("Helvetica", 12))
        self.humidity_label.pack()

        self.hum = tk.Label(result_frame, text="")
        self.hum.pack()

        self.sky_label = tk.Label(result_frame, text="Ciel:", font=("Helvetica", 12))
        self.sky_label.pack()

        self.sky = tk.Label(result_frame, text="")
        self.sky.pack()

        self.ipa_label = tk.Label(result_frame, text="IPA:", font=("Helvetica", 12))
        self.ipa_label.pack()

        self.ipa = tk.Label(result_frame, text="")
        self.ipa.pack()


if __name__ == "__main__":
    app = Appli()
    app.mainloop()