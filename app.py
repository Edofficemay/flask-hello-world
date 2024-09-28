import os
import pandas as pd
from flask import Flask, request, jsonify

# Initialiser l'application Flask
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

# Route pour télécharger un fichier et analyser les données
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Analyser le fichier téléchargé
    info_data = import_csv_info_column(file_path)

    if not info_data:
        return jsonify({"message": "Aucune donnée trouvée"}), 400

    return jsonify({"info": info_data})

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
