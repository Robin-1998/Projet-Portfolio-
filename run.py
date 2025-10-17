"""
Ce script est le point d’entrée de l’application Flask.
Il crée l’application via create_app() et la lance en mode debug si le
fichier est exécuté directement, suivant une architecture Flask modulaire.
"""
from backend.app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
