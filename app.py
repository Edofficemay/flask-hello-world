from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def Datas():
    # Spécifiez le chemin du fichier CSV
    file_path = 'C:/Users/Florian/Desktop/tEST Python/Don 383/530300383_201910_ECO.don'
   
    # Lire le fichier CSV avec pandas
    try:
        data = pd.read_csv(file_path, delimiter=';')  # Changez le délimiteur si nécessaire

        # Convertir les données en JSON
        data_json = data.to_dict(orient='records')

        # Retourner les données sous forme de JSON
        return jsonify({"data": data_json})

    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
