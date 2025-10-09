import pytest
from app import db
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

# Ces modèles n'existent pas encore dans vos fichiers
# from app.models.relation_type import RelationType
# from app.models.character_history import CharacterHistory
# from app.models.character_place import CharacterPlace
# from app.models.entity_description import EntityDescription

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
        # Vérifier que le race_id du personnage correspond bien
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
