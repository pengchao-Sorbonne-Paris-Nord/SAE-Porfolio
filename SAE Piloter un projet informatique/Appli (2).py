import tkinter as tk
from tkinter import messagebox
import requests
import mysql.connector
import io
from PIL import Image, ImageTk


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
        
        self.weather_icon_label = tk.Label(self)
        self.weather_icon_label.pack()


    def meteo_courante(self):
        city_name = self.texte.get()
        api_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
        api_key = "becb330149e04c7cb55194813230512"  # Remplacez par votre clé API
        params = {
            "key": api_key,
            "q": city_name,
            "format": "json",
            "num_of_days": "1",
            "date": "today",
            "fx": "yes",
            "cc": "yes",
            "mca": "yes",
            "fx24": "yes",
            "includelocation": "yes",
            "show_comments": "no",
            "tp": "3",
            "showlocaltime": "yes",
            "lang": "Fr",
            "alerts": "yes",
            "aqi": "yes"
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            current_condition = data['data']['current_condition'][0]
            self.temp.config(text=current_condition['temp_C'] + " °C")
            self.hum.config(text=current_condition['humidity'] + " %")
            self.sky.config(text=current_condition['weatherDesc'][0]['value'])
            self.ipa.config(text=self.calculate_ipa(current_condition['air_quality']))

            # Récupérer l'URL de l'icône météo et la mettre à jour sur l'interface
            weather_icon_url = self.get_weather_icon_url(current_condition)
            if weather_icon_url:
                self.update_weather_icon(weather_icon_url)
        else:
            print("Erreur lors de la connexion à l'API")
        self.insert_weather_data(city_name, current_condition['temp_C'], current_condition['humidity'], current_condition['weatherDesc'][0]['value'], "IQA Calculé")
        self.insert_ville_data(city_name)


    def get_weather_icon_url(self, current_condition):
        icon_data_list = current_condition.get('weatherIconUrl', [])
        if icon_data_list and 'value' in icon_data_list[0]:
            return icon_data_list[0]['value']
        return None



    def calculate_ipa(self, air_quality):
        # Calcul de l'indice de qualité de l'air (IQA) - à adapter selon votre besoin
        return "IQA Calculé"
        
    def update_weather_icon(self, icon_url):
        try:
            response = requests.get(icon_url)
            response.raise_for_status()
            icon_data = io.BytesIO(response.content)
            icon_image = Image.open(icon_data)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.weather_icon_label.config(image=icon_photo)
            self.weather_icon_label.image = icon_photo  # Gardez une référence!
        except requests.exceptions.RequestException as e:
            print(f"Erreur de téléchargement de l'icône météo : {e}")

    def meteo_precedente(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                database="meteo",
                user="root",
                password="root"  # Remplacez par votre mot de passe réel
            )
            cursor = conn.cursor()
            # Récupère les dernières données météo enregistrées
            query = "SELECT temp_C, humidity, weatherDesc, weatheriqa FROM weather ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                self.temp.config(text=result[0] + " °C")
                self.hum.config(text=result[1] + " %")
                self.sky.config(text=result[2])
                self.ipa.config(text=result[3])
                if result and len(result) > 4:
                    self.update_weather_icon(result[4])
            else:
                print("Données météorologiques précédentes non trouvées ou incomplètes")

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("Erreur lors de la connexion à la base de données : ", e)

    def insert_weather_data(self, city, temp, humidity, weather_desc, weather_iqa):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                database="meteo",
                user="root",
                password="root"  # Remplacez par votre mot de passe réel
            )
            cursor = conn.cursor()

            # Prépare la requête SQL d'insertion, sans inclure la colonne pour l'URL de l'icône
            query = "INSERT INTO weather (temp_C, humidity, weatherDesc, weatheriqa) VALUES (%s, %s, %s, %s)"
            values = (temp, humidity, weather_desc, weather_iqa)

            # Exécute la requête
            cursor.execute(query, values)
            conn.commit()

            print("Données météorologiques enregistrées dans la base de données pour la ville:", city)

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("Erreur lors de la connexion à la base de données : ", e)


            
    def meteo_demain(self):
        city_name = self.texte.get()
        api_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
        api_key = "becb330149e04c7cb55194813230512"  # Remplacez par votre clé API
        params = {
            "key": api_key,
            "q": city_name,
            "format": "json",
            "num_of_days": "1",
            "date": "tomorrow",  # Date spécifiée pour demain
            "fx": "yes",
            "cc": "yes",
            "mca": "yes",
            "fx24": "yes",
            "includelocation": "yes",
            "show_comments": "no",
            "tp": "3",
            "showlocaltime": "yes",
            "lang": "Fr",
            "alerts": "yes",
            "aqi": "yes"
        }

        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            forecast = data['data']['weather'][0]  # Prévisions pour demain
            avg_temp = forecast['avgtempC']
            max_temp = forecast['maxtempC']
            min_temp = forecast['mintempC']
            weather_desc = forecast['hourly'][0]['weatherDesc'][0]['value']
            current_condition = data['data']['current_condition'][0]

            

            # Mise à jour de l'interface graphique avec les prévisions
            self.temp.config(text=f"Temp Moy: {avg_temp} °C, Max: {max_temp} °C, Min: {min_temp} °C")
            self.sky.config(text=weather_desc)
            # Humidité et IPA peuvent être omis ou calculés différemment car ils ne sont pas directement disponibles pour les prévisions

        else:
            print("Erreur lors de la connexion à l'API")
        self.insert_ville_data(city_name)
        self.insert_weather_data(city_name, current_condition['temp_C'], current_condition['humidity'], current_condition['weatherDesc'][0]['value'], "IQA Calculé")

                
    def insert_ville_data(self, city_name):
        try:
            conn = mysql.connector.connect(host="localhost", database="meteo", user="root", password="root")
            cursor = conn.cursor()
            query = "INSERT INTO ville (query) VALUES (%s)"
            values = (city_name,)  # Mettez une virgule après city_name pour créer un tuple
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("Erreur lors de l'insertion dans la table ville : ", e)




    # Vous pouvez ajouter d'autres méthodes pour la logique de votre application

if __name__ == "__main__":
    app = Appli()
    app.mainloop()