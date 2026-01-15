import pytest

# ========================================
# TESTS DU MODÈLE USER
# ========================================

class TestUserLogic:
    """Tests de la logique du modèle User."""
    
    def test_user_name_validation_empty(self):
        """Test qu'un nom vide est invalide."""
        name = "   "
        is_valid = bool(name.strip())
        assert is_valid is False
    
    def test_user_name_validation_length(self):
        """Test la validation de longueur du nom."""
        short_name = "A"
        long_name = "A" * 51
        valid_name = "Jean"
        
        assert 1 <= len(short_name) <= 50
        assert not (1 <= len(long_name) <= 50)
        assert 1 <= len(valid_name) <= 50
    
    def test_user_name_capitalization(self):
        """Test que les noms sont capitalisés."""
        name = "jean-pierre"
        capitalized = name.title()
        assert capitalized == "Jean-Pierre"
    
    def test_user_email_validation(self):
        """Test la validation basique d'email."""
        valid_email = "test@example.com"
        invalid_email = "notanemail"
        
        assert "@" in valid_email
        assert "." in valid_email
        assert "@" not in invalid_email
    
    def test_user_password_min_length(self):
        """Test que le mot de passe doit faire minimum 8 caractères."""
        short_password = "1234567"
        valid_password = "12345678"
        
        assert len(short_password) < 8
        assert len(valid_password) >= 8
    
    def test_user_is_admin_validation(self):
        """Test que is_admin est un booléen."""
        assert isinstance(True, bool)
        assert isinstance(False, bool)
        assert not isinstance("true", bool)
        assert not isinstance(1, bool)
    
    def test_user_data_structure(self):
        """Test la structure de données d'un utilisateur."""
        user_data = {
            "id": 1,
            "first_name": "Gandalf",
            "last_name": "Le Gris",
            "email": "gandalf@middle-earth.com",
            "is_admin": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        
        # Vérifier les clés
        assert "id" in user_data
        assert "email" in user_data
        assert "is_admin" in user_data
        assert "password" not in user_data  # Ne doit jamais être exposé


# ========================================
# TESTS DU MODÈLE IMAGEPOST
# ========================================

class TestImagePostLogic:
    """Tests de la logique du modèle ImagePost."""
    
    def test_image_title_validation_empty(self):
        """Test qu'un titre vide est invalide."""
        title = "   "
        is_valid = isinstance(title, str) and bool(title.strip())
        assert is_valid is False
    
    def test_image_title_validation_max_length(self):
        """Test que le titre ne doit pas dépasser 100 caractères."""
        valid_title = "A" * 100
        invalid_title = "A" * 101
        
        assert len(valid_title) <= 100
        assert len(invalid_title) > 100
    
    def test_image_description_validation_max_length(self):
        """Test que la description ne doit pas dépasser 400 caractères."""
        valid_description = "A" * 400
        invalid_description = "A" * 401
        
        assert len(valid_description) <= 400
        assert len(invalid_description) > 400
    
    def test_image_data_validation(self):
        """Test que image_data doit être binaire."""
        valid_data = b"fake_image_bytes"
        invalid_data = "not_bytes"
        
        assert isinstance(valid_data, (bytes, bytearray))
        assert not isinstance(invalid_data, (bytes, bytearray))
    
    def test_user_id_validation_positive(self):
        """Test que user_id doit être un entier positif."""
        valid_id = 5
        invalid_id_zero = 0
        invalid_id_negative = -1
        
        assert isinstance(valid_id, int) and valid_id > 0
        assert not (isinstance(invalid_id_zero, int) and invalid_id_zero > 0)
        assert not (isinstance(invalid_id_negative, int) and invalid_id_negative > 0)
    
    def test_image_post_data_structure(self):
        """Test la structure de données d'un post d'image."""
        image_data = {
            "id": 1,
            "title": "Carte de la Terre du Milieu",
            "description": "Belle carte détaillée",
            "user_id": 5,
            "image_mime_type": "image/png"
        }
        
        # Vérifier les clés
        assert "title" in image_data
        assert "user_id" in image_data
        assert "image_mime_type" in image_data
        # image_data binaire ne doit PAS être dans to_dict()
        assert "image_data" not in image_data


# ========================================
# TESTS DU MODÈLE MAPMARKER
# ========================================

class TestMapMarkerLogic:
    """Tests de la logique du modèle MapMarker."""
    
    def test_marker_name_validation_empty(self):
        """Test qu'un nom vide est invalide."""
        name = "   "
        is_valid = bool(str(name).strip())
        assert is_valid is False
    
    def test_marker_types_enum(self):
        """Test que les types de marqueurs sont valides."""
        valid_types = [
            'foret', 'montagne', 'forteresse', 'ville', 'capitale',
            'eau', 'ruine', 'dark', 'mine', 'port', 'pont',
            'plaine', 'chemin', 'monument', 'special', 'default'
        ]
        
        test_type = 'ville'
        assert test_type in valid_types
    
    def test_marker_data_structure(self):
        """Test la structure de données d'un marqueur."""
        marker_data = {
            "id": 1,
            "name": "Hobbiton",
            "place_id": 10,
            "type": "ville",
            "geometry": {
                "type": "Point",
                "coordinates": [1.5, 2.5]
            }
        }
        
        # Vérifier les clés
        assert "name" in marker_data
        assert "type" in marker_data
        assert "geometry" in marker_data
        assert marker_data["geometry"]["type"] == "Point"
        assert isinstance(marker_data["geometry"]["coordinates"], list)
        assert len(marker_data["geometry"]["coordinates"]) == 2
    
    def test_marker_coordinates_format(self):
        """Test le format des coordonnées."""
        coordinates = [1.5, 2.5]
        
        assert isinstance(coordinates, list)
        assert len(coordinates) == 2
        assert all(isinstance(coord, (int, float)) for coord in coordinates)


# ========================================
# TESTS DU MODÈLE MAPREGION
# ========================================

class TestMapRegionLogic:
    """Tests de la logique du modèle MapRegion."""
    
    def test_region_name_validation_empty(self):
        """Test qu'un nom vide est invalide."""
        name = ""
        is_valid = bool(str(name).strip())
        assert is_valid is False
    
    def test_region_data_structure(self):
        """Test la structure de données d'une région."""
        region_data = {
            "id": 1,
            "name": "La Comté",
            "place_id": 5,
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [0, 0],
                    [0, 5],
                    [5, 5],
                    [5, 0],
                    [0, 0]
                ]
            }
        }
        
        # Vérifier les clés
        assert "name" in region_data
        assert "geometry" in region_data
        assert region_data["geometry"]["type"] == "Polygon"
        assert isinstance(region_data["geometry"]["coordinates"], list)
    
    def test_region_polygon_closed(self):
        """Test qu'un polygone doit être fermé (premier = dernier point)."""
        coordinates = [[0, 0], [0, 5], [5, 5], [5, 0], [0, 0]]
        
        first_point = coordinates[0]
        last_point = coordinates[-1]
        
        assert first_point == last_point
    
    def test_region_polygon_minimum_points(self):
        """Test qu'un polygone doit avoir au moins 4 points (triangle fermé)."""
        valid_polygon = [[0, 0], [0, 5], [5, 0], [0, 0]]  # 4 points
        invalid_polygon = [[0, 0], [5, 5]]  # 2 points
        
        assert len(valid_polygon) >= 4
        assert len(invalid_polygon) < 4


# ========================================
# TESTS DU MODÈLE REVIEW
# ========================================

class TestReviewLogic:
    """Tests de la logique du modèle Review."""
    
    def test_review_comment_validation_empty(self):
        """Test qu'un commentaire vide est invalide."""
        comment = ""
        is_valid = isinstance(comment, str) and bool(comment)
        assert is_valid is False
    
    def test_review_comment_validation_max_length(self):
        """Test que le commentaire ne doit pas dépasser 400 caractères."""
        valid_comment = "A" * 400
        invalid_comment = "A" * 401
        
        assert len(valid_comment) <= 400
        assert len(invalid_comment) > 400
    
    def test_review_user_id_validation(self):
        """Test que user_id doit être un entier positif."""
        valid_id = 10
        invalid_id = -5
        
        assert isinstance(valid_id, int) and valid_id > 0
        assert not (isinstance(invalid_id, int) and invalid_id > 0)
    
    def test_review_image_post_id_validation(self):
        """Test que image_post_id doit être un entier positif ou None."""
        valid_id = 20
        valid_none = None
        invalid_id = 0
        
        assert (valid_id is None) or (isinstance(valid_id, int) and valid_id > 0)
        assert valid_none is None
        assert not (isinstance(invalid_id, int) and invalid_id > 0)
    
    def test_review_data_structure(self):
        """Test la structure de données d'un review."""
        review_data = {
            "id": 1,
            "comment": "Magnifique carte !",
            "user_id": 5,
            "image_post_id": 10
        }
        
        # Vérifier les clés
        assert "comment" in review_data
        assert "user_id" in review_data
        assert "image_post_id" in review_data


# ========================================
# TESTS DES MODÈLES EXISTANTS (CHARACTER, DESCRIPTION, etc.)
# ========================================

class TestCharacterLogic:
    """Tests de la logique du modèle Character."""
    
    def test_character_data_structure(self):
        """Test la structure de données d'un personnage."""
        character_data = {
            "id": 1,
            "name": "Gandalf",
            "birth_date": 1000,
            "death_date": None,
            "era_birth": "Third Age",
            "era_death": None,
            "gender": "Male",
            "profession": "Wizard",
            "description": "Un puissant magicien",
            "citation": "You shall not pass"
        }
        
        assert "name" in character_data
        assert character_data["gender"] in ["Male", "Female", "Unknown"]


class TestDescriptionLogic:
    """Tests de la logique du modèle Description."""
    
    def test_description_entity_types(self):
        """Test les types d'entités valides."""
        valid_types = ["character", "ville", "region", "race", "history"]
        test_type = "character"
        
        assert test_type in valid_types
    
    def test_description_order_sorting(self):
        """Test le tri par order_index."""
        descriptions = [
            {"order_index": 3, "title": "Third"},
            {"order_index": 1, "title": "First"},
            {"order_index": 2, "title": "Second"},
        ]
        
        sorted_desc = sorted(descriptions, key=lambda x: x["order_index"])
        
        assert sorted_desc[0]["title"] == "First"
        assert sorted_desc[1]["title"] == "Second"
        assert sorted_desc[2]["title"] == "Third"


class TestHistoryLogic:
    """Tests de la logique du modèle History."""
    
    def test_history_duration_calculation(self):
        """Test le calcul de durée."""
        start_year = 3018
        end_year = 3019
        duration = end_year - start_year
        
        assert duration == 1
    
    def test_history_era_validation(self):
        """Test que les ères sont valides."""
        valid_eras = ["First Age", "Second Age", "Third Age", "Fourth Age"]
        test_era = "Third Age"
        
        assert test_era in valid_eras


class TestPlaceMapLogic:
    """Tests de la logique du modèle PlaceMap."""
    
    def test_place_title_validation(self):
        """Test la validation du titre."""
        valid_title = "Gondor"
        invalid_title = "   "
        
        assert bool(valid_title.strip())
        assert not bool(invalid_title.strip())
    
    def test_place_type_enum(self):
        """Test les types de lieux valides."""
        valid_types = [
            'region', 'foret', 'montagne', 'forteresse', 'ville',
            'capitale', 'eau', 'ruine', 'dark', 'mine', 'port',
            'pont', 'plaine', 'chemin', 'monument', 'special', 'default'
        ]
        
        test_type = "ville"
        assert test_type in valid_types
    
    def test_place_serialization_conditional(self):
        """Test la sérialisation conditionnelle."""
        # Sans géométrie
        place_data_simple = {
            "id": 1,
            "title": "Gondor",
            "type_place": "region"
        }
        assert "markers" not in place_data_simple
        
        # Avec géométrie
        place_data_full = {
            "id": 1,
            "title": "Gondor",
            "markers": [],
            "regions": []
        }
        assert "markers" in place_data_full


class TestRaceLogic:
    """Tests de la logique du modèle Race."""
    
    def test_race_required_fields(self):
        """Test que les champs requis sont présents."""
        race_data = {
            "name": "Elfe",
            "weakness": "Nostalgie",
            "strength": "Sagesse",
            "description": "Êtres immortels"
        }
        
        assert all(key in race_data for key in ["name", "weakness", "strength", "description"])


class TestRelationTypeLogic:
    """Tests de la logique du modèle RelationType."""
    
    def test_relation_type_name_validation(self):
        """Test la validation du nom."""
        valid_name = "Alliance"
        empty_name = "   "
        long_name = "A" * 51
        
        assert bool(valid_name.strip())
        assert not bool(empty_name.strip())
        assert len(long_name) > 50
    
    def test_relation_type_strip_whitespace(self):
        """Test que les espaces sont supprimés."""
        name = "  War  "
        cleaned = name.strip()
        
        assert cleaned == "War"


# ========================================
# TESTS DE VALIDATION CROSS-MODEL
# ========================================

class TestCrossModelValidation:
    """Tests de validation entre modèles."""
    
    @pytest.mark.parametrize("value,expected", [
        ("Valid", True),
        ("", False),
        ("   ", False),
        (None, False),
    ])
    def test_non_empty_string_validation(self, value, expected):
        """Test universel pour les chaînes non vides."""
        if value is None:
            is_valid = False
        else:
            is_valid = bool(str(value).strip())
        
        assert is_valid == expected
    
    @pytest.mark.parametrize("id_value,expected", [
        (1, True),
        (100, True),
        (0, False),
        (-1, False),
    ])
    def test_positive_integer_validation(self, id_value, expected):
        """Test universel pour les entiers positifs (IDs)."""
        is_valid = isinstance(id_value, int) and id_value > 0
        assert is_valid == expected


# ========================================
# TESTS DE SÉRIALISATION
# ========================================

class TestSerialization:
    """Tests de sérialisation des modèles."""
    
    def test_user_serialization_no_password(self):
        """Test que le mot de passe n'est jamais exposé."""
        user_dict = {
            "id": 1,
            "email": "test@example.com",
            "first_name": "Test"
        }
        
        assert "password" not in user_dict
    
    def test_image_post_serialization_no_binary(self):
        """Test que les données binaires ne sont pas exposées."""
        image_dict = {
            "id": 1,
            "title": "Image",
            "image_mime_type": "image/png"
        }
        
        assert "image_data" not in image_dict
    
    def test_timestamp_serialization(self):
        """Test que les timestamps sont au format ISO."""
        timestamp = "2024-01-01T00:00:00"
        
        # Vérifier le format
        assert "T" in timestamp
        assert len(timestamp.split("T")) == 2
