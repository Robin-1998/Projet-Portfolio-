"""
Module de gestion des personnages

Ce module contient les endpoints REST permettant de consulter les informations
sur les personnages. Il s'agit d'endpoints en lecture seule (GET uniquement).
"""

from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

api = Namespace('characters', description='Opérations de lecture sur les personnages')

@api.route("/")
class CharacterList(Resource):
    """Ressource pour accéder à la liste complète des personnages."""
    def get(self):
        """
        Récupère la liste de tout les personnages.
        Cette méthode retourne l'ensemble des personnages stocker en db.
        Endpoint public (pas d'authentification requise).
        """
        # Récupération de tout les personnages via la façade
        characters = facade.get_all_characters()

        # Conversion de chaque objet personnages en dictionnaire
        # La méthode to_dict() transforme l'objet en format JSON-serializable
        return [character.to_dict() for character in characters], 200

@api.route("/<int:character_id>")
class CharacterDetail(Resource):
    """ Ressource pour accéder aux détails d'une personnage spécifique. """
    def get(self, character_id):
        """
        Récupère les détails d'un personnage par son ID.

        Cette méthode retourne les informations complètes d'un personnage identifié
        par son ID unique. Endpoint public (pas d'authentification requise).
        
        Args:
            character_id (int): L'identifiant unique du personnage à récupérer
            
        Code Erreur:
            404: Si aucune personnage ne correspond à l'ID fourni
        """
        try:
            # Récupération du personnage spécifique via la façade
            character = facade.get_character(character_id)

            # Conversion de l'objet personnage en dictionnaire pour la réponse JSON
            return character.to_dict(), 200

        except ValueError as error:
            return {"error": str(error)}, 404

