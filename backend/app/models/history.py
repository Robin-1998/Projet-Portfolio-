"""
Module contenant le modèle des histoires
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class History(BaseModel):
    """
    classe History en lecture seule

    Cette classe modélise une histoire avec ses attributs principaux : nom, description rapide,
    l'année du début de l'évènement, l'année de fin de l'évènement, la période de l'histoire (l'ère), et une citation.
    Elle est liée à la table `history` dans la base de données
    """

    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_year = db.Column(db.Integer, nullable=True)
    end_year = db.Column(db.Integer, nullable=True)
    era = db.Column(db.String(25), nullable=True)
    citation = db.Column(db.String(400))


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "era": self.era,
            "citation": self.citation
        }
