from datetime import datetime, timezone
from app import db, bcrypt
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    """ Class utilisateur qui hérite de BaseModel"""

    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """ gère les conditions de validation du prénom et nom """
        if not isinstance(name, str):
            raise ValueError(f"{key} soit être une chaîne de caractères")
        name = name.strip()
        if not name:
            raise ValueError(
                f"{key} ne peut pas être vide")
        if not (1 <= len(name) <= 50):
            raise ValueError(
                f"{key} doit contenir entre 1 et 50 caractères.")
        if not re.fullmatch(r"[ a-zA-ZÀ-ÿ-]+", name):
            raise ValueError(
                f"{key} ne doit contenir que des lettres ou des tirets.")
        return name.title() # capitalisation automatique

    def to_dict(self):
        # transforme une liste de user en dico
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

# utilisation de Bcrypt comparé Werkzeug Security car plus de contrôle et
#  sécurité sur les mots de passes
