# Projet-Portfolio-
Ce projet a pour objectif de mettre en pratique l’ensemble des compétences acquises tout au long de la formation des fondamentaux à travers le développement d’un concept personnel. L'école de formation est Holberton school Laval dans les fondamentaux du dev en full stack 

# Ordre de développement du projet :

1. Naissance du projet avec rédaction de la documentation (création du wireframe + choix des technologies + mind mapping + diagramme, etc...)
2. Création d'image par IA par un prompt en respectant les droits d'auteurs et récupération d'image personnel pour l'onglet des créations artistique
3. Création des tables en base de donnée
4. Création des polygones pour création de map interactive
5. Base model
6. API simple avec une route à la fois
7. Styliser la page web
8. Frontend simple pour afficher la carte avec utilisation des marqueurs.
9. Création de nouvelle fonctionalités une par une

## Architecture
```
Projet-Portfolio-/             # Racine du projet (fullstack Flask + React)
├── app/                             # Dossier principal de l’application backend + logique
│   ├── __init__.py                          # Rend 'app' importable comme package Python
│   ├── api/                           # Routes de l’API (contrôleurs Flask)
│   │   ├── __init__.py                      # Rend 'api' importable comme package
│   │   └── V1/                          # Version 1 de l’API (prépare l’évolution future V2…)
│   │       ├── __init__.py                  # Rend 'V1' importable comme package
│   │       ├── api_admin.py                 # Endpoints liés à l’administration
│   │       ├── api_auth.py                  # Endpoints d’authentification (login, JWT)
│   │       ├── api_users.py                 # Endpoints pour la gestion des utilisateurs
│   │       ├── api_places_map.py            # Endpoints pour les lieux/cartes (points sur la carte)
│   │       ├── api_events.py                # Endpoints pour les événements
│   │       ├── api_races.py                 # Endpoints pour les races (univers/lore)
│   │       ├── api_characters.py            # Endpoints pour les personnages
│   │       ├── api_art.py                   # Endpoints pour les créations artistiques
│   │       └── api_map_data.py              # Endpoints pour données cartographiques (coord. X,Y)
│   │
│   ├── database/                        # Gestion de la base de données
│   │   ├── schema.sql                       # Script SQL pour création initiale des tables
│   │   └── migrations                       # Scripts de migration (Alembic/Flask-Migrate)
│   │
│   ├── models/                          # Définitions des modèles ORM
│   │   ├── __init__.py                      # Rend 'models' importable comme package
│   │   ├── basemodel.py                     # Classe mère (id, created_at, updated_at)
│   │   ├── events.py                        # Modèle Event (événements)
│   │   ├── races.py                         # Modèle Race (races de l’univers)
│   │   ├── characters.py                    # Modèle Character (personnages)
│   │   ├── place_map.py                     # Modèle PlaceMap (lieux/cartes)
│   │   ├── spatial.py                       # Modèle Spatial (coordonnées/objets géographiques)
│   │   └── user.py                          # Modèle User (utilisateurs)
│   │
│   ├── services/                        # Couche métier (logique de l’app)
│   │   ├── __init__.py                      # Rend 'services' importable comme package
│   │   ├── spatial_service.py               # Service métier pour gestion des données spatiales
│   │   ├── facade.py                        # Façade : point d’entrée centralisé vers les modèles
│   │   └── map_service.py                   # Service métier pour manipulation des cartes
│   │
│   ├── bases_files/                     # Partie front-end (React + Vite)
│   │   ├── images/                          # Ressources visuelles (icônes, images…)
│   │   │   ├── icons                        # Dossier des icônes
│   │   │   └── images_page                  # Images utilisées dans les pages
│   │   │
│   │   ├── src/                         # Code source React (JSX + CSS)
│   │   │   ├── app.css                      # Style global de l’application React
│   │   │   ├── app.jsx                      # Composant racine React
│   │   │   ├── index.css                    # Styles additionnels
│   │   │   └── main.jsx                     # Point d’entrée React (montage de l’app)
│   │   │
│   │   ├── eslint.config.js             # Configuration ESLint (linter JS/React)
│   │   ├── index.html                   # Fichier HTML racine injectant l’app React
│   │   ├── package.json                 # Dépendances et scripts NPM pour le front-end
│   │   └── vite.config.js               # Configuration du bundler Vite (React)
│   │
├── tests/
│   ├── unit/                            # Tests unitaires
│   │   ├── test_user_model.py               # Test des méthodes User
│   │   ├── test_character_model.py          # Test des méthodes Character
│   │   └── etc...            
│   ├── integration/                     # Tests d’intégration (API + DB)
│   │   ├── test_users_api.py                # Vérifie /api/v1/users/*
│   │   ├── test_regions_api.py              # Vérifie /api/v1/regions/*
│   │   └── etc...
│   └── postman/                         # Collection Postman + scripts Newman
│       ├── PortfolioAPI.postman_collection.json
│       └── PortfolioAPI.postman_environment.json
│
├── Documentation/                       # Documentation technique pour le projet
│
├── __init__.py                          # Rend la racine importable comme package Python
├── run.py                               # Script principal pour démarrer Flask
├── requirements.txt                     # Dépendances Python (Flask, SQLAlchemy, JWT…)
├── run-tests.py                         # Script pour exécuter la suite de tests
└── README.md                            # Documentation principale du projet
```
# Collaborateurs
Ce projet a été conçu et développé par Thérèse-Marie LEFOULON et Robin DAVID. 
