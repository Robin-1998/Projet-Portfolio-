"""
Module contenant le modèle de base pour tous les modèles de l'application

Ce module définit la classe BaseModel qui sert de classe parente à tous les modèles
de la base de données. Elle fournit des fonctionnalités communes comme les timestamps
automatiques (created_at, updated_at) et des méthodes utilitaires pour la sauvegarde
et la conversion en dictionnaire.

Tous les modèles de l'application doivent hériter de cette classe pour bénéficier
de ces fonctionnalités de base.
"""
from backend.app import db
from datetime import datetime, timezone

class BaseModel(db.Model):
    """
    Classe de base pour tout les modèles de l'app

    Attributes:
    id (BigInteger): Identifiant unique auto-incrémenté (clé primaire)
    created_at (DateTime): Date et heure de création de l'enregistrement (UTC)
    updated_at (DateTime): Date et heure de dernière modification (UTC)
    
    Note:
        Cette classe est abstraite (__abstract__ = True) et ne créera pas
        de table en base de données. Elle sert uniquement de modèle parent.
    """

    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc))

    def save(self):
        """
        sauvegarde de l'objet en base de données

        Cette méthode simplifie le processus de sauvegarde en encapsulant
        les opérations db.session.add() et db.session.commit(). Elle met
        également à jour automatiquement le champ updated_at.
        """
        self.updated_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire de base.

        Cette méthode de base retourne uniquement les champs communs (id, timestamps).
        Elle DOIT être surchargée dans les classes enfants pour inclure leurs
        attributs spécifiques.
        Returns:
            dict: Dictionnaire avec id, created_at, updated_at

        Note:
        Les dates sont converties au format ISO 8601 (ex: "2024-01-15T10:30:00")
        pour faciliter la sérialisation JSON et l'interopérabilité.
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

