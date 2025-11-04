"""
Module contenant le modèle des races

Classes :
    Race : Modèle de race, en lecture seule, associé à une race.
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class Race(BaseModel):
    """
    classe race en lecture seule
    
    Cette classe modélise une race avec ses attributs principaux : nom, faiblesses,
    force, description, et citation. Elle est liée à la table `races`
    dans la base de données et possède une relation vers le modèle `Character`.
    """

    __tablename__ = "races"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weakness = db.Column(db.String(255), nullable=False)
    strength = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    citation = db.Column(db.String(400))

    characters = db.relationship('Character', back_populates='race', lazy='dynamic')


    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "weakness": self.weakness,
            "strength": self.strength,
            "description": self.description,
            'citation': self.citation
        }
