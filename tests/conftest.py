"""
Fixtures pytest pour l'application Flask avec base PostgreSQL/PostGIS.
"""

import os
import pytest
from app import create_app, db
from sqlalchemy import text, event
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URI = os.getenv("DATABASE_URL")


@pytest.fixture(scope="session")
def app():
    """Créer l'application Flask configurée pour les tests."""
    app = create_app("testing")

    # Configuration pour éviter les problèmes de session
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'poolclass': StaticPool,
    }

    with app.app_context():
        # Créer l'extension PostGIS
        try:
            db.session.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
            db.session.commit()
        except Exception as e:
            print(f"Avertissement : PostGIS extension : {e}")
            db.session.rollback()

        # Créer toutes les tables
        db.create_all()
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    """Créer un client Flask avec support de la BD."""

    with app.app_context():
        # Supprimer les données avant chaque test
        db.drop_all()
        db.create_all()
        db.session.commit()

        # Créer le client
        test_client = app.test_client()

        yield test_client


@pytest.fixture
def app_with_context(app):
    """Fournir l'app avec son contexte actif."""
    with app.app_context():
        yield app


@pytest.fixture
def db_session(app):
    """Fournir une session DB pour les tests directs."""
    with app.app_context():
        yield db


@pytest.fixture
def runner(app):
    """Fixture pour tester les commandes Flask CLI."""
    return app.test_cli_runner()
