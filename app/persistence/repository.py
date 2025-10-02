from abc import ABC, abstractmethod
from app import db
# from app.persistence import InMemoryRepository



# from app import db  # Assuming you have set up SQLAlchemy in your Flask app

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        """Ajoute un objet à la base de données"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """ Récupère un objet par son ID """
        pass

    @abstractmethod
    def get_all(self):
        """ recupère tous les objets """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """ Met à jour un objet """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """ Supprime un objet """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """ Récupère un objet par un attribut spécifique """
        pass

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    # Vérifie que l'attribut existe sur le modèle
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                db.session.commit()
                return obj
            return None
        except Exception as e:
            db.session.rollback()
            raise

    def delete(self, obj_id):
        """
        Supprime un objet de la base de données.
        Args:
            obj_id: L'ID de l'objet à supprimer
        Returns:
            True si supprimé, False si non trouvé
        Raises:
            Exception: Si la suppression échoue
        """
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

