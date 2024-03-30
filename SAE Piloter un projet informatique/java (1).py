import mysql.connector

def create_database():
    try:
        # Connexion à MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

        # Création de la base de données "meteo"
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS meteo")
        print("Base de données 'meteo' créée avec succès.")

        # Création de la table "weather"
        cursor.execute("USE meteo")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather (
                id INT AUTO_INCREMENT PRIMARY KEY,
                temp_C VARCHAR(255),
                humidity VARCHAR(255),
                weatherDesc VARCHAR(255),
                weatherIconUrl VARCHAR(255),
                weatheriqa VARCHAR(255)
            )
            """
        )
        print("Table 'weather' créée avec succès.")

        # Création de la table "ville"
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ville (
                id INT AUTO_INCREMENT PRIMARY KEY,
                query VARCHAR(255)
            )
            """
        )
        print("Table 'ville' créée avec succès.")

    except mysql.connector.Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connexion à MySQL fermée.")

if __name__ == "__main__":
    create_database()
