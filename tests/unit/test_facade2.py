"""
Tests unitaires PURS de la Facade en lecture seule
Utilisation des mocks pour simuler les requêtes SQLAlchemy.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch


# ========================================
# TESTS DE GET_DESCRIPTIONS
# ========================================

class TestGetDescriptions:
    """Tests de la méthode get_descriptions."""
    
    @patch('backend.app.services.facade2.Description')
    @patch('backend.app.services.facade2.func')
    def test_get_descriptions_success(self, mock_func, MockDescription):
        """Test la récupération des descriptions pour une entité."""
        # Mock des descriptions
        mock_desc1 = Mock()
        mock_desc1.order_index = 1
        mock_desc2 = Mock()
        mock_desc2.order_index = 2
        
        # Mock de la query chain
        mock_query = Mock()
        mock_filter = Mock()
        mock_order = Mock()
        
        MockDescription.query = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.order_by.return_value = mock_order
        mock_order.all.return_value = [mock_desc1, mock_desc2]
        
        # Mock de func.lower
        mock_func.lower.return_value = Mock()
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_descriptions("character", 1)
        
        assert len(result) == 2
        assert result[0].order_index == 1
        assert result[1].order_index == 2
    
    @patch('backend.app.services.facade2.Description')
    @patch('backend.app.services.facade2.func')
    def test_get_descriptions_empty(self, mock_func, MockDescription):
        """Test quand il n'y a pas de descriptions."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_order = Mock()
        
        MockDescription.query = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.order_by.return_value = mock_order
        mock_order.all.return_value = []
        
        mock_func.lower.return_value = Mock()
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_descriptions("race", 5)
        
        assert result == []
    
    @patch('backend.app.services.facade2.Description')
    @patch('backend.app.services.facade2.func')
    def test_get_descriptions_case_insensitive(self, mock_func, MockDescription):
        """Test que la recherche est insensible à la casse."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_order = Mock()
        
        MockDescription.query = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.order_by.return_value = mock_order
        mock_order.all.return_value = []
        
        mock_func.lower.return_value = Mock()
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        facade.get_descriptions("CHARACTER", 1)
        
        # Vérifier que func.lower a été appelé
        mock_func.lower.assert_called()


# ========================================
# TESTS DE GET_ALL_RACES
# ========================================

class TestGetAllRaces:
    """Tests de la méthode get_all_races."""
    
    @patch('backend.app.services.facade2.Race')
    def test_get_all_races_success(self, MockRace):
        """Test la récupération de toutes les races."""
        mock_races = [Mock(), Mock(), Mock()]
        
        mock_query = Mock()
        MockRace.query = mock_query
        mock_query.all.return_value = mock_races
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_all_races()
        
        assert len(result) == 3
        assert result == mock_races
    
    @patch('backend.app.services.facade2.Race')
    def test_get_all_races_empty(self, MockRace):
        """Test quand il n'y a pas de races."""
        mock_query = Mock()
        MockRace.query = mock_query
        mock_query.all.return_value = []
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_all_races()
        
        assert result == []


# ========================================
# TESTS DE GET_RACE
# ========================================

class TestGetRace:
    """Tests de la méthode get_race."""
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_race_success(self, mock_session):
        """Test la récupération d'une race spécifique."""
        mock_race = Mock()
        mock_race.id = 1
        mock_race.name = "Elfe"
        
        mock_session.get.return_value = mock_race
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_race(1)
        
        assert result == mock_race
        mock_session.get.assert_called_once()
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_race_not_found(self, mock_session):
        """Test quand la race n'existe pas."""
        mock_session.get.return_value = None
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        with pytest.raises(ValueError, match="Race avec id 999 introuvable"):
            facade.get_race(999)


# ========================================
# TESTS DE GET_ALL_CHARACTERS
# ========================================

class TestGetAllCharacters:
    """Tests de la méthode get_all_characters."""
    
    @patch('backend.app.services.facade2.Character')
    def test_get_all_characters_success(self, MockCharacter):
        """Test la récupération de tous les personnages."""
        mock_characters = [Mock(), Mock(), Mock()]
        
        mock_query = Mock()
        MockCharacter.query = mock_query
        mock_query.all.return_value = mock_characters
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_all_characters()
        
        assert len(result) == 3
        assert result == mock_characters
    
    @patch('backend.app.services.facade2.Character')
    def test_get_all_characters_empty(self, MockCharacter):
        """Test quand il n'y a pas de personnages."""
        mock_query = Mock()
        MockCharacter.query = mock_query
        mock_query.all.return_value = []
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_all_characters()
        
        assert result == []


# ========================================
# TESTS DE GET_CHARACTER
# ========================================

class TestGetCharacter:
    """Tests de la méthode get_character."""
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_character_success(self, mock_session):
        """Test la récupération d'un personnage spécifique."""
        mock_character = Mock()
        mock_character.id = 1
        mock_character.name = "Gandalf"
        
        mock_session.get.return_value = mock_character
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_character(1)
        
        assert result == mock_character
        assert result.name == "Gandalf"
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_character_not_found(self, mock_session):
        """Test quand le personnage n'existe pas."""
        mock_session.get.return_value = None
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        with pytest.raises(ValueError, match="Character avec id 999 introuvable"):
            facade.get_character(999)


# ========================================
# TESTS DE GET_ALL_HISTORIES
# ========================================

class TestGetAllHistories:
    """Tests de la méthode get_all_histories."""
    
    @patch('backend.app.services.facade2.History')
    def test_get_all_histories_success(self, MockHistory):
        """Test la récupération de toutes les histoires."""
        mock_histories = [Mock(), Mock()]
        
        mock_query = Mock()
        MockHistory.query = mock_query
        mock_query.all.return_value = mock_histories
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_all_histories()
        
        assert len(result) == 2
        assert result == mock_histories


# ========================================
# TESTS DE GET_HISTORY
# ========================================

class TestGetHistory:
    """Tests de la méthode get_history."""
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_history_success(self, mock_session):
        """Test la récupération d'une histoire spécifique."""
        mock_history = Mock()
        mock_history.id = 1
        mock_history.name = "La Guerre de l'Anneau"
        
        mock_session.get.return_value = mock_history
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        result = facade.get_history(1)
        
        assert result == mock_history
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_history_not_found(self, mock_session):
        """Test quand l'histoire n'existe pas."""
        mock_session.get.return_value = None
        
        from backend.app.services.facade2 import PortfolioFacade
        facade = PortfolioFacade()
        
        with pytest.raises(ValueError, match="History avec id 999 introuvable"):
            facade.get_history(999)


# ========================================
# TESTS DE GET_MAP_DATA
# ========================================

class TestGetMapData:
    """Tests de la méthode get_map_data."""
    
    @patch('backend.app.services.facade2.db.session')
    @patch('backend.app.services.facade2.joinedload')
    @patch('backend.app.services.facade2.to_shape')
    def test_get_map_data_success(self, mock_to_shape, mock_joinedload, mock_session):
        """Test la récupération des données de carte."""
        # Mock d'un marker
        mock_marker = Mock()
        mock_marker.id = 1
        mock_marker.place_id = 10
        mock_marker.type.value = "ville"
        mock_marker.place = Mock()
        mock_marker.place.title = "Hobbiton"
        mock_marker.place.description = "Village des Hobbits"
        
        # Mock de la géométrie
        mock_marker_geom = Mock()
        mock_marker_geom.x = 1.5
        mock_marker_geom.y = 2.5
        
        # Mock d'une région
        mock_region = Mock()
        mock_region.id = 2
        mock_region.place_id = 20
        mock_region.place = Mock()
        mock_region.place.title = "La Comté"
        mock_region.place.description = "Terre des Hobbits"
        
        # Mock de la géométrie de région
        mock_region_geom = Mock()
        mock_region_geom.exterior.coords = [(0, 0), (0, 5), (5, 5), (5, 0), (0, 0)]
        
        # Configuration du mock to_shape
        mock_to_shape.side_effect = [mock_marker_geom, mock_region_geom]
        
        # Configuration des queries
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.all.side_effect = [[mock_marker], [mock_region]]
        
        from backend.app.services.facade2 import PortfolioFacade
        
        result = PortfolioFacade.get_map_data()
        
        # Vérifications
        assert "markers" in result
        assert "regions" in result
        assert len(result["markers"]) == 1
        assert len(result["regions"]) == 1
        
        # Vérifier le marker
        marker_data = result["markers"][0]
        assert marker_data["name"] == "Hobbiton"
        assert marker_data["description"] == "Village des Hobbits"
        assert marker_data["type"] == "ville"
        assert marker_data["geometry"]["coordinates"] == [1.5, 2.5]
        
        # Vérifier la région
        region_data = result["regions"][0]
        assert region_data["name"] == "La Comté"
        assert region_data["description"] == "Terre des Hobbits"
    
    @patch('backend.app.services.facade2.db.session')
    @patch('backend.app.services.facade2.joinedload')
    @patch('backend.app.services.facade2.to_shape')
    def test_get_map_data_marker_without_place(self, mock_to_shape, mock_joinedload, mock_session):
        """Test avec un marker sans place associé."""
        # Mock d'un marker sans place
        mock_marker = Mock()
        mock_marker.id = 5
        mock_marker.place_id = None
        mock_marker.place = None
        mock_marker.type = None
        
        mock_marker_geom = Mock()
        mock_marker_geom.x = 3.0
        mock_marker_geom.y = 4.0
        
        mock_to_shape.return_value = mock_marker_geom
        
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.all.side_effect = [[mock_marker], []]
        
        from backend.app.services.facade2 import PortfolioFacade
        
        result = PortfolioFacade.get_map_data()
        
        marker_data = result["markers"][0]
        assert marker_data["name"] == "Marker 5"
        assert marker_data["description"] == "Aucune description disponible"
        assert marker_data["type"] == "default"
    
    @patch('backend.app.services.facade2.db.session')
    @patch('backend.app.services.facade2.joinedload')
    def test_get_map_data_empty(self, mock_joinedload, mock_session):
        """Test quand il n'y a ni markers ni régions."""
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.all.side_effect = [[], []]
        
        from backend.app.services.facade2 import PortfolioFacade
        
        result = PortfolioFacade.get_map_data()
        
        assert result["markers"] == []
        assert result["regions"] == []


# ========================================
# TESTS DE GET_PLACE_DETAILED_INFO
# ========================================

class TestGetPlaceDetailedInfo:
    """Tests de la méthode get_place_detailed_info."""
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_place_detailed_info_success(self, mock_session):
        """Test la récupération d'un lieu avec descriptions."""
        # Mock du lieu
        mock_place = Mock()
        mock_place.id = 1
        mock_place.to_dict.return_value = {
            "id": 1,
            "title": "Fondcombe",
            "description": "Refuge elfique"
        }
        
        # Mock des descriptions
        mock_desc1 = Mock()
        mock_desc1.to_dict.return_value = {
            "id": 10,
            "title": "Histoire",
            "content": "Fondé par Elrond"
        }
        mock_desc2 = Mock()
        mock_desc2.to_dict.return_value = {
            "id": 11,
            "title": "Architecture",
            "content": "Bâtiments elfiques"
        }
        
        # Mock des queries
        mock_place_query = Mock()
        mock_place_query.filter_by.return_value = mock_place_query
        mock_place_query.first.return_value = mock_place
        
        mock_desc_query = Mock()
        mock_desc_query.filter_by.return_value = mock_desc_query
        mock_desc_query.order_by.return_value = mock_desc_query
        mock_desc_query.all.return_value = [mock_desc1, mock_desc2]
        
        mock_session.query.side_effect = [mock_place_query, mock_desc_query]
        
        from backend.app.services.facade2 import PortfolioFacade
        
        result = PortfolioFacade.get_place_detailed_info(1)
        
        # Vérifications
        assert result is not None
        assert result["id"] == 1
        assert result["title"] == "Fondcombe"
        assert "detailed_sections" in result
        assert len(result["detailed_sections"]) == 2
        assert result["detailed_sections"][0]["title"] == "Histoire"
        assert result["detailed_sections"][1]["title"] == "Architecture"
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_place_detailed_info_not_found(self, mock_session):
        """Test quand le lieu n'existe pas."""
        mock_place_query = Mock()
        mock_place_query.filter_by.return_value = mock_place_query
        mock_place_query.first.return_value = None
        
        mock_session.query.return_value = mock_place_query
        
        from backend.app.services.facade2 import PortfolioFacade
        
        result = PortfolioFacade.get_place_detailed_info(999)
        
        assert result is None
    
    @patch('backend.app.services.facade2.db.session')
    def test_get_place_detailed_info_without_descriptions(self, mock_session):
        """Test un lieu sans descriptions détaillées."""
        mock_place = Mock()
        mock_place.id = 1
        mock_place.to_dict.return_value = {
            "id": 1,
            "title": "Moria"
        }
        
        mock_place_query = Mock()
        mock_place_query.filter_by.return_value = mock_place_query
        mock_place_query.first.return_value = mock_place
        
        mock_desc_query = Mock()
        mock_desc_query.filter_by.return_value = mock_desc_query
        mock_desc_query.order_by.return_value = mock_desc_query
        mock_desc_query.all.return_value = []
        
        mock_session.query.side_effect = [mock_place_query, mock_desc_query]
        
        from backend.app.services.facade2 import PortfolioFacade
        
        result = PortfolioFacade.get_place_detailed_info(1)
        
        assert result["title"] == "Moria"
        assert result["detailed_sections"] == []


# ========================================
# TESTS DE LOGIQUE MÉTIER
# ========================================

class TestFacadeLogic:
    """Tests de la logique générale de la facade."""
    
    def test_facade_instantiation(self):
        """Test que la facade peut être instanciée."""
        from backend.app.services.facade2 import PortfolioFacade
        
        facade = PortfolioFacade()
        assert facade is not None
    
    def test_static_methods_callable(self):
        """Test que les méthodes statiques sont appelables."""
        from backend.app.services.facade2 import PortfolioFacade
        
        # Vérifier que les méthodes statiques existent
        assert hasattr(PortfolioFacade, 'get_map_data')
        assert hasattr(PortfolioFacade, 'get_place_detailed_info')
        
        # Vérifier qu'elles sont statiques
        assert isinstance(PortfolioFacade.__dict__['get_map_data'], staticmethod)
        assert isinstance(PortfolioFacade.__dict__['get_place_detailed_info'], staticmethod)
