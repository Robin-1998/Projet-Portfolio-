from datetime import datetime, timezone
from app import db, bcrypt
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    """ Class utilisateur qui hérite de BaseModel"""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Récupérez les identifiants ID, created_at et update_at de
        classe BaseModel. Initialisation de first_name, last_name, email et
        is_admin avec les méthodes de validation.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """Gère les conditions de validation du Nom et Prénom."""
        if not isinstance(name, str):
            raise ValueError(f"{key} soit être une chaîne de caractères")

        name = name.strip()

        if not name:
            raise ValueError(
                f"{key} ne peut pas être vide")

        if not (1 <= len(name) <= 50):
            raise ValueError(
                f"{key} doit contenir entre 1 et 50 caractères.")

        if not re.fullmatch(r"[a-zA-ZÀ-ÿ\s-]+", name):
            raise ValueError(
                f"{key} ne doit contenir que des lettres ou des tirets.")

        return name.title() # capitalisation (majuscules) automatique

    @validates('email')
    def validation_email(self, _key, email):
        """
        Méthode de validation vérifiant la validité de l'adresse e-mail
        à l'aide de la bibliothèque email-Validator
        """
        try: # on appelle la bibliothèque validate_email et on la valide
            valid = validate_email(email)
            return valid.normalized

        # Renvoie l'email propre si valide
        except EmailNotValidError as email_error:
            raise ValueError(f"Error, invalid email : {email_error}")

    def hash_password(self, password):
        """
        Utilisation de Bcrypt car plus de contrôle et sécurité sur les
        mots de passes (comparé à Werkzeug Security).

        Hache le mot de passe avant de le stocker.
        """
        if not password:
            raise ValueError("Le mot de passe ne peut être vide")

        if len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")

        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Vérifie si le mot de passe fourni correspond au mot de passe haché.
        """
        return bcrypt.check_password_hash(self.password, password)

    @validates('is_admin')
    def validate_is_admin(self, _key, is_admin):
        """
        Méthode de validation qui vérifie si l'utilisateur est administrateur
        ou non. Par défaut is_admin = False.
        """
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin doit être un booléen.")
        return is_admin

    def to_dict(self):
        """Converti un objet utilisateur (User) en un dictionnaire Python"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
