from backend.app.persistence.repository import SQLAlchemyRepository
from backend.app.models.image_post import ImagePost

class ImagePostRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(ImagePost)
    
    def get_by_title_and_user(self, title, user_id):
        """Récupère un post par titre et utilisateur (pour vérifier les doublons)"""
        return self.model.query.filter_by(
            title=title, 
            user_id=user_id
        ).first()
    
    def get_by_user_id(self, user_id):
        """Récupère tous les posts d'un utilisateur"""
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_by_title(self, title):
        """Récupère tous les posts avec un titre donné"""
        return self.model.query.filter_by(title=title).all()
