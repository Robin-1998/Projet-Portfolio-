import os
from dotenv import load_dotenv
from datetime import timedelta

# Déterminer l'environnement courant
ENV = os.getenv("FLASK_ENV", "development")

# Charger le fichier .env correspondant à l'environnement
if ENV == "testing":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuration de base commune à tous les environnements."""

    # Clé secrète obligatoire
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("La variable d'environnement SECRET_KEY doit être définie !")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # UTF-8 pour JSON
    JSON_AS_ASCII = False

    # JWT
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


# Dictionnaire de configuration global pour Flask
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
