"""
Ce module définit le modèle `RelationType`, qui représente un type de relation
entre différents objets de l'application

Chaque type de relation est stocké dans la table `relation_types` et peut être référencé
par d'autres modèles via une clé étrangère.
"""
from backend.app import db

class RelationType(db.Model):
    """
    Modèle représentant un type de relation entre entités.

    Cette table contient des types de relations nommées, uniques, pouvant être utilisées
    dans d'autres tables (ex. : relations entre personnages, lieux, etc.).

    """
    __tablename__ = 'relation_types'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
