"""
Module contenant le modèle de description

Ce module définit la classe Description, utilisée pour stocker des descriptions détaillées
associées à différents types d'entités dans la base de données (par exemple : personnages,
foret, ville, races ou encore histoire).

Chaque enregistrement de la table `descriptions` représente un bloc de texte décrivant une entité
donnée, identifié par son type (`entity_type`) et son identifiant (`entity_id`).
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel


class Description(BaseModel):
    """
    Classe représentant une description textuelle d'une entité

    Cette classe est utilisée pour enregistrer des blocs de texte décrivant divers éléments
    enregistré dans entity_type (character, region, ville, races, etc.). Chaque description est liée à une entité
    par son type et son identifiant, et peut être ordonnée via le champ `order_index`.
    """
    __tablename__ = "descriptions"

    id = db.Column(db.BigInteger, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # 'character', 'ville', 'region', 'race', 'history'
    entity_id = db.Column(db.BigInteger, nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer)

    def __repr__(self):
        return f"<Description {self.entity_type} #{self.entity_id} - {self.title}>"

    def to_dict(self):
        """
        Convertit l'objet Description en dictionnaire sérialisable.

        Returns:
            dict: Dictionnaire contenant les informations principales de la description.
        """
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "title": self.title,
            "content": self.content,
            "order_index": self.order_index,
        }
