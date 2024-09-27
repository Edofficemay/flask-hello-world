from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def Datas():

    # Spécifiez le chemin du fichier CSV
    file_path = r'C:\Users\Florian\Desktop\tEST Python\Don 383\530300383_201910_ECO.don'
    
    # Lire le fichier CSV avec pandas
    try:
        df = pd.read_csv(file_path, delimiter=',')  # Changez le délimiteur si nécessaire

        # Convertir les données en JSON (chaque ligne devient un dictionnaire)
        data = df.to_dict(orient='records')

        # Retourner les données sous forme de JSON
        return jsonify({"data": data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return '{"data": "Hello, World!"}'

