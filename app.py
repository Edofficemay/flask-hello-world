from flask import Flask, jsonify
import os
import csv

app = Flask(__name__)

# Chemin du répertoire racine
racine = r'C:\ProgramData\Pomo\dossiers.99\530302446'

# Fonction pour récupérer toutes les données des fichiers .don
def get_donnees():
    donnees = []
    # Parcourir les sous-dossiers
    for root, dirs, files in os.walk(racine):
        for file in files:
            # Vérifier si le fichier a l'extension '.don'
            if file.endswith('.don'):
                chemin_fichier = os.path.join(root, file)
                # Ouvrir et lire le fichier comme un fichier CSV
                with open(chemin_fichier, 'r', newline='', encoding='utf-8') as f:
                    # Ajuster le délimiteur si nécessaire
                    reader = csv.reader(f, delimiter=',')
                    # Ajouter les données du fichier au tableau
                    donnees.extend(list(reader))
    return donnees

@app.route('/')
def hello_world():
    # Récupérer les données
    donnees = get_donnees()
    # Retourner les données sous forme de JSON
    return jsonify({"data": donnees})

if __name__ == '__main__':
    app.run()
