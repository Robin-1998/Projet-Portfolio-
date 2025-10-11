from app import db
from app.models.basemodel import BaseModel

class Race(BaseModel):
    "classe Race en lecture seule"

    __tablename__ = "races"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weakness = db.Column(db.String(255), nullable=False)
    strength = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    characters = db.relationship('Character', back_populates='race', lazy='dynamic')


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "weakness": self.weakness,
            "strength": self.strength,
            "description": self.description
        }
