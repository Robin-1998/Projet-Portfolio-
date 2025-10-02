import os
from dotenv import load_dotenv
from datetime import timedelta

# Charger les variables d'environnement depuis .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration de base commune à tous les environnements"""

    # Clé secrète obligatoire
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("La variable d'environnement SECRET_KEY doit être définie !")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # UTF-8 pour JSON
    JSON_AS_ASCII = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)

    # ITEMS_PER_PAGE = 20, définir un nombre par défaut d’éléments à afficher par page

class DevelopmentConfig(Config):
    """Configuration pour le développement local."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = True  # afficher les requêtes SQL pour le debug

# Sélection de la configuration selon l'environnement
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
