import pytest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from shapely.geometry import Point, Polygon

from app.services.facade2 import PortfolioFacade
from app.models.user import User
from app.models.image_post import ImagePost
from app.models.review import Review
from app.models.character import Character
from app.models.race import Race
from app.models.place_map import PlaceMap
from app.models.map_region import MapRegion
from app.models.map_marker import MapMarker
from app.models.history import History

@pytest.fixture
def app():
    """Fixture pour créer une application Flask avec contexte"""
    from app import create_app
    app = create_app('testing')

    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    """Fixture pour la base de données"""
    from app import db as database

    with app.app_context():
        yield database


@pytest.fixture
def sample_race():
    """Fixture pour une race d'exemple"""
    race = Mock()
    race.id = 1
    race.name = "Elfe"
    race.to_dict.return_value = {"id": 1, "name": "Elfe"}
    return race


@pytest.fixture
def sample_character():
    """Fixture pour un personnage d'exemple"""
    character = Mock()
    character.id = 1
    character.name = "Aragorn"
    character.to_dict.return_value = {"id": 1, "name": "Aragorn"}
    return character


@pytest.fixture
def sample_history():
    """Fixture pour une histoire d'exemple"""
    history = Mock()
    history.id = 1
    history.name = "La Quête de l'Anneau"
    history.to_dict.return_value = {"id": 1, "name": "La Quête de l'Anneau"}
    return history


@pytest.fixture
def sample_image_post():
    """Fixture pour un post image d'exemple"""
    image = Mock()
    image.id = 1
    image.title = "Carte de la Terre du Milieu"
    image.to_dict.return_value = {"id": 1, "title": "Carte de la Terre du Milieu"}
    return image


# ======================== TESTS RACES ========================

class TestGetAllRaces:
    def test_get_race_success(self, app, sample_race):
        """Test récupération d'une race par ID"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = sample_race
                result = PortfolioFacade().get_race(1)
                assert result == sample_race
                mock_get.assert_called_once_with(Race, 1)

    def test_get_race_not_found(self, app):
        """Test levée d'exception si race non trouvée"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = None
                with pytest.raises(ValueError, match="Race avec id 1 introuvable"):
                    PortfolioFacade().get_race(1)


class TestGetRace:
    def test_get_race_success(self, app, sample_race):
        """Test récupération d'une race par ID"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = sample_race
                result = PortfolioFacade().get_race(1)
                assert result == sample_race
                mock_get.assert_called_once_with(Race, 1)

    def test_get_race_not_found(self, app):
        """Test levée d'exception si race non trouvée"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = None
                with pytest.raises(ValueError, match="Race avec id 1 introuvable"):
                    PortfolioFacade().get_race(1)

# ======================== TESTS CHARACTERS ========================

class TestGetAllCharacters:
    def test_get_character_success(self, app, sample_character):
        """Test récupération d'un personnage par ID"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = sample_character
                result = PortfolioFacade().get_character(1)
                assert result == sample_character
                mock_get.assert_called_once_with(Character, 1)

    def test_get_character_not_found(self, app):
        """Test levée d'exception si personnage non trouvé"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = None
                with pytest.raises(ValueError, match="Character avec id 1 introuvable"):
                    PortfolioFacade().get_character(1)


class TestGetCharacter:
    def test_get_character_success(self, app, sample_character):
        """Test récupération d'un personnage par ID"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = sample_character
                result = PortfolioFacade().get_character(1)
                assert result == sample_character
                mock_get.assert_called_once_with(Character, 1)

    def test_get_character_not_found(self, app):
        """Test levée d'exception si personnage non trouvé"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = None
                with pytest.raises(ValueError, match="Character avec id 1 introuvable"):
                    PortfolioFacade().get_character(1)


# ======================== TESTS HISTORIES ========================

class TestGetAllHistories:
    def test_get_history_success(self, app, sample_history):
        """Test récupération d'une histoire par ID"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = sample_history
                result = PortfolioFacade().get_history(1)
                assert result == sample_history
                mock_get.assert_called_once_with(History, 1)

    def test_get_history_not_found(self, app):
        """Test levée d'exception si histoire non trouvée"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = None
                with pytest.raises(ValueError, match="History avec id 1 introuvable"):
                    PortfolioFacade().get_history(1)


class TestGetHistory:
    def test_get_history_success(self, app, sample_history):
        """Test récupération d'une histoire par ID"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = sample_history
                result = PortfolioFacade().get_history(1)
                assert result == sample_history
                mock_get.assert_called_once_with(History, 1)

    def test_get_history_not_found(self, app):
        """Test levée d'exception si histoire non trouvée"""
        with app.app_context():
            with patch('app.services.facade2.db.session.get') as mock_get:
                mock_get.return_value = None
                with pytest.raises(ValueError, match="History avec id 1 introuvable"):
                    PortfolioFacade().get_history(1)

# ======================== TESTS SEARCH ========================

class TestSearchAll:
    """Tests pour la méthode search_all de PortfolioFacade"""

    def test_search_without_query(self, client):
        """Test route /search sans query param → doit renvoyer 400"""
        response = client.get("/api/v1/search")  # pas de q
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_search_with_empty_query(self, client):
        """Test route /search avec q vide → doit renvoyer 400"""
        response = client.get("/api/v1/search?q=")  # q vide
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_search_with_valid_query(self, client):
        """Test route /search avec une requête valide"""
        response = client.get("/api/v1/search?q=test")
        assert response.status_code == 200
        data = response.get_json()
        assert "results" in data
        assert "query" in data


# ======================== TESTS PLACES/REGIONS ========================

class TestGetAllRegionsWithHierarchy:
    def test_get_all_regions_success(self, app):
        """Test récupération de toutes les régions avec hiérarchie"""
        with app.app_context():
            mock_place = Mock()
            mock_place.id = 1
            mock_place.title = "Gondor"
            mock_place.type_place = "Région"
            mock_place.description = "Le royaume du Gondor"
            mock_place.children = []
            mock_place.map_regions = []
            mock_place.map_markers = []

            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.join.return_value.filter.return_value.all.return_value = [mock_place]
                with patch.object(PortfolioFacade, '_build_place_hierarchy') as mock_build:
                    mock_build.return_value = {
                        "id": 1,
                        "title": "Gondor",
                        "type_place": "Région",
                        "children": [],
                        "region_shape": None,
                        "marker_location": None
                    }

                    result = PortfolioFacade.get_all_regions_with_hierarchy()
                    assert len(result) == 1
                    assert result[0]["title"] == "Gondor"

    def test_get_all_regions_empty(self, app):
        """Test quand aucune région n'existe"""
        with app.app_context():
            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.join.return_value.filter.return_value.all.return_value = []
                result = PortfolioFacade.get_all_regions_with_hierarchy()
                assert result == []


class TestGetRegionByIdWithHierarchy:
    def test_get_region_by_id_success(self, app):
        """Test récupération d'une région spécifique"""
        with app.app_context():
            mock_region = Mock()
            mock_place = Mock()
            mock_place.id = 1
            mock_place.title = "Gondor"
            mock_place.type_place = "Région"
            mock_place.children = []
            mock_place.map_regions = []
            mock_place.map_markers = []
            mock_region.place = mock_place

            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.options.return_value.filter_by.return_value.first.return_value = mock_region
                with patch.object(PortfolioFacade, '_build_place_hierarchy') as mock_build:
                    mock_build.return_value = {
                        "id": 1,
                        "title": "Gondor",
                        "type_place": "Région",
                        "children": [],
                        "region_shape": None,
                        "marker_location": None
                    }

                    result = PortfolioFacade.get_region_by_id_with_hierarchy(1)
                    assert result["title"] == "Gondor"

    def test_get_region_by_id_not_found(self, app):
        """Test quand la région n'existe pas"""
        with app.app_context():
            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.options.return_value.filter_by.return_value.first.return_value = None
                result = PortfolioFacade.get_region_by_id_with_hierarchy(99)
                assert result is None


class TestGetPlaceById:
    def test_get_place_by_id_success(self, app):
        """Test récupération d'un lieu spécifique"""
        with app.app_context():
            mock_place = Mock()
            mock_place.id = 3
            mock_place.title = "Minas Tirith"
            mock_place.type_place = "Ville"
            mock_place.description = "La capitale du Gondor"
            mock_place.children = []
            mock_place.map_regions = []
            mock_place.map_markers = []

            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.filter_by.return_value.first.return_value = mock_place
                with patch.object(PortfolioFacade, '_build_place_hierarchy') as mock_build:
                    mock_build.return_value = {
                        "id": 3,
                        "title": "Minas Tirith",
                        "type_place": "Ville",
                        "children": [],
                        "region_shape": None,
                        "marker_location": None
                    }

                    result = PortfolioFacade.get_place_by_id(3)
                    assert result["title"] == "Minas Tirith"

    def test_get_place_by_id_not_found(self, app):
        """Test quand le lieu n'existe pas"""
        with app.app_context():
            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.filter_by.return_value.first.return_value = None
                result = PortfolioFacade.get_place_by_id(99)
                assert result is None


class TestBuildPlaceHierarchy:
    def test_build_place_hierarchy_with_marker(self, app):
        """Test construction de hiérarchie avec marqueur"""
        with app.app_context():
            mock_place = Mock()
            mock_place.id = 3
            mock_place.title = "Minas Tirith"
            mock_place.type_place = "Ville"
            mock_place.description = "La capitale"
            mock_place.children = []
            mock_place.map_regions = []

            mock_marker = Mock()
            point = Point(10.5, 20.3)
            mock_marker.location = point
            mock_place.map_markers = [mock_marker]

            with patch('app.services.facade2.to_shape') as mock_to_shape:
                mock_to_shape.return_value = point
                result = PortfolioFacade._build_place_hierarchy(mock_place)

                assert result["title"] == "Minas Tirith"
                assert result["type_place"] == "Ville"
                assert result["marker_location"]["type"] == "Point"
                assert result["marker_location"]["coordinates"] == [10.5, 20.3]

    def test_build_place_hierarchy_with_region(self, app):
        """Test construction de hiérarchie avec région"""
        with app.app_context():
            mock_place = Mock()
            mock_place.id = 1
            mock_place.title = "Gondor"
            mock_place.type_place = "Région"
            mock_place.description = "Le royaume"
            mock_place.children = []
            mock_place.map_markers = []

            mock_region = Mock()
            polygon = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
            mock_region.shape_data = polygon
            mock_place.map_regions = [mock_region]

            with patch('app.services.facade2.to_shape') as mock_to_shape:
                mock_to_shape.return_value = polygon
                result = PortfolioFacade._build_place_hierarchy(mock_place)

                assert result["title"] == "Gondor"
                assert result["region_shape"]["type"] == "Polygon"
                assert len(result["region_shape"]["coordinates"]) == 5

    def test_build_place_hierarchy_with_children(self, app):
        """Test construction de hiérarchie avec enfants"""
        with app.app_context():
            mock_child = Mock()
            mock_child.id = 2
            mock_child.title = "Enfant"
            mock_child.type_place = "Ville"
            mock_child.description = "Une enfant place"
            mock_child.children = []
            mock_child.map_regions = []
            mock_child.map_markers = []

            mock_place = Mock()
            mock_place.id = 1
            mock_place.title = "Parent"
            mock_place.type_place = "Région"
            mock_place.description = "Une place parent"
            mock_place.children = [mock_child]
            mock_place.map_regions = []
            mock_place.map_markers = []

            with patch.object(PortfolioFacade, '_build_place_hierarchy', wraps=PortfolioFacade._build_place_hierarchy):
                result = PortfolioFacade._build_place_hierarchy(mock_place)

                assert result["title"] == "Parent"
                assert len(result["children"]) == 1
                assert result["children"][0]["title"] == "Enfant"


class TestGetMapData:
    def test_get_map_data_success(self, app):
        """Test récupération des données de carte"""
        with app.app_context():
            mock_marker = Mock()
            mock_marker.to_dict.return_value = {"id": 1, "lat": 10.5, "lon": 20.3}

            mock_region = Mock()
            mock_region.to_dict.return_value = {"id": 1, "name": "Gondor"}

            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.all.side_effect = [[mock_marker], [mock_region]]

                result = PortfolioFacade.get_map_data()

                assert len(result["markers"]) == 1
                assert len(result["regions"]) == 1
                assert result["markers"][0]["lat"] == 10.5
                assert result["regions"][0]["name"] == "Gondor"

    def test_get_map_data_empty(self, app):
        """Test récupération de données de carte vide"""
        with app.app_context():
            with patch('app.services.facade2.db.session.query') as mock_query:
                mock_query.return_value.all.side_effect = [[], []]

                result = PortfolioFacade.get_map_data()

                assert result["markers"] == []
                assert result["regions"] == []
