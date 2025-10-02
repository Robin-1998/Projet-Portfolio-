from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
import os

# Initialisation des extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name=None):
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)

    # Déterminer l'environnement
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    # Charger la configuration
    from config import config
    app.config.from_object(config[config_name])

    # Initialiser les extensions avec l'app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importer les namespaces APRÈS l'initialisation des extensions
    from app.api.V1.api_users import api as users_ns
    from app.api.V1.api_auth import api as auth_ns
    from app.api.V1.api_admin import api as admin_ns

    # Initialiser Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Ajouter les namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
