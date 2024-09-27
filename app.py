from flask import Flask, jsonify, request
import os
import csv

app = Flask(__name__)

# Fonction pour récupérer toutes les données des fichiers .don
def get_donnees(dossier_number):
    donnees = []
    racine = f'C:\\ProgramData\\Pomo\\dossiers.99\\{dossier_number}'
    
    # Parcourir les sous-dossiers
    for root, dirs, files in os.walk(racine):
        for file in files:
            # Vérifier si le fichier a l'extension '.don'
            if file.endswith('.don'):
                chemin_fichier = os.path.join(root, file)
                # Ouvrir et lire le fichier comme un fichier CSV
                with open(chemin_fichier, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=',')
                    donnees.extend(list(reader))
    return donnees

@app.route('/')
def hello_world():
    # Récupérer le numéro de dossier passé en paramètre
    dossier_number = request.args.get('dossier')
    if dossier_number:
        donnees = get_donnees(dossier_number)
        return jsonify({"data": donnees})
    else:
        return jsonify({"error": "Numéro de dossier manquant"}), 400

if __name__ == '__main__':
    app.run()
