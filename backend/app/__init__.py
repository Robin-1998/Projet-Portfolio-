import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from dotenv import load_dotenv  # 👈 pour charger les fichiers .env
from config import config
from flask_cors import CORS

# Permet d'importer depuis la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Initialisation des extensions Flask
db = SQLAlchemy()   # ORM SQLAlchemy
bcrypt = Bcrypt()   # Pour le hashage des mots de passe
jwt = JWTManager()  # Pour gérer les JWT

def create_app(config_name=None):
    """ Crée et configure l'application Flask selon l'environnement. """
    # Déterminer l'environnement (development, testing, production)
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Charger le bon fichier .env
    # ---------------------------------
    if config_name == "testing":
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env.test")
    else:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

    load_dotenv(env_path)
    # ---------------------------------

    # Création l'application Flask
    app = Flask(__name__)
    app.url_map.strict_slashes = False # Flask accepte les deux versions d’une URL, avec ou sans slash sur les routes

    # Configuration du CORS pour autoriser le front local
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    ## Charger la configuration depuis config.py
    app.config.from_object(config[config_name])

    # Initialisation des extensions avec l'app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importer les namespaces RESTX APRÈS init des extensions
    from backend.app.api.V1.api_users import api as users_ns
    from backend.app.api.V1.api_auth import api as auth_ns
    from backend.app.api.V1.api_admin import api as admin_ns
    from backend.app.api.V1.api_reviews import api as review_ns
    from backend.app.api.V1.api_races import api as races_ns
    from backend.app.api.V1.api_characters import api as characters_ns
    from backend.app.api.V1.api_histories import api as histories_ns
    from backend.app.api.V1.api_image_post import api as image_post_ns
    from backend.app.api.V1.api_search import api as search_ns
    from backend.app.api.V1.api_map_data import api as map_ns
    from backend.app.api.V1.api_description import api as description_ns
    from backend.app.models.relation_type import RelationType

    # Initialiser Flask-RESTX
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    # Ajouter tous les namespaces à l'API avec leur chemin
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(admin_ns, path="/api/v1/admin")
    api.add_namespace(races_ns, path="/api/v1/races")
    api.add_namespace(characters_ns, path="/api/v1/characters")
    api.add_namespace(histories_ns, path="/api/v1/histories")
    api.add_namespace(review_ns, path="/api/v1/reviews")
    api.add_namespace(search_ns, path="/api/v1/search")
    api.add_namespace(image_post_ns, path="/api/v1/images")
    api.add_namespace(map_ns, path="/api/v1/map")
    api.add_namespace(description_ns, path="/api/v1/descriptions")

    return app
