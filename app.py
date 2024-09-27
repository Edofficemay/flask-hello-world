from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def Datas():

    # Spécifiez le chemin du fichier CSV
    file_path = r'C:\Users\Florian\Desktop\tEST Python\Don 383\530300383_201910_ECO.don'
    
    # Lire le fichier CSV avec pandas
    data = pd.read_csv(file_path, delimiter=';')  # Changez le délimiteur si nécessaire
    
    return '{"data": "Hello, World!"}'

