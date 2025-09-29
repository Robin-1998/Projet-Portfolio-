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

--Table image de user
CREATE TABLE image_post (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	title VARCHAR(200) NOT NULL,
	description TEXT NOT NULL,
	image_url TEXT NOT NULL,

	user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);

--Table commentaire image
CREATE TABLE image_comment (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	comment TEXT NOT NULL,

	user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
	image_post_id BIGINT REFERENCES image_post(id) ON DELETE CASCADE
);

--Table places
CREATE TABLE places (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	title VARCHAR(200) NOT NULL,
	type_place INT, -- j'ai remplacé type par type_place pour plus de précision/comprehension
	description TEXT NOT NULL,

	parent_id BIGINT REFERENCES places(id), --clé étrangère auto-référente,
	UNIQUE(title, parent_id)
);

--Table Races_types
CREATE TABLE races_types (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(50) NOT NULL UNIQUE --Humanoïde, Créature magique, Bête sauvage...
);

--Table Races (créature)
CREATE TABLE races (
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	name VARCHAR(50) NOT NULL, --Humain, Elfe, Orc...
	weakness VARCHAR(50) NOT NULL,
	strength VARCHAR(50) NOT NULL,
	description TEXT NOT NULL,

	races_type_id BIGINT REFERENCES races_types(id),
	place_id BIGINT REFERENCES places(id),
	UNIQUE(name, races_type_id) --Pour éviter d’avoir deux races avec le même nom dans un même type, si races_type_id = "Humanoïde", il ne faut pas avoir deux fois Elf.
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
	birth_date DATE NOT NULL,
	death_date DATE,
	gender VARCHAR(10) NOT NULL,
	profession VARCHAR(100) NOT NULL,

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

--User Timi Admin
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES('Timi', 'Admin', '10614@holbertonstudents.com', '$2y$10$1QljT3VlKRLmxEeokVLxKOS/eocY8xb3LP95mSVLJaCURQucH9pKO', TRUE);

--User connecté John Doe
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES('John', 'Doe', 'johndoe@gmail.com', '$2y$10$O8b3kgMMMZhZ5m0t6bVxZOCHoDXTSgBkJrdwNJixVQXk1Z04TKwBS', FALSE);

----------------------------------INSERT RACE-TYPE--------------------------------------------------

INSERT INTO races_types (name)
VALUES('Humanoïde'), ('Créature magique'), ('Créature maléfique'), ('Animal fantastique');

----------------------------------INSERT RELATION-TYPE----------------------------------------------

INSERT INTO relation_types (name)
VALUES('naissance'), ('résidence'), ('décès'), ('union'), ('voyage'), ('quête'), ('bataille'), ('rencontre'), ('trahison'), ('cérémonie'), ('exploration');

------------------------------------INSERT PLACES--------------------------------------------------
