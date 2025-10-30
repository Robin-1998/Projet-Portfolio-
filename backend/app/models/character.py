"""
Module contenant le modèle de character

Classes :
    Character : Modèle de personnage, en lecture seule, associé à une race.
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class Character(BaseModel):
    """
    classe Character en lecture seule
    
    Cette classe modélise un personnage avec ses attributs principaux : nom, dates,
    genre, profession, description, et citation. Elle est liée à la table `characters`
    dans la base de données et possède une relation vers le modèle `Race`.
    """

    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Integer, nullable=True)
    death_date = db.Column(db.Integer, nullable=True)
    era_birth = db.Column(db.String(25), nullable=False)
    era_death = db.Column(db.String(25), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    profession = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    citation = db.Column(db.String(400))


    race_id = db.Column(db.BigInteger, db.ForeignKey('races.id'))
    # Relation ORM vers la classe Race
    race = db.relationship('Race', back_populates='characters')

    def to_dict(self):
        """
        Convertit l'objet Character en dictionnaire sérialisable.

        Cette méthode surcharge `BaseModel.to_dict()` afin d’inclure
        les champs spécifiques au modèle Character.
        """
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "era_birth": self.era_birth,
            "era_death": self.era_death,
            "gender": self.gender,
            "profession": self.profession,
            "description": self.description,
            "citation": self.citation
        }

