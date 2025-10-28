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
-- -----------------------------
-- Tables reviews
-- -----------------------------
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
CREATE TYPE place_enum AS ENUM (
    'region',
    'foret',
    'montagne',
    'forteresse',
    'ville',
    'capitale',
    'eau',
    'ruine',
    'dark',
    'mine',
    'port',
    'pont',
    'plaine',
    'chemin',
    'monument',
    'special',
    'default'
);
-- -----------------------------
-- Table Places
-- -----------------------------
DROP TABLE IF EXISTS places CASCADE;
CREATE TABLE places (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(200) NOT NULL UNIQUE,
    type_place place_enum NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(500),
    parent_id BIGINT REFERENCES places(id)
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
	citation VARCHAR(400)
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
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT NOT NULL,
	citation VARCHAR(400),
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
    name VARCHAR(100) NOT NULL UNIQUE,
    birth_date SMALLINT,
    death_date SMALLINT,
    era_birth VARCHAR(25) NOT NULL,
    era_death VARCHAR(25),
    gender VARCHAR(10) NOT NULL,
    profession VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
	citation VARCHAR(400),
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
    name VARCHAR(100) NOT NULL UNIQUE,
    shape_data GEOMETRY(POLYGON, 0) NOT NULL,
    place_id BIGINT REFERENCES places(id)
);

-- Création de l'ENUM pour les catégories de marqueurs
CREATE TYPE marker_type AS ENUM (
    'foret',
    'montagne',
    'forteresse',
    'ville',
    'capitale',
    'eau',
    'ruine',
    'dark',
    'mine',
    'port',
    'pont',
    'plaine',
    'chemin',
    'monument',
    'special',
    'default'
);

DROP TABLE IF EXISTS map_marker CASCADE;
CREATE TABLE map_marker (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL UNIQUE,
    location GEOMETRY(POINT, 0) NOT NULL,
    type marker_type NOT NULL DEFAULT 'default',
    place_id BIGINT REFERENCES places(id)
);

CREATE TABLE descriptions (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL CHECK (entity_type IN ('character', 'place', 'race', 'history', 'region', 'foret',
    'montagne',
    'forteresse',
    'ville',
    'capitale',
    'eau',
    'ruine',
    'dark',
    'mine',
    'port',
    'pont',
    'plaine',
    'chemin',
    'monument',
    'special',
    'default')),
    entity_id BIGINT NOT NULL,
    title VARCHAR(100),
    content TEXT NOT NULL,
    order_index INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
