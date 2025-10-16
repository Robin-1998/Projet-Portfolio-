## 28/09/25
- Création de la Structure en attente de Pull Request Robin (branche feature/structure).

## 29/09/25
- début création base de données à partir du document Base de données établie dans la Part 3 du projet (branche feature/basedonneeTM).
	-> Problème observé : manque relation entre character et race dans le doc.

	-> choix de BIGSERIAL au lieu de BIGINT pour id (PostgreSQL crée automatiquement une séquence. Chaque nouvel INSERT génère un nouvel ID unique automatiquement).

	-> utilisation de SMALLINT pour star_year et death_year (2 octets au lieu de 4 pour int).

	-> Table map_marker x et y FLOAT transformé en location GEOMETRY(POINT, 0) pour la cohérence/homogénéité avec map_region. POINT contient déjà x et y, il ne faut qu'une seule colonne donc x et y = location.

	-> Ajout d'une table "relation_type" pour lié le personnage, et aussi la table histoire : évolution facile, évite les erreurs de frappe, évite les doublons (anniversaire lié à Bilbon ET hobbit-bourg) peut être réutiliser pour d'autre table, plus flexible (ajoute de colonnes supplémentaire, meilleure compatibilité avec les ORM. On peut ajouter un champ category dans relation_types pour spécifier la relation (optionnel, ex : personnage, histoire, les_deux).

  	-> insertion données 2 Users Admin : Robin Admin et Timi Admin + 1 User connecté John Doe.
	-> insertion données race_type.
	-> insertion données relation_type.

## 30/09/25
- continue à implémenter la base de données.
- début configuration aplication Flask.
- début code class user.

## 01/10/25
- modification de la structure.
	-> supprimer des models inutiles (character, race, events).
  	-> ajout des models reviews et image_post.
  	-> ajout du dossier persistence et fichier repository.
- début implémentation de api_user, facade user, repository, repository_user.

## 02/10/25
- continue sur api_user, facade user, repository, repository_user.
- test avec Postman pour User Post get, get_id, put TEST OK.
- implémentation de reviews model, image_post fini.
- implémentation de la facade reviews et image_post en cours.
- implémentation de api_auth et api_admin en cours, récupération de Token OK.
- implémentation de la base de données pour Timi en local OK.
- ajout des routes dans __init__.py de app.

## 03/10/25
✅ Tests fonctionnels (Postman)

Réalisation de tests Postman pour toutes les fonctionnalités CRUD sur les parties suivantes :
- admin, auth, post_image ➕ Ajout de nouvelles fonctionnalités

Ajout des modèles et des namespaces associés suivants :
- Race, Character, History

Implémentation des APIs :
- Race, Character, History, Reviews (non testé sur Postman)

🛠️ Modifications sur post_image
- Modification du schéma de la base de données :

Ajout de deux colonnes :
- image_data (type BYTEA) pour stocker les images directement en base.
- image_mime_type pour conserver le type MIME (ex: image/png, image/jpeg, etc.).

Raisons du changement :
- Les images sont uploadées par les utilisateurs → pas d’URL, donc stockage en base requis.
- Mise à jour des modèles et des fonctions CRUD pour refléter ces changements de structure.

Refactorisation de la facade :
- Mise en place de facade2 pour la gestion centralisée des entités race, character, et history.

🖥️ Environnement local
Mise en place des bases de données locales dédiées pour Robin & Timi
→ Serveurs de développement indépendants configurés localement.

## 06/10/25

- Review test API Postman ok GET_id, GET_ALL, POST, PUT, DELETE.

- Implémentation de search api et facade, test GET sur race, personnage, histoire OK.

- Mise à jour de la base de données avec les modifications sur table image_post pour Timi en local.

- En cours :
	- API - model - facade pour Place - map_marker et map_région.
	- ajout de model pour marker et région.
	- test api fonctionne mais désordonnée.
	- problème lié entre parent_id et children, en cours de recherche.

## 07/10/25

- Base de données :
	- Création de data.sql = utilisé pour faire les insert de données en dur
	- schema.sql = création des tables uniquement

- Reviews :
	- Ajout de route dans l'api_reviews pour récupérer les reviews par user ou par image.
	- Modification de la méthode get image pour retourner un objet au lieu d'un dict.
	- Test APi ok

- Map marker & map region :
	- Finalisation model api facade
	- Test API Map marker et map régions = OK

- Utilisation de QGIS :
	- pour géoréférencer l'image et visualiser les points.
	- point cardinaux ok

## 08/10/25

- Tests back-end
	- Commencement des tests pour les différents modèles et API
	- Github actions ne sera peut-être pas utilisé car utilisation des tests en brut sans interrogé une base de donnée fictive

- Apprentissage de React

## 09/10/25

- Tests back-end
	- Test en utilisant une copie de notre base de donnée (DB test) pour éviter de faire les tests sur notre base de donnée

- QGIS
	- QGIS ne sera utile que pour la visualisation des coordonnées pour après les implémenter via postgresql/leaflet.
	- QGIS sera également utile pour visualiser les polygones en tant réelle pour avoir un visuel de ce que ça pourrait donner.

- Apprentissage de React

## 10/10/2025

- Test back-end
	- Finalisation des tests unitaires sur modèle + façade + API à l'aide de pytest qui interroge une copie de notre base de donnée
	- Script de test postman réalisé sur toutes les routes API terminé

## 13/10/2025

- Supression de fichier et dossier inutile
- Apprentissage de React
- Architecture du projet grandement modifié sur la partie front-end avec react
- Familiarisation avec React : test de démarrage utilisant Vite sur les fichiers main.jsx et app.jsx

## 14/10/2025

- Apprentissage de React
- Ajout des composants de fonction pour footer + header et navigation (non terminés)
- Images redimensionné pour la barre de navigation

## 15/10/2025

- Familiarisation avec les routes react (premier test réussi pour le login)
- Restructuration de l'architecture dans le README
- Continuation sur le footer / header / Navigation
- Contenu des pages mentions légales et sources ajoutés

## 16/10/2025

- 
## 17/10/2025
## 20/10/2025
## 21/10/2025
## 22/10/2025
## 23/10/2025
## 24/10/2025
