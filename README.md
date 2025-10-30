# 🗺️ Wiki Interactif - Univers du Seigneur des Anneaux

[![Flask](https://img.shields.io/badge/Flask-2.3+-blue.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.0+-green.svg)](https://postgis.net/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Projet portfolio développé dans le cadre de la formation Holberton School Laval - Fondamentaux du développement Full Stack

Un site web immersif inspiré de l'univers du Seigneur des Anneaux, combinant une carte interactive, une encyclopédie enrichie et un espace communautaire pour partager des créations artistiques.

## 📋 Table des matières

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Tests](#-tests)
- [Processus de développement](#-processus-de-développement)
- [Contribution](#-contribution)
- [Licence](#-licence)
- [Contact](#-contact)

## 🎯 Aperçu

Ce projet met en pratique l'ensemble des compétences acquises en développement full stack à travers la création d'une application web complète dédiée à l'univers du Seigneur des Anneaux. Il offre une expérience utilisateur riche avec navigation géographique, consultation encyclopédique et partage communautaire.

### Objectifs pédagogiques

- Développement d'une API RESTful avec Flask
- Création d'une interface moderne avec React
- Gestion de données géographiques avec PostGIS
- Authentification sécurisée avec JWT
- Architecture en couches (MVC + Repository Pattern)
- Tests unitaires et d'intégration

## ✨ Fonctionnalités

### 🗺️ Carte Interactive
- Navigation fluide entre les régions et villes de la Terre du Milieu
- Affichage des points d'intérêt via marqueurs géolocalisés
- Gestion des données géospatiales avec PostGIS
- Polygones personnalisés pour chaque région

### 🔐 Authentification
- Inscription et connexion sécurisées
- Gestion de sessions avec JWT (JSON Web Tokens)
- Différenciation des rôles (utilisateur / administrateur)
- Protection des routes sensibles

### 📚 Encyclopédie (Wiki SDA)
- Consultation détaillée des races
- Chronologie des événements historiques
- Fiches personnages complètes

### 🎨 Galerie Artistique
- Upload de créations artistiques
- Support d'images (JPEG, PNG, WebP)
- Système de commentaires sur les publications
- Galerie communautaire

### 👤 Gestion des Utilisateurs
- Historique des publications
- Gestion des commentaires

## 🛠️ Technologies

### Backend
- **Flask** 2.3+ - Framework web Python
- **PostgreSQL** 14+ - Base de données relationnelle
- **PostGIS** 3.0+ - Extension géospatiale pour PostgreSQL
- **SQLAlchemy** - ORM Python
- **Flask-JWT-Extended** - Gestion JWT
- **Python** 3.10+

### Frontend
- **React** 18+ - Bibliothèque UI
- **Vite** - Build tool moderne
- **Leaflet** - Cartographie interactive
- **Axios** - Client HTTP
- **React Router** - Navigation SPA

### Outils de développement
- **pytest** - Framework de tests Python
- **Postman** - Tests API
- **ESLint** - Linter JavaScript

## 📁 Architecture

```
Projet-Portfolio-/
├── app/                              # Backend Flask
│   ├── __init__.py                   # Factory pattern Flask
│   ├── api/                          # Contrôleurs API
│   │   └── V1/                       # Version 1 de l'API
│   │       ├── api_admin.py          # Routes admin
│   │       ├── api_auth.py           # Authentification
│   │       ├── api_characters.py     # Personnages
│   │       ├── api_histories.py      # Événements historiques
│   │       ├── api_image_post.py     # Publications d'images
│   │       ├── api_map_data.py       # Données cartographiques
│   │       ├── api_races.py          # Races
│   │       ├── api_reviews.py        # Commentaires
│   │       ├── api_search.py         # Recherche globale
│   │       └── api_users.py          # Gestion utilisateurs
│   │
│   ├── models/                       # Modèles ORM
│   │   ├── basemodel.py              # Classe mère
│   │   ├── character.py              # Modèle Personnage
│   │   ├── history.py                # Modèle Événement
│   │   ├── image_post.py             # Modèle Publication
│   │   ├── map_marker.py             # Modèle Marqueur
│   │   ├── map_region.py             # Modèle Région
│   │   ├── place_map.py              # Modèle Lieu
│   │   ├── race.py                   # Modèle Race
│   │   ├── review.py                 # Modèle Commentaire
│   │   └── user.py                   # Modèle Utilisateur
│   │
│   ├── persistence/                  # Couche d'accès aux données
│   │   ├── repository.py             # Repository générique
│   │   ├── image_post_repository.py  # Repository images
│   │   ├── review_repository.py      # Repository commentaires
│   │   └── user_repository.py        # Repository utilisateurs
│   │
│   ├── services/                     # Logique métier
│   │   ├── facade.py                 # Façade utilisateur
│   │   └── facade2.py                # Façade entités statiques
│   │
│   └── database/                     # Scripts SQL
│       ├── schema.sql                # Définition des tables
│       └── data.sql                  # Données d'initialisation
│
├── frontend/                         # Application React
│   ├── src/
│   │   ├── components/               # Composants réutilisables
│   │   ├── pages/                    # Pages de l'application
│   │   ├── services/                 # Services API
│   │   ├── styles/                   # Styles CSS
│   │   ├── assets/                   # Ressources statiques
│   │   │   └── fonts/                # Polices personnalisées
│   │   ├── App.jsx                   # Composant racine
│   │   └── main.jsx                  # Point d'entrée
│   ├── index.html                    # Template HTML
│   └── vite.config.js                # Configuration Vite
│
├── tests/                            # Suite de tests
│   ├── unit/                         # Tests unitaires
│   │   ├── test_api.py               # Tests des routes API
│   │   ├── test_facade1.py           # Tests façade utilisateur
│   │   ├── test_facade2.py           # Tests façade statique
│   │   ├── test_model_statique.py    # Tests modèles statiques
│   │   └── test_model_dynamique.py   # Tests modèles dynamiques
│   ├── postman/
│   │   └── script_postman.json       # Collection Postman
│   └── conftest.py                   # Configuration pytest
│
├── Documentation/                    # Documentation technique
├── .env.test                         # Variables d'environnement de test
├── .gitignore                        # Fichiers ignorés par Git
├── .prettierrc                       # Configuration Prettier
├── requirements.txt                  # Dépendances Python
└── README.md                         # Ce fichier
```

## 🚀 Installation

### Prérequis

- Python 3.10 ou supérieur
- Node.js 18 ou supérieur
- PostgreSQL 14 ou supérieur avec PostGIS
- npm

### Étapes d'installation

#### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/Projet-Portfolio-.git
cd Projet-Portfolio-
```

#### 2. Configuration de la base de données

```bash
# Créer la base de données PostgreSQL
createdb nom_database

# Activer l'extension PostGIS
psql nom_database -c "CREATE EXTENSION postgis;"

# Importer le schéma
psql nom_database < app/database/schema.sql

# Importer les données initiales
psql nom_database < app/database/data.sql
```

#### 3. Installation Backend (Flask)

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

#### 4. Installation Frontend (React)

```bash
cd frontend
npm install
```

## ⚙️ Configuration

### Variables d'environnement Backend

Créer un fichier `.env` à la racine du projet :

```env
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete_tres_securisee
DATABASE_URL=postgresql://user:password@localhost/nom_database
JWT_SECRET_KEY=votre_jwt_secret_key
```

### Variables d'environnement Frontend

Créer un fichier `.env` dans le dossier `frontend/` :

```env
VITE_API_URL=http://localhost:5000/api/v1
```

## 💻 Utilisation

### Lancer l'application en mode développement

#### Terminal 1 - Backend Flask

```bash
# À la racine du projet
source venv/bin/activate  # Activer l'environnement virtuel
python run.py
```

Le serveur Flask démarre sur `http://localhost:5000`

#### Terminal 2 - Frontend React

```bash
cd frontend
npm run dev
```

Le serveur de développement Vite démarre sur `http://localhost:5173`

### Accéder à l'application

Ouvrir votre navigateur et accéder à : `http://localhost:5173`

## 📡 API Documentation

### Authentification

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| POST | `/api/v1/auth/register` | Créer un nouveau compte | Non |
| POST | `/api/v1/auth/login` | Se connecter | Non |
| GET | `/api/v1/auth/me` | Obtenir l'utilisateur actuel | Oui |

### Utilisateurs

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/users` | Liste tous les utilisateurs | Non |
| GET | `/api/v1/users/:id` | Détails d'un utilisateur | Non |
| PUT | `/api/v1/users/:id` | Modifier un utilisateur | Oui (propriétaire) |
| DELETE | `/api/v1/users/:id` | Supprimer un utilisateur | Oui (propriétaire) |

### Carte Interactive

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/map/regions` | Liste des régions | Non |
| GET | `/api/v1/map/markers` | Liste des marqueurs | Non |
| GET | `/api/v1/map/places/:id` | Détails d'un lieu | Non |

### Encyclopédie

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/races` | Liste des races | Non |
| GET | `/api/v1/races/:id` | Détails d'une race | Non |
| GET | `/api/v1/characters` | Liste des personnages | Non |
| GET | `/api/v1/characters/:id` | Détails d'un personnage | Non |
| GET | `/api/v1/histories` | Liste des événements | Non |
| GET | `/api/v1/histories/:id` | Détails d'un événement | Non |

### Galerie

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/images` | Liste des images | Non |
| GET | `/api/v1/images/:id` | Détails d'une image | Non |
| POST | `/api/v1/images` | Publier une image | Oui |
| PUT | `/api/v1/images/:id` | Modifier une image | Oui (propriétaire) |
| DELETE | `/api/v1/images/:id` | Supprimer une image | Oui (propriétaire) |

### Commentaires

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/reviews/image/:id` | Commentaires d'une image | Non |
| POST | `/api/v1/reviews` | Créer un commentaire | Oui |
| PUT | `/api/v1/reviews/:id` | Modifier un commentaire | Oui (propriétaire) |
| DELETE | `/api/v1/reviews/:id` | Supprimer un commentaire | Oui (propriétaire) |

### Recherche

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/search?q=terme` | Recherche globale | Non |

### Administration

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/api/v1/admin/users` | Liste tous les utilisateurs | Admin |
| DELETE | `/api/v1/admin/users/:id` | Supprimer un utilisateur | Admin |
| POST | `/api/v1/races` | Créer une race | Admin |
| POST | `/api/v1/characters` | Créer un personnage | Admin |
| POST | `/api/v1/histories` | Créer un événement | Admin |

### Format des requêtes

#### Exemple : Inscription

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "frodon",
  "email": "frodon@shire.com",
  "password": "oneRing123"
}
```

#### Exemple : Upload d'image

```bash
POST /api/v1/images
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "La Comté",
  "description": "Vue magnifique du village",
  "image_data": "<base64_encoded_image>",
  "image_mime_type": "image/jpeg"
}
```

## 🧪 Tests

### Tests Backend (Python)

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer tous les tests
pytest

# Lancer avec couverture
pytest --cov=app tests/

# Lancer un fichier de test spécifique
pytest tests/unit/test_api.py

# Lancer avec verbose
pytest -v
```

### Tests avec Postman

1. Importer la collection : `tests/postman/script_postman.json`
2. Configurer les variables d'environnement Postman
3. Exécuter la collection

### Structure des tests

- **test_model_statique.py** : Tests des modèles Race, Character, History
- **test_model_dynamique.py** : Tests des modèles User, ImagePost, Review
- **test_facade1.py** : Tests de la logique métier utilisateur
- **test_facade2.py** : Tests de la logique métier statique
- **test_api.py** : Tests d'intégration des routes API
- **test_routes.py** : Tests supplémentaires des endpoints

## 📝 Processus de développement

Le projet a suivi une méthodologie structurée en 9 étapes :

1. **Documentation initiale** : Wireframes, choix technologiques, mind mapping, diagrammes UML
2. **Création des assets** : Génération d'images par IA (respect des droits d'auteur)
3. **Modélisation base de données** : Définition des tables et relations
4. **Création des polygones** : Cartographie des régions avec PostGIS
5. **Modèles de base** : Implémentation des classes ORM
6. **API basique** : Développement route par route
7. **Stylisation** : Design et CSS de l'interface
8. **Frontend cartographique** : Intégration Leaflet et marqueurs
9. **Fonctionnalités avancées** : Ajout itératif des features

### Workflow Git

- `main` : Branche de production
- `develop` : Branche de développement
- `feature/*` : Branches de fonctionnalités
- `bugfix/*` : Branches de correction

### Guidelines

- Suivre les conventions de code Python (PEP 8)
- Utiliser Prettier pour le formatage JavaScript
- Écrire des tests pour les nouvelles fonctionnalités
- Documenter les nouvelles API routes
- Mettre à jour le README si nécessaire

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Thérèse-Marie LEFOULON & Robin DAVID**
- École : Holberton School Laval
- Formation : Fondamentaux du développement Full Stack
- GitHub : [@Timi-Holberton](https://github.com/Timi-Holberton)
- GitHub : [@Robin-1998](https://github.com/Robin-1998)


## 🙏 Remerciements

- **Holberton School Laval** pour la formation complète en développement Full Stack
- **J.R.R. Tolkien** pour l'univers inspirant du Seigneur des Anneaux
- La communauté open source pour les outils et bibliothèques utilisés

## 📚 Ressources

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation React](https://react.dev/)
- [Documentation PostGIS](https://postgis.net/documentation/)
- [Documentation Leaflet](https://leafletjs.com/)
- [Holberton School](https://www.holbertonschool.com/)
