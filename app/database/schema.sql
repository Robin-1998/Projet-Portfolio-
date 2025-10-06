-- -----------------------------
-- Activer PostGIS (si pas déjà)
-- -----------------------------
CREATE EXTENSION IF NOT EXISTS postgis;
-- -----------------------------
-- Table Users
-- -----------------------------
DROP TABLE IF EXISTS users CASCADE;
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
-- -----------------------------
-- Tables images
-- -----------------------------
DROP TABLE IF EXISTS image_post CASCADE;
CREATE TABLE image_post (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    image_data BYTEA NOT NULL,
    image_mime_type VARCHAR(50) NOT NULL,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);
DROP TABLE IF EXISTS reviews CASCADE;
CREATE TABLE reviews (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT NOT NULL,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    image_post_id BIGINT REFERENCES image_post(id) ON DELETE CASCADE
);
-- -----------------------------
-- Enum Place
-- -----------------------------
DROP TYPE IF EXISTS place_enum;
CREATE TYPE place_enum AS ENUM ('Région','Ville','Village','Forteresse','Mer','Lac/Marais','Rivière');
-- -----------------------------
-- Table Places
-- -----------------------------
DROP TABLE IF EXISTS places CASCADE;
CREATE TABLE places (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(200) NOT NULL,
    type_place place_enum NOT NULL,
    description TEXT NOT NULL,
    parent_id BIGINT REFERENCES places(id),
    UNIQUE(title, parent_id)
);
-- -----------------------------
-- Table Races
-- -----------------------------
DROP TABLE IF EXISTS races CASCADE;
CREATE TABLE races (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(50) NOT NULL UNIQUE,
    weakness VARCHAR(255) NOT NULL,
    strength VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    place_id BIGINT REFERENCES places(id)
);
-- -----------------------------
-- Table Relation Types
-- -----------------------------
DROP TABLE IF EXISTS relation_types CASCADE;
CREATE TABLE relation_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
-- -----------------------------
-- Table History
-- -----------------------------
DROP TABLE IF EXISTS history CASCADE;
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
    UNIQUE(name, start_year, place_id)
);
-- -----------------------------
-- Table Characters
-- -----------------------------
DROP TABLE IF EXISTS characters CASCADE;
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
-- -----------------------------
-- Table Character_History
-- -----------------------------
DROP TABLE IF EXISTS character_history CASCADE;
CREATE TABLE character_history (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50) NOT NULL,
    character_id BIGINT REFERENCES characters(id),
    history_id BIGINT REFERENCES history(id),
    UNIQUE(character_id, history_id)
);
-- -----------------------------
-- Table Character_Place
-- -----------------------------
DROP TABLE IF EXISTS character_place CASCADE;
CREATE TABLE character_place (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    relation_type_id BIGINT REFERENCES relation_types(id),
    character_id BIGINT REFERENCES characters(id),
    place_id BIGINT REFERENCES places(id),
    UNIQUE(character_id, place_id, relation_type_id)
);
-- -----------------------------
-- Tables Map avec PostGIS
-- -----------------------------
DROP TABLE IF EXISTS map_region CASCADE;
CREATE TABLE map_region (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    shape_data GEOMETRY(POLYGON, 0) NOT NULL,
    place_id BIGINT REFERENCES places(id)
);
DROP TABLE IF EXISTS map_marker CASCADE;
CREATE TABLE map_marker (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    location GEOMETRY(POINT, 0) NOT NULL,
    place_id BIGINT REFERENCES places(id)
);
-- -----------------------------
-- Table Entity Descriptions
-- -----------------------------
DROP TABLE IF EXISTS entity_descriptions CASCADE;
CREATE TABLE entity_descriptions (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    order_index INT,
    relation_type_id BIGINT REFERENCES relation_types(id),
    entity_id BIGINT
);
-- -----------------------------
-- Inserts utilisateurs
-- -----------------------------
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES
('Robin','Admin','10616@holbertonstudents.com','$2y$10$pNic29UShtoK5gwuE0DS8eNQEK.RsZLIt/EO4dkS22aAqrcchuzEm',TRUE),
('Timi','Admin','10614@holbertonstudents.com','$2y$10$1QljT3VlKRLmxEeokVLxKOS/eocY8xb3LP95mSVLJaCURQucH9pKO',TRUE),
('John','Doe','johndoe@gmail.com','$2y$10$O8b3kgMMMZhZ5m0t6bVxZOCHoDXTSgBkJrdwNJixVQXk1Z04TKwBS',FALSE);
-- -----------------------------
-- Inserts Relation Types
-- -----------------------------
INSERT INTO relation_types (name)
VALUES
('naissance'), ('résidence'), ('décès'), ('union'), ('voyage'), ('quête'),
('bataille'), ('rencontre'), ('trahison'), ('cérémonie'), ('exploration');
-- -----------------------------
-- Inserts Places
-- -----------------------------
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Gondor', 'Région', 'Région du Gondor', NULL),
('Rohan', 'Région', 'Région du Rohan', NULL);
-- Sous-places
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Minas Tirith', 'Ville', 'Capitale du Gondor', 1),
('Osgiliath', 'Village', 'Cité fortifiée en ruine attaquée par les orques', 1),
('Forêt de Fangorn', 'Rivière', 'Ancienne et mystérieuse forêt peuplée d’Ents, gardiens des arbres', 2);
-- -----------------------------
-- Inserts Races
-- -----------------------------
INSERT INTO races (name, weakness, strength, description, place_id)
VALUES
('Humain',
 'Corruptibles par le pouvoir, influençable, faiblesse aux maladies et magie',
 'Stratèges militaires, nombreux',
 'Dans le pays que les elfes appelaient Hildórien, situé dans la partie extrême-orientale de la Terre du Milieu',
 1),
('Nain',
 'Orgueilleux et avare',
 'Résistant et force physique',
 'Aulë, le forgeron des Valar, façonna les septs père des nains dans une grande caverne sous les montagnes de la Terre du Milieu',
 2);
-- -----------------------------
-- Inserts Characters
-- -----------------------------
INSERT INTO characters (name, birth_date, death_date, era_birth, era_death, gender, profession, description, race_id)
VALUES
('Gimli', 2879, 120, 'Troisième âge', 'Quatrième âge', 'Masculin', 'Guerrier', 'Nain robuste et fier du royaume d’Erebor, membre de la Communauté de l’Anneau.', 2),
('Eowyn', 2995, NULL, 'Troisième âge', 'Quatrième âge', 'Féminin', 'Guerrière, noble', 'Fille du Rohan, nièce du roi Théoden et sœur d’Eomer', 1);
-- -----------------------------
-- Inserts History
-- -----------------------------
INSERT INTO history (name, description, start_year, end_year, era, place_id, relation_type_id)
VALUES
('Bataille des Champs du Pelennor',
 'Affrontement décisif devant Minas Tirith entre Gondor et les forces de Sauron.',
 3019, 3019, 'Troisième âge', 3, 7), -- 3 = Minas Tirith, 7 = bataille
('Anniversaire de Bilbon Sacquet',
 'Bilbon organisa une grande fête pour ses 111 ans.',
 3001, 3001, 'Troisième âge', 3, 4); -- 3 = Minas Tirith, 4 = union/fête
-- -----------------------------
-- Inserts Map
-- -----------------------------
INSERT INTO map_region (name, shape_data, place_id)
VALUES
('Gondor', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[400,450],[650,450],[650,600],[400,600],[400,450]]]}'), 1);
INSERT INTO map_marker (name, location, place_id)
VALUES
('Minas Tirith', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[500,500]}'), 3);
