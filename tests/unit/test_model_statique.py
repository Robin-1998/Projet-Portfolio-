import pytest
from app import db, create_app
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.image_post import ImagePost
from app.models.review import Review
from app.models.character import Character
from app.models.race import Race
from app.models.place_map import PlaceMap
from app.models.map_region import MapRegion
from app.models.map_marker import MapMarker
from app.models.history import History
from shapely.geometry import Point, Polygon
from geoalchemy2.shape import from_shape

try:
    from geoalchemy2.elements import WKTElement
except ImportError:
    WKTElement = None

# ==================== FIXTURES ====================

@pytest.fixture
def history_instance(app):
    """Fixture pour créer une instance History dans le contexte Flask."""
    with app.app_context():
        hist = History(
            name="Guerre de l'Anneau",
            description="Conflit majeur entre les peuples libres et Sauron",
            start_year=3018,
            end_year=3019,
            era="Troisième Âge"
        )
        db.session.add(hist)
        db.session.commit()
        yield hist
        db.session.delete(hist)
        db.session.commit()

@pytest.fixture
def race_instance(app):
    """Fixture pour créer une instance Race."""
    with app.app_context():
        race = Race(
            name="Elfe",
            weakness="Sensibles aux poisons",
            strength="Vision nocturne et agilité",
            description="Peuple ancien et gracieux"
        )
        db.session.add(race)
        db.session.commit()
        yield race
        db.session.delete(race)
        db.session.commit()

@pytest.fixture
def character_for_race(app, race_instance):
    """Fixture pour créer un personnage lié à une race."""
    with app.app_context():
        char = Character(
            name="Legolas",
            birth_date=87,
            death_date=None,
            era_birth="Troisième Âge",
            era_death=None,
            gender="Masculin",
            profession="Archer",
            description="Prince elfe de la Forêt Noire",
            race_id=race_instance.id
        )
        db.session.add(char)
        db.session.commit()
        yield char
        db.session.delete(char)
        db.session.commit()

@pytest.fixture
def character_instance(app, race_instance):
    """Fixture pour créer un personnage complet."""
    with app.app_context():
        char = Character(
            name="Legolas",
            birth_date=87,
            death_date=None,
            era_birth="Troisième Âge",
            era_death=None,
            gender="Masculin",
            profession="Archer",
            description="Prince elfe de la Forêt Noire",
            race_id=race_instance.id
        )
        db.session.add(char)
        db.session.commit()
        yield char
        db.session.delete(char)
        db.session.commit()


@pytest.fixture
def place_region(app):
    """Créer un lieu de type Région."""
    with app.app_context():
        p = PlaceMap(
            title="Rohan",
            type_place="Région",
            description="Grande plaine habitée par les cavaliers du Rohan.",
            parent_id=None
        )
        db.session.add(p)
        db.session.commit()
        place_id = p.id
        yield p
        try:
            db.session.query(PlaceMap).filter_by(id=place_id).delete()
            db.session.commit()
        except:
            db.session.rollback()


@pytest.fixture
def place_village(app, place_region):
    """Créer un lieu de type Village (enfant d'une région)."""
    with app.app_context():
        p = PlaceMap(
            title="Edoras",
            type_place="Village",
            description="Capitale du Rohan, construite sur une colline.",
            parent_id=place_region.id
        )
        db.session.add(p)
        db.session.commit()
        place_id = p.id
        yield p
        try:
            db.session.query(PlaceMap).filter_by(id=place_id).delete()
            db.session.commit()
        except:
            db.session.rollback()


@pytest.fixture
def map_marker(app, place_village):
    """Créer un marqueur (POINT)."""
    if not WKTElement:
        pytest.skip("GeoAlchemy2 non installé.")
    with app.app_context():
        marker = MapMarker(
            name="Théoden",
            location=WKTElement("POINT(12 45)", srid=0),
            place_id=place_village.id
        )
        db.session.add(marker)
        db.session.commit()
        marker_id = marker.id
        yield marker
        try:
            db.session.query(MapMarker).filter_by(id=marker_id).delete()
            db.session.commit()
        except:
            db.session.rollback()


@pytest.fixture
def map_region(app, place_region):
    """Créer une région (POLYGON)."""
    if not WKTElement:
        pytest.skip("GeoAlchemy2 non installé.")
    with app.app_context():
        region = MapRegion(
            name="Frontière du Rohan",
            shape_data=WKTElement("POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))", srid=0),
            place_id=place_region.id
        )
        db.session.add(region)
        db.session.commit()
        region_id = region.id
        yield region
        try:
            db.session.query(MapRegion).filter_by(id=region_id).delete()
            db.session.commit()
        except:
            db.session.rollback()


# ==================== TEST HISTORY ====================

def test_history_creation(app, history_instance):
    """Tester la création et le stockage d'une instance History."""
    with app.app_context():
        assert history_instance.id is not None
        assert history_instance.name == "Guerre de l'Anneau"
        assert history_instance.start_year == 3018
        assert history_instance.era == "Troisième Âge"

def test_history_to_dict(app, history_instance):
    """Tester la méthode to_dict."""
    with app.app_context():
        dict_data = history_instance.to_dict()
        assert dict_data["id"] == history_instance.id
        assert dict_data["name"] == history_instance.name
        assert dict_data["description"] == history_instance.description
        assert dict_data["start_year"] == history_instance.start_year
        assert dict_data["end_year"] == history_instance.end_year
        assert dict_data["era"] == history_instance.era

def test_history_name_description_not_null(app):
    """Tester que name et description ne peuvent pas être nuls."""
    with app.app_context():
        hist = History(name=None, description=None)
        db.session.add(hist)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

# ==================== TESTS RACE ====================

def test_race_creation(app, race_instance):
    """Tester la création et le stockage d'une Race."""
    with app.app_context():
        assert race_instance.id is not None
        assert race_instance.name == "Elfe"
        assert race_instance.weakness == "Sensibles aux poisons"
        assert race_instance.strength == "Vision nocturne et agilité"
        assert race_instance.description == "Peuple ancien et gracieux"

def test_race_to_dict(app, race_instance):
    """Tester la méthode to_dict de Race."""
    with app.app_context():
        data = race_instance.to_dict()
        assert data["id"] == race_instance.id
        assert data["name"] == race_instance.name
        assert data["weakness"] == race_instance.weakness
        assert data["strength"] == race_instance.strength
        assert data["description"] == race_instance.description

def test_race_name_not_null(app):
    """Tester que le nom ne peut pas être nul."""
    with app.app_context():
        race = Race(
            name=None,
            weakness="Aucune",
            strength="Aucune",
            description="Test"
        )
        db.session.add(race)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

def test_race_fields_not_null(app):
    """Tester que weakness, strength et description ne peuvent pas être nuls."""
    with app.app_context():
        race = Race(name="Nain", weakness=None, strength=None, description=None)
        db.session.add(race)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

# ==================== TEST RELATION CHARACTERS ====================

def test_race_characters_relationship(app, race_instance, character_for_race):
    """Tester la relation entre Race et Character."""
    with app.app_context():
        characters = race_instance.characters.all()
        character_ids = [c.id for c in characters]
        assert character_for_race.id in character_ids
        assert character_for_race.race_id == race_instance.id


# ==================== TESTS CHARACTER ====================

def test_character_creation(app, character_instance):
    """Tester la création et le stockage d'une instance Character."""
    with app.app_context():
        assert character_instance.id is not None
        assert character_instance.name == "Legolas"
        assert character_instance.birth_date == 87
        assert character_instance.era_birth == "Troisième Âge"
        assert character_instance.gender == "Masculin"
        assert character_instance.profession == "Archer"
        assert character_instance.description == "Prince elfe de la Forêt Noire"
        assert character_instance.race is not None

def test_character_to_dict(app, character_instance):
    """Tester la méthode to_dict du Character."""
    with app.app_context():
        data = character_instance.to_dict()
        assert data["id"] == character_instance.id
        assert data["name"] == character_instance.name
        assert data["birth_date"] == character_instance.birth_date
        assert data["death_date"] == character_instance.death_date
        assert data["era_birth"] == character_instance.era_birth
        assert data["era_death"] == character_instance.era_death
        assert data["gender"] == character_instance.gender
        assert data["profession"] == character_instance.profession
        assert data["description"] == character_instance.description

def test_character_fields_not_null(app, race_instance):
    """Tester que les champs obligatoires ne peuvent pas être None."""
    with app.app_context():
        char = Character(
            name=None,
            birth_date=None,
            era_birth=None,
            gender=None,
            profession=None,
            description=None,
            race_id=race_instance.id
        )
        db.session.add(char)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

def test_character_race_relationship(app, race_instance, character_instance):
    """Tester que le Character est bien lié à sa Race."""
    with app.app_context():
        characters = race_instance.characters.all()
        character_ids = [c.id for c in characters]
        assert character_instance.id in character_ids
        assert character_instance.race_id == race_instance.id

# ==================== TESTS PLACE_MAP ====================

def test_place_map_creation(place_region):
    """Tester la création d'un lieu valide."""
    assert place_region.id is not None
    assert place_region.title == "Rohan"
    assert place_region.type_place == "Région"
    assert place_region.description.startswith("Grande plaine")
    assert place_region.parent_id is None


def test_place_map_to_dict_basic(place_region):
    """Vérifie le format du dictionnaire sans géométrie."""
    data = place_region.to_dict()
    assert data["title"] == "Rohan"
    assert data["type_place"] == "Région"
    assert data["description"] == "Grande plaine habitée par les cavaliers du Rohan."
    assert "markers" not in data
    assert "regions" not in data


def test_place_map_to_dict_with_geometry(place_region, map_region):
    """Vérifie que les markers et regions sont inclus si demandé."""
    data = place_region.to_dict(include_geometry=True)
    assert "regions" in data
    assert isinstance(data["regions"], list)
    assert data["regions"][0]["geometry"]["type"] == "Polygon"


def test_place_map_invalid_type(app):
    """type_place invalide doit lever une exception SQLAlchemy."""
    with app.app_context():
        with pytest.raises(Exception):
            invalid_place = PlaceMap(
                title="Endor",
                type_place="Planète",
                description="Type inconnu dans l'enum",
                parent_id=None
            )
            db.session.add(invalid_place)
            db.session.commit()
        db.session.rollback()


def test_place_map_empty_fields(app):
    """Titre ou description vide doit lever une erreur."""
    with app.app_context():
        with pytest.raises(Exception):
            PlaceMap(title="", type_place="Région", description="test", parent_id=None)
        with pytest.raises(Exception):
            PlaceMap(title="Test", type_place="Région", description="", parent_id=None)


def test_place_map_hierarchy(place_region, place_village):
    """Vérifie la relation parent/enfant."""
    assert place_village.parent_id == place_region.id
    # Comparer par ID au lieu de comparer les objets
    children_ids = [c.id for c in place_region.children]
    assert place_village.id in children_ids


# ==================== TESTS MAP_MARKER ====================

def test_map_marker_creation(map_marker, place_village):
    """Créer un marqueur valide."""
    assert map_marker.id is not None
    assert map_marker.name == "Théoden"
    assert map_marker.place_id == place_village.id


def test_map_marker_to_dict(map_marker):
    """Vérifie la sérialisation en dictionnaire."""
    data = map_marker.to_dict()
    assert data["geometry"]["type"] == "Point"
    assert isinstance(data["geometry"]["coordinates"], list)
    assert "name" in data and data["name"] == "Théoden"


def test_map_marker_invalid_location(app, place_village):
    """Location invalide doit lever une erreur."""
    with app.app_context():
        with pytest.raises(Exception):
            MapMarker(name="Test", location="not_geom", place_id=place_village.id)


def test_map_marker_missing_name(app, place_village):
    """Nom vide ou None doit lever une erreur."""
    if not WKTElement:
        pytest.skip("GeoAlchemy2 non installé.")
    with app.app_context():
        with pytest.raises(Exception):
            MapMarker(name="", location=WKTElement("POINT(1 1)", srid=0), place_id=place_village.id)


# ==================== TESTS MAP_REGION ====================

def test_map_region_creation(map_region, place_region):
    """Créer une région valide."""
    assert map_region.id is not None
    assert map_region.name == "Frontière du Rohan"
    assert map_region.place_id == place_region.id


def test_map_region_to_dict(map_region):
    """Vérifie la sérialisation en dictionnaire."""
    data = map_region.to_dict()
    assert data["geometry"]["type"] == "Polygon"
    assert isinstance(data["geometry"]["coordinates"], list)
    assert len(data["geometry"]["coordinates"]) >= 3


def test_map_region_invalid_shape(app, place_region):
    """Shape non géométrique doit lever une erreur."""
    with app.app_context():
        with pytest.raises(Exception):
            MapRegion(name="Test", shape_data="not_polygon", place_id=place_region.id)


def test_map_region_missing_name(app, place_region):
    """Nom vide doit lever une erreur."""
    if not WKTElement:
        pytest.skip("GeoAlchemy2 non installé.")
    with app.app_context():
        with pytest.raises(Exception):
            MapRegion(
                name="",
                shape_data=WKTElement("POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))", srid=0),
                place_id=place_region.id
            )


# ==================== TEST RELATIONS ====================

def test_place_map_relationships(place_region, map_region, place_village, map_marker):
    """Vérifie les relations entre PlaceMap, MapMarker et MapRegion."""
    # Comparer par ID au lieu de comparer les objets
    assert map_region.place_id == place_region.id
    assert map_marker.place_id == place_village.id

    # Ou vérifier les IDs dans les listes
    region_ids = [r.id for r in place_region.map_regions]
    assert map_region.id in region_ids

    marker_ids = [m.id for m in place_village.map_markers]
    assert map_marker.id in marker_ids

# ==================== TEST SEARCH ====================

def test_search_without_query(client, mocker):
    """Test route /search sans query param → doit renvoyer 400"""
    from app.api.V1 import api_search
    mocker.patch.object(api_search.facade, "search_all", side_effect=ValueError("Aucun terme de recherche fourni"))

    response = client.get("/api/v1/search")  # pas de q
    assert response.status_code == 400
    assert b"Aucun terme de recherche fourni" in response.data

def test_search_with_empty_query(client, mocker):
    """Test route /search avec q vide → doit renvoyer 400"""
    from app.api.V1 import api_search
    mocker.patch.object(api_search.facade, "search_all", side_effect=ValueError("Aucun terme de recherche fourni"))

    response = client.get("/api/v1/search?q=")
    assert response.status_code == 400
    assert b"Aucun terme de recherche fourni" in response.data
