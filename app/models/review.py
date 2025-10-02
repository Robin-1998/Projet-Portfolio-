from app.models.basemodel import BaseModel
from app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Commentaire d'image"""
    __tablename__ = 'reviews'

    comment = db.Column(db.String(400), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    post_image_id = db.Column(db.BigInteger, db.ForeignKey('post_images.id'), nullable=False)

    def __init__(self, comment, user_id, post_image_id):
        super().__init__()
        self.comment = self.validate_text("comment", comment)
        self.user_id = self.validate_user_id("user_id", user_id)
        self.post_image_id = self.validate_post_image_id("post_image_id", post_image_id)

    @validates('comment')
    def validate_text(self, _key, comment):
        """ Vérifier que le texte est une chaîne non vide d'une longueur maximale de 400 caractères. """
        if not isinstance(comment, str):
            raise ValueError("Le commentaire doit être une chaîne de caractère")
        if not comment:
            raise ValueError("Le texte est requis.")
        if len(comment) > 400:
            raise ValueError("Le commentaire ne doit pas dépasser 400 caractères.")
        return comment

    @validates('user_id')
    def validate_user_id(self, _key, user_id):
        """ Validation que le user_id est un entier positif"""
        if not isinstance(user_id, int):
            raise ValueError("user_id doit être en entier")
        if user_id <= 0:
            raise ValueError("user_iddoit être un entier posifif")
        return user_id
    
    @validates('post_image_id')
    def validate_post_image_id(self, _key, post_image_id):
        """ Valide que post_image_id est un entier positif """
        if not isinstance(post_image_id, int):
            raise ValueError("post_image_id doit être un entier")
        if post_image_id <= 0:
            raise ValueError("post_image_id doit être un entier positif.")
        return post_image_id

    def to_dict(self):
        """Convert the Review instance to a Python dictionary for serialization."""
        return {
            "id": self.id,
            "comment": self.comment,
            "user_id": self.user_id,
            "post_image_id": self.post_image_id
        }
