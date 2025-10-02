from app import db
from datetime import datetime, timezone

class BaseModel(db.Model):
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

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire de base.
        DOIT être surchargée dans les classes enfants pour inclure leurs attributs.
        
        Returns:
            dict: Dictionnaire avec id, created_at, updated_at
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ⚠️ IMPORTANT : J'ai supprimé les méthodes delete() et update() de BaseModel
# Car elles entrent en conflit avec le pattern Repository que vous utilisez.
# 
# Avec le pattern Repository :
# - Les opérations CRUD passent par le Repository
# - Le Repository gère les transactions (commit/rollback)
# - Les modèles restent des objets de données simples
#
# Si vous voulez vraiment garder ces méthodes, utilisez plutôt :
# - obj.save() pour sauvegarder les changements d'un objet existant
# - repository.delete(obj_id) pour supprimer
# - repository.update(obj_id, data) pour mettre à jour
