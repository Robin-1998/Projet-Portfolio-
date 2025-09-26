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

Portfolio Holberton/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── V1/
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── places_map.py
│   │       ├── events.py
│   │       ├── races.py
│   │       ├── characters.py
│   │       ├── art.py
│   │       └── map_data.py # données cartographiques x,y
│   ├── database/
│   │   ├── schema.sql
│   │   └── migrations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── basemodel.py
│   │   ├── events.py
│   │   ├── races.py
│   │   ├── characters.py
│   │   ├── place_map.py
│   │   ├── spatial.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── spatial_service.py
│   │   ├── facade.py
│   │   └── map_service.py
│   └── bases_files/
│       ├── images/
│       │   ├── icons
│       │   └── images_page
│       ├── src/
│       │   ├── app.css
│       │   ├── app.jsx
│       │   ├── index.css
│       │   └── main.jsx
│       ├── eslint.config.js
│       ├── index.html
│       ├── package.json
│       └── vite.config.js
├── __init__.py
├── run.py
├── tests
├── requirements.txt
├── run-tests.py
└── README.md

# Collaborateurs
Il a été conçu et développé par Thérèse-Marie LEFOULON et Robin DAVID. 
