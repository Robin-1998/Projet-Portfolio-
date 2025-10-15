from backend.app.persistence.repository import SQLAlchemyRepository
from backend.app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    """Repository spécifique pour les commentaires."""
    
    def __init__(self):
        """Initialise le repository avec le modèle Review"""
        super().__init__(Review)
    
    def get_by_image_post_id(self, image_post_id):
        return self.model.query.filter_by(image_post_id=image_post_id).all()
    
    def get_by_user_id(self, user_id):
        """Récupère tous les commentaires d'un utilisateur"""
        return self.model.query.filter_by(user_id=user_id).all()
