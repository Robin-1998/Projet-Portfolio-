import os
from dotenv import load_dotenv
from datetime import timedelta

# Déterminer l'environnement courant (development, testing, production)
ENV = os.getenv("FLASK_ENV", "development")

# Charger le bon fichier .env
if ENV == "testing":
    load_dotenv(".env.test") # variables spécifiques aux tests
else:
    load_dotenv(".env")      # variables standard pour dev ou prod

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

    # Pagination (optionnelle)
    # ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Configuration pour le développement local."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ECHO = True  # afficher les requêtes SQL pour le debug


class TestingConfig(Config):
    """Configuration utilisée pendant les tests pytest."""

    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL", "postgresql://postgres:test@localhost:5432/database_test"
    )

    if "test" not in SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "⚠️ Vous tentez de lancer les tests sur une base non dédiée aux tests !"
        )


class ProductionConfig(Config):
    """Configuration pour la production (déploiement)."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


# Dictionnaire global pour Flask
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
