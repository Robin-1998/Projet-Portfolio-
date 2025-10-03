from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    """Repository spécifique pour les commentaires."""
    def get_by_post_image_id(self, image_post_id):
        return Review.query.filter_by(image_post_id=image_post_id).all()
