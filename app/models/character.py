from app import db
from app.models.basemodel import BaseModel

class Character(BaseModel):
    "classe Character en lecture seule"

    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Integer, nullable=False)
    death_date = db.Column(db.Integer, nullable=True)
    era_birth = db.Column(db.String(25), nullable=False)
    era_death = db.Column(db.String(25), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "era_birth": self.era_birth,
            "era_death": self.era_death,
            "gender": self.gender,
            "profession": self.profession,
            "description": self.description
        }

