"""
Ce script est le point d’entrée de l’application Flask.
Il crée l’application via create_app() et la lance en mode debug si le
fichier est exécuté directement, suivant une architecture Flask modulaire.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
