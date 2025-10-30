"""
Ce module définit le `ReviewRepository`, responsable de la gestion
des entités `Review` (commentaires d’images).


Il hérite de `SQLAlchemyRepository`, qui fournit les opérations CRUD de base,
et ajoute des méthodes spécifiques pour :
    - Récupérer tous les commentaires associés à une image (`get_by_image_post_id`)
    - Récupérer tous les commentaires d’un utilisateur (`get_by_user_id`)

Ce repository permet d’isoler la logique d’accès aux données des commentaires,
afin que le reste de l’application n’interagisse jamais directement avec SQLAlchemy.
"""
from backend.app.persistence.repository import SQLAlchemyRepository
from backend.app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour la gestion des entités `Review`.

    Hérite de :
        SQLAlchemyRepository : fournit les opérations CRUD génériques.
    """
    
    def __init__(self):
        """Initialise le repository avec le modèle Review"""
        super().__init__(Review)
    
    def get_by_image_post_id(self, image_post_id):
        """
        Récupère tous les commentaires liés à une image spécifique.
        """
        return self.model.query.filter_by(image_post_id=image_post_id).all()
    
    def get_by_user_id(self, user_id):
        """Récupère tous les commentaires d'un utilisateur"""
        return self.model.query.filter_by(user_id=user_id).all()
