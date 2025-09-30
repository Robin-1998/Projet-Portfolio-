from app import db
from datetime import datetime, timezone

class BaseModel(db.model):
    """ Classe de base pour tout les modèles"""

    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc))

    def save(self):
        """ sauvegarde de l'objet en base de données"""
        self.updated_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprime l'objet de la base"""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Met à jour les attributs de l'objet"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:  # Protège id et created_at
                setattr(self, key, value)
        self.save()
