"""
Fixtures pytest pour l'application Flask avec base PostgreSQL/PostGIS.
"""

import os
import pytest
from app import create_app, db
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy import create_engine, text

# Récupérer l'URL de la base de test depuis la config
TEST_DATABASE_URI = os.getenv("DATABASE_URL")  # .env.test doit être chargé via config.py

# Créer l'engine SQLAlchemy pour la base de test
engine = create_engine(TEST_DATABASE_URI)


@pytest.fixture(scope="session")
def app():
    """Créer l'application Flask configurée pour les tests et initialiser la base."""

    # Créer la base de test si elle n'existe pas
    if not database_exists(TEST_DATABASE_URI):
        create_database(TEST_DATABASE_URI)

    # Créer l'app Flask en mode testing
    app = create_app("testing")  # utilisera TestingConfig et .env.test

    with app.app_context():
        # Supprimer les tables existantes (pas besoin de supprimer le schéma)
        db.drop_all()

        # Créer l'extension PostGIS si nécessaire
        db.session.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        db.session.commit()

        # Créer toutes les tables
        db.create_all()

        yield app  # <-- ici les tests vont s'exécuter

        # Nettoyer la DB après les tests
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Créer un client Flask pour simuler les requêtes HTTP."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture pour tester les commandes Flask CLI."""
    return app.test_cli_runner()
