28/09/25
- Création de la Structure en attente de Pull Request Robin (branche feature/structure).  

29/09/25
- début création base de données à partir du document Base de données établie dans la Part 3 du projet (branche feature/basedonneeTM).  
	-> Problème observé : manque relation entre character et race dans le doc.  

	-> choix de BIGSERIAL au lieu de BIGINT pour id (PostgreSQL crée automatiquement une séquence. Chaque nouvel INSERT génère un nouvel ID unique automatiquement).
   
	-> utilisation de SMALLINT pour star_year et death_year (2 octets au lieu de 4 pour int).  

	-> Table map_marker x et y FLOAT transformé en location GEOMETRY(POINT, 0) pour la cohérence/homogénéité avec map_region. POINT contient déjà x et y, il ne faut qu'une seule colonne donc x et y = location.  

	-> Ajout d'une table "relation_type" pour lié le personnage, et aussi la table histoire : évolution facile, évite les erreurs de frappe, évite les doublons (anniversaire lié à Bilbon ET hobbit-bourg) peut être réutiliser pour d'autre table, plus flexible (ajoute de colonnes supplémentaire, meilleure compatibilité avec les ORM. On peut ajouter un champ category dans relation_types pour spécifier la relation (optionnel, ex : personnage, histoire, les_deux).

  	-> insertion données 2 Users Admin : Robin Admin et Timi Admin + 1 User connecté John Doe.  
	-> insertion données race_type.  
	-> insertion données relation_type.  

30/09/25
- continue à implémenter la base de données.
- début configuration aplication Flask.
- début code class user.

01/10/25
- modification de la structure.  
	-> supprimer des models inutiles (character, race, events).  
  	-> ajout des models reviews et image_post.  
  	-> ajout du dossier persistence et fichier repository.
- début implémentation de api_user, facade user, repository, repository_user.  

02/10/25
- continue sur api_user, facade user, repository, repository_user.
- test avec Postman pour User Post get, get_id, put TEST OK.
- implémentation de reviews model, image_post fini.
- implémentation de la facade reviews et image_post en cours.
- implémentation de api_auth et api_admin en cours, récupération de Token OK.
- implémentation de la base de données pour Timi en local OK.
- ajout des routes dans __init__.py de app.  

03/10/25
✅ Tests fonctionnels (Postman)

Réalisation de tests Postman pour toutes les fonctionnalités CRUD sur les parties suivantes :
- admin
- auth
- post_image

➕ Ajout de nouvelles fonctionnalités

Intégration de l’API reviews :
L'API a été ajoutée mais pas encore testée sous Postman.

🛠️ Modifications sur post_image
Modification du schéma de la base de données :

Ajout de deux colonnes :
- image_data (type BYTEA) pour stocker les images directement en base.
- image_mime_type pour conserver le type MIME (ex: image/png, image/jpeg, etc.).

Raisons du changement :
Les images sont uploadées par les utilisateurs → pas d’URL, donc stockage en base requis.

Mise à jour des modèles et des fonctions CRUD pour refléter ces changements de structure.

🖥️ Environnement local

Mise en place des bases de données locales dédiées pour :
- Robin
- Timi
→ Serveurs de développement indépendants configurés localement.
