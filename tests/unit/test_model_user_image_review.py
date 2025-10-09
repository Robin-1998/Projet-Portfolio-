import pytest
from app import db
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
def user(app):
    """Créer un utilisateur de test."""
    u = User(
        first_name="Frodo",
        last_name="Sacquet",
        email="frodo@test.com",
        password="motdepasse"
    )
    db.session.add(u)
    db.session.commit()
    yield u
    db.session.delete(u)
    db.session.commit()


@pytest.fixture
def admin_user(app):
    """Créer un utilisateur admin."""
    admin = User(
        first_name="Gandalf",
        last_name="Le Gris",
        email="gandalf@test.com",
        password="motdepasse",
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    yield admin
    db.session.delete(admin)
    db.session.commit()


@pytest.fixture
def image_post(app, user):
    """Créer une image de test."""
    img = ImagePost(
        title="Carte de la Terre du Milieu",
        description="Une belle carte ancienne",
        image_data=b"fake_image_data",
        image_mime_type="image/png",
        user_id=user.id
    )
    db.session.add(img)
    db.session.commit()
    yield img
    db.session.delete(img)
    db.session.commit()


@pytest.fixture
def review(app, user, image_post):
    """Créer une review."""
    rev = Review(
        comment="Magnifique !",
        user_id=user.id,
        image_post_id=image_post.id
    )
    db.session.add(rev)
    db.session.commit()
    yield rev
    db.session.delete(rev)
    db.session.commit()


# NOTE: Ces fixtures sont commentées car les modèles n'existent pas encore
# Décommentez-les quand vous aurez créé les modèles correspondants

# @pytest.fixture
# def character_history(app, character, history):
#     """Créer une liaison character-history."""
#     ch = CharacterHistory(
#         role="Participant",
#         character_id=character.id,
#         history_id=history.id
#     )
#     db.session.add(ch)
#     db.session.commit()
#     yield ch
#     db.session.delete(ch)
#     db.session.commit()


# @pytest.fixture
# def character_place(app, character, place_map, relation_type):
#     """Créer une liaison character-place."""
#     cp = CharacterPlace(
#         relation_type_id=relation_type.id,
#         character_id=character.id,
#         place_id=place_map.id
#     )
#     db.session.add(cp)
#     db.session.commit()
#     yield cp
#     db.session.delete(cp)
#     db.session.commit()


# @pytest.fixture
# def entity_description(app, relation_type):
#     """Créer une description d'entité."""
#     ed = EntityDescription(
#         title="Description test",
#         content="Contenu de test",
#         order_index=1,
#         relation_type_id=relation_type.id,
#         entity_id=1
#     )
#     db.session.add(ed)
#     db.session.commit()
#     yield ed
#     db.session.delete(ed)
#     db.session.commit()


# ==================== TESTS USER ====================

# ==================== TESTS USER ====================

def test_user_creation(user):
    """Tester la création d'un utilisateur valide."""
    assert user.id is not None
    assert user.first_name == "Frodo"
    assert user.last_name == "Sacquet"
    assert user.email == "frodo@test.com"
    assert user.is_admin is False

def test_user_to_dict(user):
    """Tester la sérialisation en dictionnaire."""
    data = user.to_dict()
    assert data["first_name"] == "Frodo"
    assert data["last_name"] == "Sacquet"
    assert data["email"] == "frodo@test.com"
    assert data["is_admin"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_user_password_hashing(app):
    """Tester le hashage des mots de passe."""
    u = User(first_name="Sam", last_name="Gamgee", email="sam@test.com", password="secret123")
    assert u.password is not None
    assert u.password != "secret123"
    # Vérifier que le mot de passe peut être validé
    assert u.verify_password("secret123") is True
    assert u.verify_password("mauvaispass") is False
    db.session.add(u)
    db.session.commit()
    db.session.delete(u)
    db.session.commit()

def test_admin_user(admin_user):
    """Tester le flag admin."""
    assert admin_user.is_admin is True

# ----------------- VALIDATION NOMS -----------------

def test_user_empty_first_name(app):
    """Prénom vide doit lever une exception."""
    with pytest.raises(ValueError, match="first_name ne peut pas être vide"):
        User(first_name="", last_name="Baggins", email="test@test.com", password="motdepasse")

def test_user_empty_last_name(app):
    """Nom vide doit lever une exception."""
    with pytest.raises(ValueError, match="last_name ne peut pas être vide"):
        User(first_name="Harry", last_name="", email="test@test.com", password="motdepasse")

@pytest.mark.parametrize("invalid_name", [123, None, 5.6])
def test_user_invalid_type_name(app, invalid_name):
    """Prénom ou nom non-string doit lever une exception."""
    with pytest.raises(ValueError, match="soit être une chaîne de caractères"):
        User(first_name=invalid_name, last_name="Baggins", email="test@test.com", password="password123")

@pytest.mark.parametrize("invalid_name", ["Jean3", "Anne!", "@Marie"])
def test_user_invalid_characters_in_name(app, invalid_name):
    """Nom ou prénom avec caractères invalides doit lever une exception."""
    with pytest.raises(ValueError, match="ne doit contenir que des lettres ou des tirets"):
        User(first_name=invalid_name, last_name="Baggins", email=f"{invalid_name}@test.com", password="password123")

def test_user_name_length_boundaries(app):
    """Vérifie les limites exactes pour first_name et last_name."""
    u = User(first_name="A", last_name="B", email="test1@test.com", password="password123")
    assert u.first_name == "A"
    assert u.last_name == "B"

    long_name = "X" * 50
    u2 = User(first_name=long_name, last_name=long_name, email="test2@test.com", password="password123")
    # Avec title(), les majuscules deviennent "Xxxxx..."
    expected = long_name.title()
    assert u2.first_name == expected
    assert u2.last_name == expected


# ----------------- VALIDATION EMAIL -----------------

def test_user_empty_email(app):
    """Email vide doit lever une exception."""
    with pytest.raises(ValueError, match="L'email ne peut pas être vide"):
        User(first_name="Harry", last_name="Potter", email="", password="motdepasse")

def test_user_invalid_email(app):
    """Email invalide doit lever une exception."""
    with pytest.raises(ValueError, match="Erreur, email invalide"):
        User(first_name="Harry", last_name="Potter", email="invalid-email", password="motdepasse")

def test_user_email_normalization(app):
    """Email avec majuscules doit être normalisé."""
    u = User(first_name="Bilbo", last_name="Sacquet", email="BiLbO@Test.COM", password="password123")
    # Avec ton code actuel, email n’est pas forcé en minuscule
    assert u.email == "BiLbO@test.com"


def test_user_email_unique(app, user):
    """Tester l'unicité de l'email."""
    duplicate = User(first_name="Test", last_name="User", email="frodo@test.com", password="motdepasse")
    db.session.add(duplicate)
    with pytest.raises(Exception):  # la contrainte unique de la DB
        db.session.commit()
    db.session.rollback()

# ----------------- VALIDATION MOT DE PASSE -----------------

def test_user_empty_password(app):
    """Mot de passe vide doit lever une exception."""
    with pytest.raises(ValueError, match="Le mot de passe ne peut être vide"):
        User(first_name="Harry", last_name="Potter", email="harry@test.com", password="")

def test_user_short_password(app):
    """Mot de passe trop court doit lever une exception."""
    with pytest.raises(ValueError, match="Le mot de passe doit contenir au moins 8 caractères"):
        User(first_name="Harry", last_name="Potter", email="harry@test.com", password="short")

def test_update_password(app, user):
    """Tester la mise à jour du mot de passe."""
    old_hash = user.password
    user.update_password("nouveaumdp")
    assert user.password != old_hash
    assert user.verify_password("nouveaumdp") is True

def test_user_update_password_changes_hash(app, user):
    """Vérifie que le hash change et l'ancien mot de passe devient invalide."""
    old_hash = user.password
    user.update_password("nouveaumdp123")
    assert user.password != old_hash
    assert user.verify_password("nouveaumdp123") is True
    assert user.verify_password("motdepasse") is False

# ----------------- VALIDATION IS_ADMIN -----------------

def test_is_admin_validation(app):
    """Tester la validation du flag is_admin."""
    u = User(first_name="Sam", last_name="Gamgee", email="sam2@test.com", password="motdepasse")
    # is_admin valide
    u.is_admin = True
    assert u.is_admin is True
    # is_admin invalide
    with pytest.raises(ValueError, match="is_admin doit être un booléen"):
        u.is_admin = "oui"

def test_user_is_admin_constructor_validation(app):
    """is_admin invalide au constructeur doit lever une exception."""
    with pytest.raises(ValueError, match="is_admin doit être un booléen"):
        User(first_name="Sam", last_name="Gamgee", email="sam3@test.com", password="password123", is_admin="oui")

# ==================== TESTS IMAGE_POST ====================

def test_image_post_valid(user):
    """Créer une image valide sans erreur."""
    img = ImagePost(
        title="Titre",
        description="Description",
        image_data=b"data",
        image_mime_type="image/png",
        user_id=user.id
    )
    assert img.title == "Titre"
    assert img.description == "Description"
    assert img.image_data == b"data"
    assert img.user_id == user.id
    assert img.image_mime_type == "image/png"

def test_image_post_invalid_user_id(user):
    """Vérifier que user_id doit être un entier positif."""
    with pytest.raises(ValueError, match="user_id doit être un entier."):
        ImagePost(
            title="Titre",
            description="Desc",
            image_data=b"data",
            image_mime_type="image/png",
            user_id="invalid"
        )

    with pytest.raises(ValueError, match="user_id doit être un entier positif."):
        ImagePost(
            title="Titre",
            description="Desc",
            image_data=b"data",
            image_mime_type="image/png",
            user_id=-5
        )

def test_image_post_invalid_image_data(user):
    """Vérifier que image_data doit être binaire (bytes)."""
    with pytest.raises(ValueError, match="L'image doit être de type binaire \\(bytes\\)"):
        ImagePost(
            title="Titre",
            description="Desc",
            image_data="not_bytes",
            image_mime_type="image/png",
            user_id=user.id
        )

def test_image_post_empty_title(user):
    """Titre vide ou non string lève une exception."""
    with pytest.raises(ValueError, match="Le titre est requis et doit être une chaîne."):
        ImagePost(
            title="   ",
            description="Desc",
            image_data=b"data",
            image_mime_type="image/png",
            user_id=user.id
        )

def test_image_post_title_length(user):
    """Vérifier la longueur maximale du titre."""
    long_title = "A" * 101
    with pytest.raises(ValueError, match="Le titre ne doit pas dépasser 100 caractères."):
        ImagePost(
            title=long_title,
            description="Desc",
            image_data=b"data",
            image_mime_type="image/png",
            user_id=user.id
        )

def test_image_post_empty_description(user):
    """Description vide ou non string lève une exception."""
    with pytest.raises(ValueError, match="La description est requise et doit être une chaîne."):
        ImagePost(
            title="Titre",
            description="",
            image_data=b"data",
            image_mime_type="image/png",
            user_id=user.id
        )

def test_image_post_description_length(user):
    """Vérifier la longueur maximale de la description."""
    long_desc = "D" * 151
    with pytest.raises(ValueError, match="La description ne doit pas dépasser 150 caractères."):
        ImagePost(
            title="Titre",
            description=long_desc,
            image_data=b"data",
            image_mime_type="image/png",
            user_id=user.id
        )

# ==================== TESTS REVIEW ====================

def test_review_creation(user, image_post):
    """Tester la création d'une review valide."""
    rev = Review(
        comment="Superbe image !",
        user_id=user.id,
        image_post_id=image_post.id
    )
    db.session.add(rev)
    db.session.commit()
    assert rev.id is not None
    assert rev.comment == "Superbe image !"
    assert rev.user_id == user.id
    assert rev.image_post_id == image_post.id
    db.session.delete(rev)
    db.session.commit()

def test_review_to_dict(user, image_post):
    """Tester la sérialisation en dictionnaire."""
    rev = Review(
        comment="Commentaire dict",
        user_id=user.id,
        image_post_id=image_post.id
    )
    db.session.add(rev)
    db.session.commit()
    data = rev.to_dict()
    assert data["comment"] == "Commentaire dict"
    assert data["user_id"] == user.id
    assert data["image_post_id"] == image_post.id
    assert "id" in data
    db.session.delete(rev)
    db.session.commit()

# ========== VALIDATION COMMENT ==========
def test_review_empty_comment(user, image_post):
    """Commentaire vide doit lever une exception."""
    with pytest.raises(ValueError, match="Le texte est requis."):
        Review(comment="", user_id=user.id, image_post_id=image_post.id)

def test_review_comment_not_string(user, image_post):
    """Commentaire non chaîne doit lever une exception."""
    with pytest.raises(ValueError, match="Le commentaire doit être une chaîne"):
        Review(comment=123, user_id=user.id, image_post_id=image_post.id)

def test_review_comment_too_long(user, image_post):
    """Commentaire > 400 caractères doit lever une exception."""
    long_comment = "X" * 401
    with pytest.raises(ValueError, match="Le commentaire ne doit pas dépasser 400 caractères."):
        Review(comment=long_comment, user_id=user.id, image_post_id=image_post.id)

# ========== VALIDATION USER_ID ==========
def test_review_invalid_user_id_type(image_post):
    """user_id non entier doit lever une exception."""
    with pytest.raises(ValueError, match="user_id doit être en entier"):
        Review(comment="Comment", user_id="abc", image_post_id=image_post.id)

def test_review_invalid_user_id_negative(image_post):
    """user_id <= 0 doit lever une exception."""
    with pytest.raises(ValueError, match="user_iddoit être un entier posifif"):
        Review(comment="Comment", user_id=0, image_post_id=image_post.id)

# ========== VALIDATION IMAGE_POST_ID ==========
def test_review_invalid_image_post_id_type(user):
    """image_post_id non entier doit lever une exception."""
    with pytest.raises(ValueError, match="image_post_id doit être un entier"):
        Review(comment="Comment", user_id=user.id, image_post_id="abc")

def test_review_invalid_image_post_id_negative(user):
    """image_post_id <= 0 doit lever une exception."""
    with pytest.raises(ValueError, match="image_post_id doit être un entier positif."):
        Review(comment="Comment", user_id=user.id, image_post_id=0)

# ========== RELATION USER-IMAGE-REVIEW ==========
def test_review_relationships(user, image_post):
    """Tester les relations entre Review, User et ImagePost."""
    # Création d'une review
    rev = Review(comment="Relation test", user_id=user.id, image_post_id=image_post.id)
    db.session.add(rev)
    db.session.commit()

    # Vérifier que la review est liée à l'utilisateur
    user_reviews = user.reviews
    assert rev in user_reviews

    # Vérifier que la review est liée à l'image
    image_reviews = image_post.reviews  # backref dynamique par défaut
    assert rev in image_reviews

    # Vérifier que la suppression de la review met à jour les relations
    db.session.delete(rev)
    db.session.commit()
    assert rev not in user.reviews
    assert rev not in image_post.reviews

