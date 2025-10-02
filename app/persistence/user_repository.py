from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository spécifique pour les utilisateurs."""
    def __init__(self):
        """ Initializes the UserRepository with the User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """ Retrieve a user instance by their email address."""
        return self.model.query.filter_by(email=email).first()
    
    def email_exists(self, email):
        """
        Vérifie si un email existe déjà dans la base de données.
        
        Args:
            email (str): L'adresse email à vérifier
        
        Returns:
            bool: True si l'email existe, False sinon
        """
        return self.get_user_by_email(email) is not None

    def get_all_admins(self):
        """
        Récupère tous les utilisateurs administrateurs.
        
        Returns:
            list: Liste des utilisateurs avec is_admin=True
        """
        return self.model.query.filter_by(is_admin=True).all()

    def get_all_regular_users(self):
        """
        Récupère tous les utilisateurs non-administrateurs.
        
        Returns:
            list: Liste des utilisateurs avec is_admin=False
        """
        return self.model.query.filter_by(is_admin=False).all()
    

