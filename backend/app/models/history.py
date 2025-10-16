from backend.app import db
from backend.app.models.basemodel import BaseModel

class History(BaseModel):
    "classe History en lecture seule"

    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_year = db.Column(db.Integer, nullable=True)
    end_year = db.Column(db.Integer, nullable=True)
    era = db.Column(db.String(25), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "era": self.era
        }
