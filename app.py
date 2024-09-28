import os
import pandas as pd
from flask import Flask, jsonify
from tkinter import Tk, filedialog

# Utiliser une boîte de dialogue pour sélectionner le dossier à analyser
root = Tk()
root.withdraw()  # Cacher la fenêtre principale
folder_path = filedialog.askdirectory(title="Sélectionner le dossier à analyser")

# Vérifier si un dossier a été sélectionné
if not folder_path:
    print("Aucun dossier sélectionné.")
    exit()

# Vérifier si le dossier existe
if not os.path.exists(folder_path):
    print(f"Erreur : Le dossier '{folder_path}' n'existe pas.")
    exit()

# Initialiser l'application Flask
app = Flask(__name__)

# Fonction pour importer uniquement la colonne 'Info' d'un fichier CSV
def import_csv_info_column(file_path, delimiter='='):
    try:
        # Lire le fichier CSV
        df = pd.read_csv(file_path, sep=delimiter, names=["Lib", "Info"], encoding='latin-1')

        # Suppression des lignes vides et des informations non pertinentes
        df.dropna(subset=['Info'], inplace=True)
        df = df[~df['Info'].isin(["0", "0.0", "0.00", "0.000"])]

        # Conversion de la colonne 'Info' en liste
        info_data = df['Info'].tolist()

        return info_data
    except FileNotFoundError:
        print(f"Erreur : le fichier '{file_path}' n'a pas été trouvé.")
    except pd.errors.EmptyDataError:
        print("Erreur : le fichier est vide.")
    except pd.errors.ParserError:
        print("Erreur : le fichier ne peut pas être analysé, vérifiez le délimiteur.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    return []

# Fonction pour collecter les données de la colonne 'Info' de tous les fichiers du dossier sélectionné
def collect_info_from_folder(folder_path):
    all_info_data = []
    for filename in os.listdir(folder_path):
        if (filename.endswith(".don") or filename.endswith(".don99")) and "ECO" in filename:
            file_path = os.path.join(folder_path, filename)

            # Vérifier si le fichier est bien un fichier (pas un sous-dossier)
            if os.path.isfile(file_path):
                # Importer les données du fichier CSV
                info_data = import_csv_info_column(file_path)

                if info_data:
                    all_info_data.append({
                        "filename": filename,
                        "info": info_data
                    })
    return all_info_data

# Collecter les données du dossier sélectionné
collected_info = collect_info_from_folder(folder_path)

# Définir une route pour afficher les données sur le localhost
@app.route('/')
def datas():
    if not collected_info:
        return jsonify({"message": "Aucune donnée trouvée dans le dossier sélectionné."})
    return jsonify({"collected_info": collected_info})

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
