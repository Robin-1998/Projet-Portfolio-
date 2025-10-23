from backend.app import db

class RelationType(db.Model):
    __tablename__ = 'relation_types'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
