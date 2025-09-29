28/09/25 - Timi
- Création de la Structure en attente de Pull Request Robin (branche feature/structure).  

29/09/25 - Timi
- début création base de données à partir du document Base de données établie dans la Part 3 du projet (branche feature/basedonneeTM).  
	-> Problème observé : manque relation entre character et race dans le doc.  

	-> choix de BIGSERIAL au lieu de BIGINT pour id (PostgreSQL crée automatiquement une séquence. Chaque nouvel INSERT génère un nouvel ID unique automatiquement).
   
	-> utilisation de SMALLINT pour star_year et death_year (2 octets au lieu de 4 pour int).  

	-> Table map_marker x et y FLOAT transformé en location GEOMETRY(POINT, 0) pour la cohérence/homogénéité avec map_region. POINT contient déjà x et y, il ne faut qu'une seule colonne donc x et y = location.  

	-> Ajout d'une table "relation_type" pour lié le personnage, et aussi la table histoire : évolution facile, évite les erreurs de frappe, évite les doublons (anniversaire lié à Bilbon ET hobbit-bourg) peut être réutiliser pour d'autre table, plus flexible (ajoute de colonnes supplémentaire, meilleure compatibilité avec les ORM. On peut ajouter un champ category dans relation_types pour spécifier la relation (optionnel, ex : personnage, histoire, les_deux).

  	-> insertion données 2 Users Admin : Robin Admin et Timi Admin + 1 User connecté John Doe
	-> insertion données race_type
	-> insertion données relation_type
