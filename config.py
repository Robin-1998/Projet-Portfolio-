import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Répertoire de base du projet
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuration de base commune à tous les environnements."""

    # Clé secrète Flask (nécessaire pour sessions et JWT)
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("La variable d'environnement SECRET_KEY doit être définie !")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # UTF-8 pour JSON (évite les caractères bizarres)
    JSON_AS_ASCII = False

    # JWT (durée de validité du token)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)

class DevelopmentConfig(Config):
    """Configuration pour le développement local."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ECHO = True  # afficher les requêtes SQL pour le debug


class ProductionConfig(Config):
    """Configuration pour la production (déploiement)."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


# Dictionnaire de configuration global pour Flask
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
