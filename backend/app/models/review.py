"""
Ce module définit le modèle `Review`, représentant un commentaire laissé par un utilisateur
sur une image publiée dans l'application.

Chaque commentaire est lié :
- à un utilisateur (`User`), via `user_id`,
- à une image (`ImagePost`), via `image_post_id`.
"""
from backend.app.models.basemodel import BaseModel
from backend.app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    """
    Modèle représentant un commentaire d'image postée par un utilisateur.

    Relations :
        user (User) : L'utilisateur qui a écrit le commentaire.
        image_post (ImagePost) : L'image à laquelle le commentaire est associé.
    """
    __tablename__ = 'reviews'

    comment = db.Column(db.String(400), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    image_post_id = db.Column(db.BigInteger, db.ForeignKey('image_post.id'), nullable=False)

    # ---------------------
    # Relations ORM
    # ---------------------

    user = db.relationship('User', backref='reviews')
    image_post = db.relationship('ImagePost', backref='reviews')

    def __init__(self, comment, user_id, image_post_id):
        super().__init__()
        self.comment = self.validate_text("comment", comment)
        self.user_id = self.validate_user_id("user_id", user_id)
        self.image_post_id = self.validate_image_post_id("image_post_id", image_post_id)

    # ---------------------
    # Validations des champs
    # ---------------------

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

    @validates('image_post_id')
    def validate_image_post_id(self, _key, image_post_id):
        """ Valide que image_post_id est un entier positif """
        # Accepter None lors de la suppression (orphan removal)
        if image_post_id is None:
            return image_post_id

        if not isinstance(image_post_id, int):
            raise ValueError("image_post_id doit être un entier")
        if image_post_id <= 0:
            raise ValueError("image_post_id doit être un entier positif")
        return image_post_id

    def to_dict(self):
        """
        Sérialise l'objet Review en dictionnaire JSON-compatible.
        """
        return {
            "id": self.id,
            "comment": self.comment,
            "user_id": self.user_id,
            "image_post_id": self.image_post_id
        }
