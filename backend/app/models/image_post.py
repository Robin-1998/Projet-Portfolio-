"""
Module contenant le modèle des envoie d'images

Ce module définit la classe ImagePost, qui représente une image envoyée par un utilisateur connecté.
Chaque image est stockée directement sous forme binaire dans la base de données, avec son type MIME
et des métadonnées associées (titre, description, auteur).
"""
from backend.app.models.basemodel import BaseModel
from backend.app import db
from sqlalchemy.orm import validates

class ImagePost(BaseModel):
    """
    Classe représentant un envoi d’image par un utilisateur.

    Cette classe gère les informations relatives à une image postée par un utilisateur.
    L’image est enregistrée dans la base de données en binaire (champ `image_data`) ainsi
    que son type MIME (`image_mime_type`)
    """
    __tablename__ = 'image_post'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    image_mime_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)

    # Relation ORM vers l'utilisateur (chaque image appartient à un utilisateur)
    user = db.relationship('User', back_populates='image_posts')

    def __init__(self, title, description, image_data, image_mime_type, user_id):
        super().__init__()
        self.title = self.validate_title("title", title)
        self.description = self.validate_description("description", description)
        self.image_data = self.validate_image_data("image_data", image_data)
        self.image_mime_type = image_mime_type
        self.user_id = self.validate_user_id("user_id", user_id)

    # ------------------- VALIDATIONS DES CHAMPS -------------------

    @validates('title')
    def validate_title(self, _key, title):
        """Valide le titre : chaîne non vide, longueur <= 100 caractères."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Le titre est requis et doit être une chaîne.")
        if len(title) > 100:
            raise ValueError("Le titre ne doit pas dépasser 100 caractères.")
        return title
    
    @validates('description')
    def validate_description(self, _key, description):
        """Valide la description : chaîne non vide, longueur <= 150 caractères."""
        if not isinstance(description, str) or not description.strip():
            raise ValueError("La description est requise et doit être une chaîne.")
        if len(description) > 150:
            raise ValueError("La description ne doit pas dépasser 150 caractères.")
        return description

    @validates('image_data')
    def validate_image_data(self, _key, image_data):
        """Vérifie que l’image est fournie et de type binaire (bytes)."""
        if not image_data:
            raise ValueError("Les données de l'image sont requises.")
        if not isinstance(image_data, (bytes, bytearray)):
            raise ValueError("L'image doit être de type binaire (bytes).")
        return image_data

    @validates('user_id')
    def validate_user_id(self, _key, user_id):
        """Vérifie que user_id est un entier positif."""
        if not isinstance(user_id, int):
            raise ValueError("user_id doit être un entier.")
        if user_id <= 0:
            raise ValueError("user_id doit être un entier positif.")
        return user_id

    def to_dict(self):
        """
        Convertit l'objet ImagePost en dictionnaire JSON-sérialisable.

        Note :
            Le champ `image_data` n’est **pas** inclus pour éviter de transférer
            de grandes quantités de données binaires dans les réponses API.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "image_mime_type": self.image_mime_type,
        }
