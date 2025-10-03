from app.models.basemodel import BaseModel
from app import db
from sqlalchemy.orm import validates
from app.models.user import User

class ImagePost(BaseModel):
    """ Un utilisateur connecté peut poster une image """
    __tablename__ = 'image_post'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    image_mime_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='image_posts')

    def __init__(self, title, description, image_data, image_mime_type, user_id):
        super().__init__()
        self.title = self.validate_title("title", title)
        self.description = self.validate_description("description", description)
        self.image_data = self.validate_image_data("image_data", image_data)
        self.image_mime_type = image_mime_type
        self.user_id = self.validate_user_id("user_id", user_id)

    @validates('title')
    def validate_title(self, _key, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Le titre est requis et doit être une chaîne.")
        if len(title) > 100:
            raise ValueError("Le titre ne doit pas dépasser 100 caractères.")
        return title
    
    @validates('description')
    def validate_description(self, _key, description):
        if not isinstance(description, str) or not description.strip():
            raise ValueError("La description est requise et doit être une chaîne.")
        if len(description) > 150:
            raise ValueError("La description ne doit pas dépasser 150 caractères.")
        return description

    @validates('image_data')
    def validate_image_data(self, _key, image_data):
        if not image_data:
            raise ValueError("Les données de l'image sont requises.")
        if not isinstance(image_data, (bytes, bytearray)):
            raise ValueError("L'image doit être de type binaire (bytes).")
        return image_data

    @validates('user_id')
    def validate_user_id(self, _key, user_id):
        if not isinstance(user_id, int):
            raise ValueError("user_id doit être un entier.")
        if user_id <= 0:
            raise ValueError("user_id doit être un entier positif.")
        return user_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "image_mime_type": self.image_mime_type,
            # Note : l'image elle-même n'est pas incluse ici (trop lourde !)
        }
