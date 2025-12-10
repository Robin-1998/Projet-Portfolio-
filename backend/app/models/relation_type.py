"""
Ce module définit le modèle `RelationType`, qui représente un type de relation
entre différents objets de l'application

Chaque type de relation est stocké dans la table `relation_types` et peut être référencé
par d'autres modèles via une clé étrangère.
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel
from sqlalchemy.orm import validates

class RelationType(BaseModel):
    """
    Modèle représentant un type de relation entre entités.

    Cette table contient des types de relations nommées, uniques, pouvant être utilisées
    dans d'autres tables (ex. : relations entre personnages, lieux, etc.).

    """
    __tablename__ = 'relation_types'

    name = db.Column(db.String(50), nullable=False, unique=True)

    histories = db.relationship("History", back_populates="relation_type", lazy='select')


    @validates('name')
    def validate_text(self, _key, name):
        """ Vérifier que le texte est une chaîne non vide d'une longueur maximale de 50 caractères. """
        if not isinstance(name, str):
            raise ValueError("Le nom doit être une chaîne de caractère")
        name = name.strip()
        if not name:
            raise ValueError("Le texte est requis.")
        if len(name) > 50:
            raise ValueError("Le nom ne doit pas dépasser 50 caractères.")
        return name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
