import pytest
import base64
from unittest.mock import Mock, MagicMock, patch
from app import create_app, db
from app.services.facade import PortfolioFacade
from app.models.user import User
from app.models.review import Review
from app.models.image_post import ImagePost


@pytest.fixture(scope='function')
def app():
    """Fixture pour créer l'application Flask en mode test"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def facade(app):
    """Fixture pour créer une instance de PortfolioFacade avec contexte"""
    with app.app_context():
        # Mock db.session pour éviter les vraies transactions
        with patch('app.services.facade.db.session.commit'):
            with patch('app.services.facade.db.session.rollback'):
                yield PortfolioFacade()


@pytest.fixture
def mock_user():
    """Fixture pour créer un utilisateur mock"""
    user = Mock()
    user.id = 1
    user.email = "test@example.com"
    user.username = "testuser"
    user.is_admin = False
    user.verify_password = Mock(return_value=True)
    user.update_password = Mock()
    user.to_dict = Mock(return_value={"id": 1, "email": "test@example.com"})
    return user


@pytest.fixture
def mock_review():
    """Fixture pour créer un commentaire mock"""
    review = Mock()
    review.id = 1
    review.comment = "Test comment"
    review.user_id = 1
    review.image_post_id = 1
    review.to_dict = Mock(return_value={"id": 1, "comment": "Test comment"})
    return review


@pytest.fixture
def mock_image_post():
    """Fixture pour créer un post image mock"""
    post = Mock()
    post.id = 1
    post.title = "Test Image"
    post.description = "Test description"
    post.user_id = 1
    post.image_data = b"fake_image_data"
    post.image_mime_type = "image/jpeg"
    post.to_dict = Mock(return_value={"id": 1, "title": "Test Image"})
    return post


# ==================== Tests User ====================

class TestUserOperations:
    """Tests pour les opérations liées aux utilisateurs"""

    def test_create_user_success(self, facade, mock_user):
        """Test création d'utilisateur avec succès"""
        user_data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "password123"
        }

        facade.user_repo.get_user_by_email = Mock(return_value=None)
        facade.user_repo.add = Mock(return_value=mock_user)

        with patch('app.services.facade.User', return_value=mock_user):
            result = facade.create_user(user_data)

        assert result == mock_user
        facade.user_repo.add.assert_called_once()

    def test_create_user_email_exists(self, facade, mock_user):
        """Test création d'utilisateur avec email existant"""
        user_data = {
            "email": "existing@example.com",
            "username": "newuser",
            "password": "password123"
        }

        facade.user_repo.get_user_by_email = Mock(return_value=mock_user)

        with pytest.raises(ValueError, match="existe déjà"):
            facade.create_user(user_data)

    def test_create_user_no_password(self, facade):
        """Test création d'utilisateur sans mot de passe"""
        user_data = {
            "email": "new@example.com",
            "username": "newuser"
        }

        facade.user_repo.get_user_by_email = Mock(return_value=None)

        with pytest.raises(ValueError, match="mot de passe est requis"):
            facade.create_user(user_data)

    def test_login_user_success(self, facade, mock_user):
        """Test connexion utilisateur avec succès"""
        facade.user_repo.get_user_by_email = Mock(return_value=mock_user)

        result = facade.login_user("test@example.com", "password123")

        assert result == mock_user
        mock_user.verify_password.assert_called_once_with("password123")

    def test_login_user_wrong_password(self, facade, mock_user):
        """Test connexion avec mauvais mot de passe"""
        mock_user.verify_password = Mock(return_value=False)
        facade.user_repo.get_user_by_email = Mock(return_value=mock_user)

        with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
            facade.login_user("test@example.com", "wrongpassword")

    def test_login_user_not_found(self, facade):
        """Test connexion avec utilisateur inexistant"""
        facade.user_repo.get_user_by_email = Mock(return_value=None)

        with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
            facade.login_user("notfound@example.com", "password")

    def test_get_users_success(self, facade, mock_user):
        """Test récupération d'un utilisateur par ID"""
        facade.user_repo.get = Mock(return_value=mock_user)

        result = facade.get_users(1)

        assert result == mock_user
        facade.user_repo.get.assert_called_once_with(1)

    def test_get_users_not_found(self, facade):
        """Test récupération d'un utilisateur inexistant"""
        facade.user_repo.get = Mock(return_value=None)

        with pytest.raises(ValueError, match="Aucun utilisateur trouvé"):
            facade.get_users(999)

    def test_get_all_user(self, facade, mock_user):
        """Test récupération de tous les utilisateurs"""
        facade.user_repo.get_all = Mock(return_value=[mock_user, mock_user])

        result = facade.get_all_user()

        assert len(result) == 2
        assert all(isinstance(u, dict) for u in result)

    def test_get_user_by_email_success(self, facade, mock_user):
        """Test recherche utilisateur par email"""
        facade.user_repo.get_user_by_email = Mock(return_value=mock_user)

        result = facade.get_user_by_email("test@example.com")

        assert result == mock_user

    def test_get_user_by_email_not_found(self, facade):
        """Test recherche utilisateur par email inexistant"""
        facade.user_repo.get_user_by_email = Mock(return_value=None)

        with pytest.raises(ValueError, match="Aucun utilisateur trouvé"):
            facade.get_user_by_email("notfound@example.com")

    def test_update_user_success(self, facade, mock_user):
        """Test mise à jour utilisateur avec succès"""
        update_data = {"username": "updated_user"}
        facade.user_repo.get = Mock(return_value=mock_user)
        facade.user_repo.update = Mock()

        result = facade.update_user(1, 1, update_data)

        assert result == mock_user
        facade.user_repo.update.assert_called_once_with(1, update_data)

    def test_update_user_password_blocked(self, facade, mock_user):
        """Test que la mise à jour du mot de passe est bloquée"""
        update_data = {"password": "newpassword"}
        facade.user_repo.get = Mock(return_value=mock_user)

        with pytest.raises(ValueError, match="Impossible de modifier le mot de passe"):
            facade.update_user(1, 1, update_data)

    def test_update_user_permission_denied(self, facade, mock_user):
        """Test mise à jour sans permissions"""
        update_data = {"username": "hacker"}
        target_user = Mock(spec=User)
        target_user.id = 2

        facade.user_repo.get = Mock(side_effect=[target_user, mock_user])

        with pytest.raises(PermissionError, match="Vous ne pouvez modifier"):
            facade.update_user(2, 1, update_data)

    def test_update_user_password_success(self, facade, mock_user):
        """Test changement de mot de passe avec succès"""
        facade.user_repo.get = Mock(return_value=mock_user)

        result = facade.update_user_password(1, "oldpass", "newpass")

        assert result == mock_user
        mock_user.verify_password.assert_called_once_with("oldpass")
        mock_user.update_password.assert_called_once_with("newpass")

    def test_update_user_password_wrong_old(self, facade, mock_user):
        """Test changement de mot de passe avec mauvais ancien mot de passe"""
        mock_user.verify_password = Mock(return_value=False)
        facade.user_repo.get = Mock(return_value=mock_user)

        with pytest.raises(ValueError, match="ancien mot de passe est incorrect"):
            facade.update_user_password(1, "wrongold", "newpass")

    def test_delete_user_success(self, facade, mock_user):
        """Test suppression utilisateur avec succès"""
        facade.user_repo.get = Mock(return_value=mock_user)
        facade.user_repo.delete = Mock()

        result = facade.delete_user(1)

        assert result is True
        facade.user_repo.delete.assert_called_once_with(1)

    def test_delete_user_not_found(self, facade):
        """Test suppression utilisateur inexistant"""
        facade.user_repo.get = Mock(return_value=None)

        with pytest.raises(ValueError, match="Aucun utilisateur trouvé"):
            facade.delete_user(999)


# ==================== Tests Review ====================

class TestReviewOperations:
    """Tests pour les opérations liées aux commentaires"""

    def test_create_review_success(self, facade, mock_user, mock_image_post):
        """Test création de commentaire avec succès"""
        review_data = {
            "user_id": 1,
            "image_post_id": 1,
            "comment": "Great photo!"
        }

        facade.get_user_by_id = Mock(return_value=mock_user)
        facade.get_post_image = Mock(return_value=mock_image_post)
        facade.review_repo.add = Mock()

        with patch('app.services.facade.Review') as MockReview:
            mock_review = Mock()
            MockReview.return_value = mock_review
            result = facade.create_review(review_data)

            assert result == mock_review
            facade.review_repo.add.assert_called_once()

    def test_create_review_missing_user_id(self, facade):
        """Test création de commentaire sans user_id"""
        review_data = {
            "image_post_id": 1,
            "comment": "Great photo!"
        }

        with pytest.raises(ValueError, match="user_id est requis"):
            facade.create_review(review_data)

    def test_create_review_missing_image_id(self, facade):
        """Test création de commentaire sans image_post_id"""
        review_data = {
            "user_id": 1,
            "comment": "Great photo!"
        }

        with pytest.raises(ValueError, match="image_post_id est requis"):
            facade.create_review(review_data)

    def test_get_review_success(self, facade, mock_review):
        """Test récupération d'un commentaire"""
        facade.review_repo.get = Mock(return_value=mock_review)

        result = facade.get_review(1)

        assert result == mock_review

    def test_get_all_reviews(self, facade, mock_review):
        """Test récupération de tous les commentaires"""
        facade.review_repo.get_all = Mock(return_value=[mock_review, mock_review])

        result = facade.get_all_reviews()

        assert len(result) == 2
        assert all(isinstance(r, dict) for r in result)

    def test_get_reviews_by_image(self, facade, mock_review):
        """Test récupération des commentaires par image"""
        facade.review_repo.get_by_image_post_id = Mock(return_value=[mock_review])

        result = facade.get_reviews_by_image(1)

        assert len(result) == 1
        assert result[0] == mock_review

    def test_get_reviews_by_user(self, facade, mock_review):
        """Test récupération des commentaires par utilisateur"""
        facade.review_repo.get_by_user_id = Mock(return_value=[mock_review])

        result = facade.get_reviews_by_user(1)

        assert len(result) == 1
        assert isinstance(result[0], dict)

    def test_update_review_success(self, facade, mock_review):
        """Test mise à jour d'un commentaire"""
        update_data = {"comment": "Updated comment"}
        facade.review_repo.get = Mock(return_value=mock_review)
        facade.review_repo.update = Mock()

        result = facade.update_review(1, update_data)

        assert result == mock_review
        facade.review_repo.update.assert_called_once_with(1, update_data)

    def test_delete_review_success(self, facade, mock_review):
        """Test suppression d'un commentaire"""
        facade.review_repo.get = Mock(return_value=mock_review)
        facade.review_repo.delete = Mock()

        result = facade.delete_review(1)

        assert result is True
        facade.review_repo.delete.assert_called_once_with(1)


# ==================== Tests ImagePost ====================

class TestImagePostOperations:
    """Tests pour les opérations liées aux posts d'images"""

    def test_create_image_post_success(self, facade, mock_user):
        """Test création d'un post image avec succès"""
        image_b64 = base64.b64encode(b"fake_image_data").decode()
        post_data = {
            "user_id": 1,
            "title": "My Photo",
            "description": "A great photo",
            "image_data": image_b64,
            "image_mime_type": "image/jpeg"
        }

        facade.get_user_by_id = Mock(return_value=mock_user)
        facade.image_post_repo.get_by_title_and_user = Mock(return_value=None)
        facade.image_post_repo.add = Mock()

        with patch('app.services.facade.ImagePost') as MockImagePost:
            mock_post = Mock()
            MockImagePost.return_value = mock_post
            result = facade.create_image_post(post_data)

            assert result == mock_post
            facade.image_post_repo.add.assert_called_once()

    def test_create_image_post_missing_user_id(self, facade):
        """Test création post image sans user_id"""
        post_data = {
            "title": "My Photo",
            "image_data": "base64data"
        }

        with pytest.raises(ValueError, match="user_id est requis"):
            facade.create_image_post(post_data)

    def test_create_image_post_duplicate_title(self, facade, mock_user, mock_image_post):
        """Test création post image avec titre existant"""
        image_b64 = base64.b64encode(b"fake_image_data").decode()
        post_data = {
            "user_id": 1,
            "title": "Existing Photo",
            "image_data": image_b64
        }

        facade.get_user_by_id = Mock(return_value=mock_user)
        facade.image_post_repo.get_by_title_and_user = Mock(return_value=mock_image_post)

        with pytest.raises(ValueError, match="Cette image existe déjà"):
            facade.create_image_post(post_data)

    def test_create_image_post_invalid_base64(self, facade, mock_user):
        """Test création post image avec base64 invalide"""
        post_data = {
            "user_id": 1,
            "title": "My Photo",
            "image_data": "not_valid_base64!!!"
        }

        facade.get_user_by_id = Mock(return_value=mock_user)
        facade.image_post_repo.get_by_title_and_user = Mock(return_value=None)

        with pytest.raises(ValueError, match="base64 valide"):
            facade.create_image_post(post_data)

    def test_get_post_image_success(self, facade, mock_image_post):
        """Test récupération d'une image"""
        facade.image_post_repo.get = Mock(return_value=mock_image_post)

        result = facade.get_post_image(1)

        assert result == mock_image_post

    def test_get_all_post_images(self, facade, mock_image_post):
        """Test récupération de toutes les images"""
        facade.image_post_repo.get_all = Mock(return_value=[mock_image_post, mock_image_post])

        result = facade.get_all_post_images()

        assert len(result) == 2

    def test_get_post_images_by_user(self, facade, mock_image_post):
        """Test récupération des images par utilisateur"""
        facade.image_post_repo.get_by_user_id = Mock(return_value=[mock_image_post])

        result = facade.get_post_images_by_user(1)

        assert len(result) == 1

    def test_update_image_post_success(self, facade, mock_image_post):
        """Test mise à jour d'un post image"""
        update_data = {"title": "Updated Title"}
        mock_image_post.user_id = 1

        facade.image_post_repo.get = Mock(return_value=mock_image_post)
        facade.image_post_repo.update = Mock()

        result = facade.update_image_post(1, 1, update_data)

        assert result == mock_image_post
        facade.image_post_repo.update.assert_called_once()

    def test_update_image_post_permission_denied(self, facade, mock_image_post):
        """Test mise à jour post image sans permission"""
        update_data = {"title": "Hacked Title"}
        mock_image_post.user_id = 2

        facade.image_post_repo.get = Mock(return_value=mock_image_post)

        with pytest.raises(PermissionError, match="pas autorisé"):
            facade.update_image_post(1, 1, update_data)

    def test_update_image_post_with_image(self, facade, mock_image_post):
        """Test mise à jour avec nouvelle image"""
        image_b64 = base64.b64encode(b"new_image_data").decode()
        update_data = {
            "title": "Updated Title",
            "image_data": image_b64
        }
        mock_image_post.user_id = 1

        facade.image_post_repo.get = Mock(return_value=mock_image_post)
        facade.image_post_repo.update = Mock()

        result = facade.update_image_post(1, 1, update_data)

        assert result == mock_image_post
        assert isinstance(update_data["image_data"], bytes)

    def test_delete_image_post_success(self, facade, mock_image_post):
        """Test suppression d'un post image"""
        mock_image_post.user_id = 1

        facade.image_post_repo.get = Mock(return_value=mock_image_post)
        facade.image_post_repo.delete = Mock()

        result = facade.delete_image_post(1, 1)

        assert result is True
        facade.image_post_repo.delete.assert_called_once_with(1)

    def test_delete_image_post_permission_denied(self, facade, mock_image_post):
        """Test suppression post image sans permission"""
        mock_image_post.user_id = 2

        facade.image_post_repo.get = Mock(return_value=mock_image_post)

        with pytest.raises(PermissionError, match="pas autorisé"):
            facade.delete_image_post(1, 1)
