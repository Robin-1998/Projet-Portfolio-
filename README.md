# Projet-Portfolio-
Ce projet a pour objectif de mettre en pratique l’ensemble des compétences acquises tout au long de la formation des fondamentaux à travers le développement d’un concept personnel. L'école de formation est Holberton school Laval dans les fondamentaux du dev en full stack

Wiki Interactif - Univers du Seigneur des Anneaux
Ce projet est un site web immersif inspiré de l'univers du Seigneur des Anneaux, combinant une carte interactive, une encyclopédie enrichie de données (personnages, lieux, races) et un espace communautaire pour partager des créations artistiques. Il intègre une authentification sécurisée, une API REST, une base de données relationnelle, ainsi qu'une interface moderne construite avec React.

# Fonctionalité

- Carte interactive -> Navigation entre les régions/villes avec affichage des points d'intérêt via marqueur (gestion POSTGIS)
- Authentification -> Inscription, connexion (gestion par JWT)
- Wiki SDA -> Consultation des races, histoires, personnages
- Galerie artistique -> Ajout de créations artistiques en images liées à l’univers SDA
- Backend RESTful API -> Flask, avec endpoints organisés par version
- Frontend React -> SPA avec Vite, composants modulaires

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
│   │       ├── api_characters.py            # Endpoints pour les personnages
│   │       ├── api_histories.py             # Endpoints pour les événements
│   │       ├── api_image_post.py            # Endpoints pour l'envoie d'image par un utilisateur connecté
│   │       └── api_map_data.py              # Endpoints pour les marqueurs et un lieu
│   │       ├── api_races.py                 # Endpoints pour les races (univers/lore)
│   │       └── api_reviews.py               # Endpoints pour les commentaires sur le post d'une image
│   │       ├── api_search.py                # Endpoints pour la gestion d'une barre de recherche
│   │       ├── api_users.py                 # Endpoints pour la gestion des utilisateurs
│   │
│   ├── database/                        # Gestion de la base de données
│   │   ├── schema.sql                       # Script SQL pour création initiale des tables
│   │   └── data.sql                         # Scripts SQL pour toute les inserctions de tables
│   │
│   ├── models/                          # Définitions des modèles ORM
│   │   ├── __init__.py                      # Rend 'models' importable comme package
│   │   ├── basemodel.py                     # Classe mère (id, created_at, updated_at)
│   │   ├── character.py                     # Modèle character (Personnage)
│   │   ├── history.py                       # Modèle history (événements de l'univers)
│   │   ├── image_post.py                    # Modèle Image_post (envoie d'une image)
│   │   ├── map_marker.py                    # Modèle Map_marker (marqueur/point d'un lieu sur la carte interactive)
│   │   ├── map_region.py                    # Modèle Map_region (polygone d'une région sur la carte interactive)
│   │   ├── place_map.py                     # Modèle PlaceMap (lieux/cartes)
│   │   ├── race.py                          # Modèle Race (races de l’univers)
│   │   ├── review.py                        # Modèle Review (Commentaire sur une image)
│   │   └── user.py                          # Modèle User (utilisateurs)
│   │
│   ├── persistence/                     # Accès et gestion de la base de donnée CRUD
│   │   ├── __init__.py                      # Rend 'persistence' importable comme package
│   │   ├── image_post_repository            # Classe qui gère les opérations CRUD pour l'entité ImagePost
│   │   ├── repository                       # Repository générique pour les implémentation CRUD
│   │   ├── review_repository                # Classe qui gère les opérations CRUD pour l'entité review
│   │   ├── user_repository                  # Classe qui gère les opérations CRUD pour l'entité user
│   │
│   ├── services/                        # Couche métier (logique de l’app)
│   │   ├── __init__.py                      # Rend 'services' importable comme package
│   │   ├── facade.py                        # Façade : point d’entrée centralisé vers les modèles lié à un utilisateur
│   │   ├── facade2.py                       # Façade : point d’entrée centralisé vers les modèles non lié à un utilisateur
│   │
├── frontend/                        # Dossier principal de l’application frontend
│   ├── src/                            # Code source de l'application React (composants, routes, styles, etc.).
│   │   ├── assets/                       # Contient les fichiers statiques utilisés par l'application (images, icônes, styles, etc.).
│   │       ├── fonts                     # Pour les polices importés
│   │   ├── components/                   # Composant de fonction React
│   │   ├── pages/                        # Fichiers React pour chaque page utilisé
│   │   ├── services/                     # 
│   │   ├── styles/                       # Répertoire regroupant les fichiers de styles utilisés dans l'application.
│   │   ├── app.jsx                       # Composant racine de l'application React.
│   │   ├── main.jsx                      # Point d'entrée de l'application React, qui monte le composant App dans le DOM.
│   ├── eslint.config.js/                              #
│   ├── index.html                        # Fichier HTML principal dans lequel l’application React est injectée.
│   │
├── tests/                               # Dossier principal des tests
│   ├── unit/                            # Tests unitaires
│   │   ├── __init__.py                  # Rend 'unit' importable comme package
│   │   ├── test_api.py                  # Test des API
│   │   ├── test_facade1.py              # Test de la première facade
│   │   ├── test_facade2.py              # Test de la deuixème facade
│   │   ├── test_model_statique.py       # Test des modèles non liés à l'utilisateur
│   │   ├── test_model_dynamique.py      # Test des modèles liés à l'utilisateur
│   │   └── test_routes.py               # tests supplémentaire des routes API
│   │
│   ├── postman/                         # Collection Postman
│       └── script_postman.json          # Script postman pour tout les tests (requêtes) des différents routes
│   │
│   ├── __init__.py                      # Rend 'unit' importable comme package
│   └── conftest.py                      # Centralise la configuration et les fixtures pour les tests pytest.
│   │
├── Documentation/                       # Documentation technique pour le projet
│
├── __init__.py                          # Rend la racine importable comme package Python
├── config.py                            # Définit les paramètres de configuration selon l'environnement (développement, production, test).
├── journal_de_bord.md                   # Journal quotidien par jour des taches effectués et problème rencontré
└── README.md                            # Documentation principale du projet
├── requirements.txt                     # Dépendances Python (Flask, SQLAlchemy, JWT…)
├── run-tests.py                         # Script pour exécuter la suite de tests
├── run.py                               # Script principal pour démarrer Flask
```
# Collaborateurs
Ce projet a été conçu et développé par Thérèse-Marie LEFOULON et Robin DAVID. 
