from app.models.BaseModel import BaseModel
from app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Commentaire d'image"""
    __tablename__ = 'reviews'

    comment = db.Column(db.String(400), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)


    def __init__(self, comment):
        """Initialize a Review instance with text, rating, user_id and place_id."""
        super().__init__()
        self.comment = self.validate_text("text", text)
        self.user_id = self.validate_user_id("user_id", user_id)

    @validates('text')
    def validate_text(self, _key, comment):
        """Validate that text is a non-empty string with max length 400."""
        if not isinstance(text, str):
            raise ValueError("The comment must be a string.")
        if not text:
            raise ValueError("Text is required.")
        if len(text) > 400:
            raise ValueError("The comment must not exceed 400 characters.")
        return text

    @validates('user_id')
    def validate_user_id(self, _key, user_id):
        """Validate that user_id is a 36-character UUID string."""
        if not isinstance(user_id, str):
            raise ValueError("user_id must be a UUID string.")
        if len(user_id) != 36:
            raise ValueError("user_id must be 36 characters long (UUID format).")
        return user_id

    def to_dict(self):
        """Convert the Review instance to a Python dictionary for serialization."""
        return {
            "id": self.id,
            "comment": self.comment
        }
