from backend.app import db
from datetime import datetime
from sqlalchemy import Enum
import enum

class EntityTypeEnum(enum.Enum):
    character = 'character'
    place = 'place'
    race = 'race'
    history = 'history'

class EntityDescription(db.Model):
    __tablename__ = 'entity_descriptions'

    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer)
    image_url = db.Column(db.String(500))  # Ajoute cette colonne
    relation_type_id = db.Column(db.BigInteger, db.ForeignKey('relation_types.id'))
    entity_type = db.Column(Enum(EntityTypeEnum), nullable=False)
    entity_id = db.Column(db.BigInteger, nullable=False)

    # Relations
    relation_type = db.relationship('RelationType', backref='entity_descriptions')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'order_index': self.order_index,
            'image_url': self.image_url,
            'entity_type': self.entity_type.value,
            'entity_id': self.entity_id,
            'relation_type': self.relation_type.name if self.relation_type else None
        }
