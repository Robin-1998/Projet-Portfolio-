"""
Ce module définit le repository `ImagePostRepository`, qui gère la persistance
des entités `ImagePost` (images publiées par les utilisateurs).

Il hérite de `SQLAlchemyRepository`, une implémentation générique du parent Repository,
et ajoute des méthodes spécifiques liées aux publications d'images :
    - récupération par titre et utilisateur (pour éviter les doublons),
    - récupération de toutes les images d’un utilisateur,
    - recherche d’images par titre.
"""
from backend.app.persistence.repository import SQLAlchemyRepository
from backend.app.models.image_post import ImagePost

class ImagePostRepository(SQLAlchemyRepository):
    """
        Repository dédié à la gestion des entités `ImagePost`.
        Fournit des méthodes spécifiques de recherche et de filtrage
        liées aux publications d’images dans la base de données.
        Hérite de :
            SQLAlchemyRepository : Classe générique fournissant les opérations CRUD de base.

    """
    def __init__(self):
        """
        Initialise le repository pour le modèle `ImagePost`.

        Appelle le constructeur parent (`SQLAlchemyRepository`) en lui passant
        la classe du modèle à manipuler.
        """
        super().__init__(ImagePost)
    
    def get_by_title_and_user(self, title, user_id):
        """
        Récupère un post par titre et utilisateur (pour vérifier les doublons)
        Utile pour vérifier qu’un utilisateur n’a pas déjà publié un post
        portant le même titre (prévention des doublons).
        """
        return self.model.query.filter_by(
            title=title, 
            user_id=user_id
        ).first()
    
    def get_by_user_id(self, user_id):
        """Récupère tous les posts d'un utilisateur"""
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_by_title(self, title):
        """Récupère tous les posts avec un titre donné"""
        return self.model.query.filter_by(title=title).all()
