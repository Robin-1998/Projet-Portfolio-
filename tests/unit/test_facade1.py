"""
Tests unitaires PURS de la Facade
Utilisation des mocks pour simuler les repositories.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import base64


# ========================================
# TESTS DE CREATE_USER
# ========================================

class TestCreateUser:
    """Tests de la méthode create_user."""
    
    def test_create_user_success(self):
        """Test la création réussie d'un utilisateur."""
        mock_user_repo = Mock()
        mock_user_repo.get_user_by_email.return_value = None
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        user_data = {
            "first_name": "Gandalf",
            "last_name": "Le Gris",
            "email": "gandalf@middle-earth.com",
            "password": "password123"
        }
        
        with patch('backend.app.services.facade.User') as MockUser:
            mock_user_instance = Mock()
            MockUser.return_value = mock_user_instance
            
            result = facade.create_user(user_data)
            
            mock_user_repo.get_user_by_email.assert_called_once_with("gandalf@middle-earth.com")
            mock_user_repo.add.assert_called_once_with(mock_user_instance)
            assert result == mock_user_instance
    
    @patch('backend.app.services.facade.db.session')
    def test_create_user_email_already_exists(self, mock_session):
        """Test qu'on ne peut pas créer un utilisateur avec un email existant."""
        mock_user_repo = Mock()
        existing_user = Mock()
        mock_user_repo.get_user_by_email.return_value = existing_user
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        user_data = {
            "email": "existing@example.com",
            "password": "password123"
        }
        
        with pytest.raises(ValueError, match="existe déjà"):
            facade.create_user(user_data)
        
        mock_session.rollback.assert_called_once()
    
    @patch('backend.app.services.facade.db.session')
    def test_create_user_missing_password(self, mock_session):
        """Test qu'un mot de passe est requis."""
        mock_user_repo = Mock()
        mock_user_repo.get_user_by_email.return_value = None
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        user_data = {
            "email": "test@example.com"
        }
        
        with pytest.raises(ValueError, match="mot de passe est requis"):
            facade.create_user(user_data)
        
        mock_session.rollback.assert_called_once()


# ========================================
# TESTS DE LOGIN_USER
# ========================================

class TestLoginUser:
    """Tests de la méthode login_user."""
    
    def test_login_success(self):
        """Test une connexion réussie."""
        mock_user = Mock()
        mock_user.verify_password.return_value = True
        
        mock_user_repo = Mock()
        mock_user_repo.get_user_by_email.return_value = mock_user
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        result = facade.login_user("test@example.com", "password123")
        
        assert result == mock_user
        mock_user.verify_password.assert_called_once_with("password123")
    
    def test_login_missing_credentials(self):
        """Test qu'email et mot de passe sont requis."""
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        
        with pytest.raises(ValueError, match="Email et mot de passe sont requis"):
            facade.login_user("", "password")
        
        with pytest.raises(ValueError, match="Email et mot de passe sont requis"):
            facade.login_user("email@test.com", "")
    
    def test_login_user_not_found(self):
        """Test avec un email inexistant."""
        mock_user_repo = Mock()
        mock_user_repo.get_user_by_email.return_value = None
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
            facade.login_user("unknown@example.com", "password123")
    
    def test_login_wrong_password(self):
        """Test avec un mauvais mot de passe."""
        mock_user = Mock()
        mock_user.verify_password.return_value = False
        
        mock_user_repo = Mock()
        mock_user_repo.get_user_by_email.return_value = mock_user
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
            facade.login_user("test@example.com", "wrongpassword")


# ========================================
# TESTS DE UPDATE_USER
# ========================================

class TestUpdateUser:
    """Tests de la méthode update_user."""
    
    def test_update_user_success(self):
        """Test la mise à jour réussie d'un utilisateur."""
        mock_user = Mock()
        mock_user.id = 1
        mock_user.is_admin = False
        
        mock_current_user = Mock()
        mock_current_user.id = 1
        mock_current_user.is_admin = False
        
        mock_user_repo = Mock()
        mock_user_repo.get.side_effect = [mock_user, mock_current_user, mock_user]
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        update_data = {"first_name": "Updated"}
        
        result = facade.update_user(1, 1, update_data)
        
        mock_user_repo.update.assert_called_once_with(1, update_data)
        assert result == mock_user
    
    @patch('backend.app.services.facade.db.session')
    def test_update_user_cannot_modify_password(self, mock_session):
        """Test qu'on ne peut pas modifier le mot de passe via update_user."""
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        
        update_data = {"password": "newpassword"}
        
        with pytest.raises(ValueError, match="Impossible de modifier le mot de passe"):
            facade.update_user(1, 1, update_data)
        
        mock_session.rollback.assert_called_once()
    
    @patch('backend.app.services.facade.db.session')
    def test_update_user_permission_denied(self, mock_session):
        """Test qu'un utilisateur ne peut modifier que son propre profil."""
        mock_user = Mock()
        mock_user.id = 2
        
        mock_current_user = Mock()
        mock_current_user.id = 1
        mock_current_user.is_admin = False
        
        mock_user_repo = Mock()
        mock_user_repo.get.side_effect = [mock_user, mock_current_user]
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        with pytest.raises(PermissionError, match="Vous ne pouvez modifier que votre propre profil"):
            facade.update_user(2, 1, {"first_name": "Test"})
        
        mock_session.rollback.assert_called_once()
    
    def test_update_user_admin_can_modify_others(self):
        """Test qu'un admin peut modifier n'importe quel profil."""
        mock_user = Mock()
        mock_user.id = 2
        
        mock_admin = Mock()
        mock_admin.id = 1
        mock_admin.is_admin = True
        
        mock_user_repo = Mock()
        mock_user_repo.get.side_effect = [mock_user, mock_admin, mock_user]
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        result = facade.update_user(2, 1, {"first_name": "Modified"})
        
        mock_user_repo.update.assert_called_once()
        assert result == mock_user


# ========================================
# TESTS DE UPDATE_USER_PASSWORD
# ========================================

class TestUpdateUserPassword:
    """Tests de la méthode update_user_password."""
    
    @patch('backend.app.services.facade.db.session')
    def test_update_password_success(self, mock_session):
        """Test la mise à jour réussie du mot de passe."""
        mock_user = Mock()
        mock_user.verify_password.return_value = True
        
        mock_user_repo = Mock()
        mock_user_repo.get.return_value = mock_user
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        result = facade.update_user_password(1, "oldpass", "newpass123")
        
        mock_user.verify_password.assert_called_once_with("oldpass")
        mock_user.update_password.assert_called_once_with("newpass123")
        mock_session.commit.assert_called_once()
        assert result == mock_user
    
    @patch('backend.app.services.facade.db.session')
    def test_update_password_wrong_old_password(self, mock_session):
        """Test avec un mauvais ancien mot de passe."""
        mock_user = Mock()
        mock_user.verify_password.return_value = False
        
        mock_user_repo = Mock()
        mock_user_repo.get.return_value = mock_user
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        with pytest.raises(ValueError, match="L'ancien mot de passe est incorrect"):
            facade.update_user_password(1, "wrongold", "newpass")
        
        mock_session.rollback.assert_called_once()


# ========================================
# TESTS DE CREATE_REVIEW
# ========================================

class TestCreateReview:
    """Tests de la méthode create_review."""
    
    @patch('backend.app.services.facade.Review')
    def test_create_review_success(self, MockReview):
        """Test la création réussie d'un commentaire."""
        mock_user = Mock()
        mock_user.id = 1
        
        mock_image = Mock()
        mock_image.id = 10
        
        mock_review_repo = Mock()
        mock_review_instance = Mock()
        MockReview.return_value = mock_review_instance
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.review_repo = mock_review_repo
        facade.get_user_by_id = Mock(return_value=mock_user)
        facade.get_post_image = Mock(return_value=mock_image)
        
        review_data = {
            "user_id": 1,
            "image_post_id": 10,
            "comment": "Super image !"
        }
        
        result = facade.create_review(review_data)
        
        MockReview.assert_called_once_with(
            comment="Super image !",
            user_id=1,
            image_post_id=10
        )
        mock_review_repo.add.assert_called_once_with(mock_review_instance)
        assert result == mock_review_instance
    
    @patch('backend.app.services.facade.db.session')
    def test_create_review_missing_user_id(self, mock_session):
        """Test qu'user_id est requis."""
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        
        review_data = {
            "image_post_id": 10,
            "comment": "Test"
        }
        
        with pytest.raises(ValueError, match="user_id est requis"):
            facade.create_review(review_data)
        
        mock_session.rollback.assert_called_once()
    
    @patch('backend.app.services.facade.db.session')
    def test_create_review_missing_image_post_id(self, mock_session):
        """Test qu'image_post_id est requis."""
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        
        review_data = {
            "user_id": 1,
            "comment": "Test"
        }
        
        with pytest.raises(ValueError, match="image_post_id est requis"):
            facade.create_review(review_data)
        
        mock_session.rollback.assert_called_once()


# ========================================
# TESTS DE CREATE_IMAGE_POST
# ========================================

class TestCreateImagePost:
    """Tests de la méthode create_image_post."""
    
    @patch('backend.app.services.facade.ImagePost')
    def test_create_image_post_success(self, MockImagePost):
        """Test la création réussie d'un post image."""
        mock_user = Mock()
        mock_user.id = 1
        
        mock_image_post_repo = Mock()
        mock_image_post_repo.get_by_title_and_user.return_value = None
        mock_image_instance = Mock()
        MockImagePost.return_value = mock_image_instance
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.image_post_repo = mock_image_post_repo
        facade.get_user_by_id = Mock(return_value=mock_user)
        
        image_bytes = b"fake_image_data"
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        image_data = {
            "user_id": 1,
            "title": "Carte du Gondor",
            "description": "Belle carte",
            "image_data": image_b64,
            "image_mime_type": "image/png"
        }
        
        result = facade.create_image_post(image_data)
        
        call_args = MockImagePost.call_args[1]
        assert isinstance(call_args['image_data'], bytes)
        assert call_args['title'] == "Carte du Gondor"
        
        mock_image_post_repo.add.assert_called_once_with(mock_image_instance)
        assert result == mock_image_instance
    
    @patch('backend.app.services.facade.db.session')
    def test_create_image_post_missing_user_id(self, mock_session):
        """Test qu'user_id est requis."""
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        
        image_data = {
            "title": "Test"
        }
        
        with pytest.raises(ValueError, match="user_id est requis"):
            facade.create_image_post(image_data)
        
        mock_session.rollback.assert_called_once()
    
    @patch('backend.app.services.facade.db.session')
    def test_create_image_post_duplicate_title(self, mock_session):
        """Test qu'on ne peut pas créer deux posts avec le même titre."""
        mock_user = Mock()
        mock_user.id = 1
        
        existing_post = Mock()
        
        mock_image_post_repo = Mock()
        mock_image_post_repo.get_by_title_and_user.return_value = existing_post
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.image_post_repo = mock_image_post_repo
        facade.get_user_by_id = Mock(return_value=mock_user)
        
        image_b64 = base64.b64encode(b"test").decode('utf-8')
        
        image_data = {
            "user_id": 1,
            "title": "Duplicate",
            "description": "Test",
            "image_data": image_b64,
            "image_mime_type": "image/png"
        }
        
        with pytest.raises(ValueError, match="existe déjà"):
            facade.create_image_post(image_data)
        
        mock_session.rollback.assert_called_once()


# ========================================
# TESTS DE UPDATE_IMAGE_POST
# ========================================

class TestUpdateImagePost:
    """Tests de la méthode update_image_post."""
    
    @patch('backend.app.services.facade.db.session')
    def test_update_image_post_success(self, mock_session):
        """Test la mise à jour réussie d'un post image."""
        mock_image_post = Mock()
        mock_image_post.user_id = 1
        
        mock_updated_post = Mock()
        
        mock_image_post_repo = Mock()
        mock_image_post_repo.get.side_effect = [mock_image_post, mock_updated_post]
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.image_post_repo = mock_image_post_repo
        
        update_data = {"title": "Nouveau titre"}
        
        result = facade.update_image_post(10, 1, update_data)
        
        mock_image_post_repo.update.assert_called_once_with(10, update_data)
        assert result == mock_updated_post
    
    @patch('backend.app.services.facade.db.session')
    def test_update_image_post_permission_denied(self, mock_session):
        """Test qu'on ne peut modifier que ses propres posts."""
        mock_image_post = Mock()
        mock_image_post.user_id = 2
        
        mock_image_post_repo = Mock()
        mock_image_post_repo.get.return_value = mock_image_post
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.image_post_repo = mock_image_post_repo
        
        with pytest.raises(PermissionError, match="Vous n'êtes pas autorisé"):
            facade.update_image_post(10, 1, {"title": "Test"})
        
        mock_session.rollback.assert_called_once()


# ========================================
# TESTS DE DELETE_IMAGE_POST
# ========================================

class TestDeleteImagePost:
    """Tests de la méthode delete_image_post."""
    
    @patch('backend.app.services.facade.db.session')
    def test_delete_image_post_success(self, mock_session):
        """Test la suppression réussie d'un post image."""
        mock_image_post = Mock()
        mock_image_post.user_id = 1
        
        mock_image_post_repo = Mock()
        mock_image_post_repo.get.return_value = mock_image_post
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.image_post_repo = mock_image_post_repo
        
        result = facade.delete_image_post(10, 1)
        
        mock_image_post_repo.delete.assert_called_once_with(10)
        assert result is True
    
    @patch('backend.app.services.facade.db.session')
    def test_delete_image_post_permission_denied(self, mock_session):
        """Test qu'on ne peut supprimer que ses propres posts."""
        mock_image_post = Mock()
        mock_image_post.user_id = 2
        
        mock_image_post_repo = Mock()
        mock_image_post_repo.get.return_value = mock_image_post
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.image_post_repo = mock_image_post_repo
        
        with pytest.raises(PermissionError, match="Vous n'êtes pas autorisé"):
            facade.delete_image_post(10, 1)
        
        mock_session.rollback.assert_called_once()


# ========================================
# TESTS DE GET METHODS
# ========================================

class TestGetMethods:
    """Tests des méthodes de récupération."""
    
    def test_get_all_user(self):
        """Test la récupération de tous les utilisateurs."""
        mock_users = [Mock(), Mock(), Mock()]
        for i, user in enumerate(mock_users):
            user.to_dict.return_value = {"id": i, "name": f"User{i}"}
        
        mock_user_repo = Mock()
        mock_user_repo.get_all.return_value = mock_users
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.user_repo = mock_user_repo
        
        result = facade.get_all_user()
        
        assert len(result) == 3
        assert all(isinstance(item, dict) for item in result)
    
    def test_get_reviews_by_image(self):
        """Test la récupération des reviews par image."""
        mock_reviews = [Mock(), Mock()]
        
        mock_review_repo = Mock()
        mock_review_repo.get_by_image_post_id.return_value = mock_reviews
        
        from backend.app.services.facade import PortfolioFacade
        facade = PortfolioFacade()
        facade.review_repo = mock_review_repo
        
        result = facade.get_reviews_by_image(10)
        
        mock_review_repo.get_by_image_post_id.assert_called_once_with(10)
        assert result == mock_reviews
