--Table Users
CREATE TABLE users (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE,
	password VARCHAR(128) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE
);

--Table image art
CREATE TABLE image_post (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	title VARCHAR(200) NOT NULL,
	description TEXT NOT NULL,
	image_url TEXT NOT NULL,

	user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);

--Table Image commentaire
CREATE TABLE image_comment (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	comment TEXT NOT NULL,

	user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
	image_post_id BIGINT REFERENCES image_post(id) ON DELETE CASCADE
);

CREATE TYPE place_enum AS ENUM ('Région','Ville', 'Village','Forteresse','Mer','Lac/Marais','Rivière')

--Table places
CREATE TABLE places (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	title VARCHAR(200) NOT NULL,
	type_place place_enum NOT NULL, -- j'ai remplacé type par type_place pour plus de précision/comprehension
	description TEXT NOT NULL,

	parent_id BIGINT REFERENCES places(id), --clé étrangère auto-référente,
	UNIQUE(title, parent_id)
);

--Table Races (créature)
CREATE TABLE races (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(50) NOT NULL UNIQUE, --Humain, Elfe, Orc...
	weakness VARCHAR(50) NOT NULL,
	strength VARCHAR(50) NOT NULL,
	description TEXT NOT NULL,

	place_id BIGINT REFERENCES places(id)
);

--Table Relation_types (vaut pour le personnage et pour l'histoire : naissance, résidence, décès, voyage, bataille, cérémonie, quête, rencontre...)
CREATE TABLE relation_types (
	id BIGSERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE
);

--Table histoire
CREATE TABLE history (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(150) NOT NULL,
	description TEXT NOT NULL,
	start_year SMALLINT,
	end_year SMALLINT,
	era VARCHAR(25),

	place_id BIGINT REFERENCES places(id),
	relation_type_id BIGINT REFERENCES relation_types(id),
	UNIQUE(name, start_year, place_id) -- Pour éviter d’avoir le même événement historique en double dans un même lieu.
);

--Table characters
CREATE TABLE characters (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(100) NOT NULL,
	birth_date SMALLINT NOT NULL,
	death_date SMALLINT,
	era_birth VARCHAR(25) NOT NULL,
	era_death VARCHAR(25),

	gender VARCHAR(10) NOT NULL,
	profession VARCHAR(100) NOT NULL,
	description TEXT NOT NULL,

	race_id BIGINT REFERENCES races(id)
);

--Table character_history
CREATE TABLE character_history (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	role VARCHAR(50) NOT NULL,

	character_id BIGINT REFERENCES characters(id),
	history_id BIGINT REFERENCES history(id),
	UNIQUE(character_id, history_id) --Un personnage ne peut pas être lié deux fois au même événement historique.
);

--Table character_place
CREATE TABLE character_place (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	relation_type_id BIGINT REFERENCES relation_types(id),
	character_id BIGINT REFERENCES characters(id),
	place_id BIGINT REFERENCES places(id),
	UNIQUE(character_id, place_id, relation_type_id) --évite qu’un personnage ait plusieurs fois la même relation sur un même lieu
);

--Table map_region
CREATE TABLE map_region (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(100) NOT NULL,
	shape_data GEOMETRY(POLYGON, 0) NOT NULL, -- SRID 0 = coordonnées locales, shape_data pourra stocker un polygone défini en pixels ou proportion de l’image.

	place_id BIGINT REFERENCES places(id)
);

--Table map_marker
CREATE TABLE map_marker (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(100) NOT NULL,
	location GEOMETRY(POINT, 0) NOT NULL, -- POINT contient déjà x et y, il ne faut qu'une seule colonne

	place_id BIGINT REFERENCES places(id)
);

--Table entity_descriptions
CREATE TABLE entity_descriptions (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	title VARCHAR(100) NOT NULL,
	content TEXT NOT NULL,
	order_index INT,

	relation_type_id BIGINT REFERENCES relation_types(id),
	entity_id BIGINT -- ??
);

----------------------------------INSERT USER--------------------------------------------------
--Table sans dépendances
--User Robin Admin
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES('Robin', 'Admin', '10616@holbertonstudents.com', '$2y$10$pNic29UShtoK5gwuE0DS8eNQEK.RsZLIt/EO4dkS22aAqrcchuzEm', TRUE);
RETURNING id;

--User Timi Admin
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES('Timi', 'Admin', '10614@holbertonstudents.com', '$2y$10$1QljT3VlKRLmxEeokVLxKOS/eocY8xb3LP95mSVLJaCURQucH9pKO', TRUE);

--User connecté John Doe
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES('John', 'Doe', 'johndoe@gmail.com', '$2y$10$O8b3kgMMMZhZ5m0t6bVxZOCHoDXTSgBkJrdwNJixVQXk1Z04TKwBS', FALSE);

--------------------------------------INSERT RELATION-TYPE----------------------------------------------

INSERT INTO relation_types (name)
VALUES('naissance'), ('résidence'), ('décès'), ('union'), ('voyage'), ('quête'), ('bataille'), ('rencontre'), ('trahison'), ('cérémonie'), ('exploration');

-----------------------------------------INSERT PLACES--------------------------------------------------

INSERT INTO places (title, type_place, description, parent_id)
VALUES('Gondor', 'Région', 'Région du Gondor', NULL);

INSERT INTO places (title, type_place, description, parent_id)
VALUES ('Minas Tirith', 'Ville', 'Capitale du Gondor', 1);

INSERT INTO places (title, type_place, description, parent_id)
VALUES('Rohan', 'Région', 'Région du Rohan', NULL);

INSERT INTO places (title, type_place, description, parent_id)
VALUES('Forêt de Fangorn', 'Forêt', 'Ancienne et mystérieuse forêt peuplée d’Ents, gardiens des arbres', 1);

INSERT INTO places (title, type_place, description, parent_id)
VALUES('Osgiliath', 'Village', 'Cité fortirtifié en ruine attaqué par les orques', 2);

-----------------------------------------INSERT Races--------------------------------------------------

INSERT INTO races (name, weakness, strength, description)
VALUES('Humain', 'Corruptibles par le pouvoir, influençable, faiblesse au maladie + magie' 'Stratèges militaires, nombreux', 'Dans le pays que les elfes appelaient Hildórien, (pays des suivants), situé dans la partie extrême-orientale de la terre du milieu, les hommes ouvrirent les yeux à cette nouvelle lumière');

INSERT INTO races (name, weakness, strength, description)
VALUES('Nain', 'Orgueilleux et avare', 'Résistant et force physique', 'Aulë, le forgeron des Valar, façonna les septs père des nains dans une grande caverne sous les montagnes de la Terre du Milieu. Aulë fit les nains trapus et forts, insensible au froid et au feu, et plus robustes que les races qui suivirent.')

-----------------------------------------INSERT History--------------------------------------------------

INSERT INTO history (name, description, start_year, end_year, era)
VALUES('Bataille des Champs du Pelennor', 'La bataille des Champs du Pelennor est un affrontement décisif devant Minas Tirith, où les forces du Gondor et de ses alliés affrontent l’armée de Sauron pour défendre la cité et préparer la chute du Mordor. La bataille a duré une journée', '3019', 'NULL', 'Troisième âge')

INSERT INTO history (name, description, start_year, end_year, era)
VALUES('Anniversaire de Bilbon Saquet', "En l'an 3001, Bilbon organisa une grande fête d'anniversaire pour son 111ème anniversaire. Il disparut sous les yeux de ses invités laissant tout ses biens, y compris l'anneau unique, à son jeune cousin Frodon Sacquet. Bilbon s'en va vers Foncombe passer des jours paisible.", '3001', NULL, 'Troisième âge')

-----------------------------------------INSERT Character--------------------------------------------------

INSERT INTO characters (name, birth_date, death_date, era_birth, era_death, gender, profession, description)
VALUES('Gimli', 2879, 120, 'Troisième âge', 'Quatrième âge', 'Masculin', 'Guerrier', 'Nain robuste et fier du royaume d Erebor, membre de la Communauté de l Anneau.');

INSERT INTO characters (name, birth_date, death_date, era_birth, era_death, gender, profession, description)
VALUES('Eowyn', 2995, NULL, 'Troisième âge', 'Quatrième âge', 'Féminin', 'Guerrière, noble', 'Est une femme du rohan, nièce du roi Théoden et la soeur d''Eomer');

-----------------------------------------INSERT Image--------------------------------------------------



-----------------------------------INSERT Commentaire image--------------------------------------------------



-----------------------------------------INSERT map_region--------------------------------------------------

INSERT INTO regions (nom, shape_data)
VALUES ('Gondor', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[400,450],[650,450],[650,600],[400,600],[400,450]]]}'));

-----------------------------------------INSERT map_marker--------------------------------------------------

INSERT INTO map_marker (name, location)
VALUES('Minas Tirith', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[500,500]}'));

