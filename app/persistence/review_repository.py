from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    """Repository spécifique pour les commentaires."""
    
    def __init__(self):
        """Initialise le repository avec le modèle Review"""
        super().__init__(Review)
    
    def get_by_post_image_id(self, image_post_id):
        """Récupère tous les commentaires d'une image spécifique"""
        return self.model.query.filter_by(image_post_id=image_post_id).all()
    
    def get_by_user_id(self, user_id):
        """Récupère tous les commentaires d'un utilisateur"""
        return self.model.query.filter_by(user_id=user_id).all()
