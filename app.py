from flask import Flask, jsonify, request
import os
import pandas as pd

app = Flask(__name__)

# Fonction pour parcourir les sous-dossiers de manière récursive avec os.listdir()
def parcourir_dossier(racine):
    donnees = []

    # Lister les éléments du répertoire racine
    for item in os.listdir(racine):
        chemin_complet = os.path.join(racine, item)

        # Si c'est un sous-dossier, on appelle récursivement la fonction
        if os.path.isdir(chemin_complet):
            donnees.extend(parcourir_dossier(chemin_complet))

        # Si c'est un fichier .don, on le traite comme un fichier CSV
        elif os.path.isfile(chemin_complet) and item.endswith('.don'):
            try:
                # Lire le fichier avec pandas, en ajustant le séparateur et l'encodage
                if os.path.getsize(chemin_complet) > 0:  # Vérifie si le fichier n'est pas vide
                    df = pd.read_csv(chemin_complet, skiprows=0, sep=';', encoding='latin1')
                    # Convertir le DataFrame en liste de listes et l'ajouter à donnees
                    donnees.extend(df.values.tolist())
                else:
                    print(f"Le fichier {chemin_complet} est vide.")
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {chemin_complet}: {e}")

    return donnees

# Route principale de l'API
@app.route('/')
def hello_world():
    # Récupérer le numéro de dossier passé en paramètre
    dossier_number = request.args.get('dossier')
    if dossier_number:
        racine = f'C:\\ProgramData\\Pomo\\dossiers.99\\{dossier_number}'
        # Récupérer les données du dossier spécifié
        donnees = parcourir_dossier(racine)
        return jsonify({"data": donnees})
    else:
        return jsonify({"error": "Numéro de dossier manquant"}), 400

if __name__ == '__main__':
    app.run()
