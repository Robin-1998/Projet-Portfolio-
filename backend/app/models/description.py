from datetime import datetime
from backend.app import db
from backend.app.models.basemodel import BaseModel


class Description(BaseModel):
    __tablename__ = "descriptions"

    id = db.Column(db.BigInteger, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # 'character', 'place', 'race', 'history'
    entity_id = db.Column(db.BigInteger, nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer)

    def __repr__(self):
        return f"<Description {self.entity_type} #{self.entity_id} - {self.title}>"
