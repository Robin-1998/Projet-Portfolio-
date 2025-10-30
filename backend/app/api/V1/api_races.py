"""
Module de gestion des races

Ce module contient les endpoints REST permettant de consulter les informations
sur les races. Il s'agit d'endpoints en lecture seule (GET uniquement).
"""
from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

# Namespace races
api = Namespace('races', description='Opérations de lecture sur les races')

@api.route("/")
class RaceList(Resource):
    """Ressource pour accéder à la liste complète des races."""
    def get(self):
        """
        Récupère la liste de toute les races.
        Cette méthode retourne l'ensemble des races stocker en db.
        Endpoint public (pas d'authentification requise).
        """
        # Récupération de toute les races via la façade
        races = facade.get_all_races()

        # Conversion de chaque objet races en dictionnaire
        # La méthode to_dict() transforme l'objet en format JSON-serializable
        return [race.to_dict() for race in races], 200

@api.route("/<int:race_id>")
class RaceDetail(Resource):
    """ Ressource pour accéder aux détails d'une race spécifique. """
    def get(self, race_id):
        """
        Récupère les détails d'une race par son ID.

        Cette méthode retourne les informations complètes d'une race identifié
        par son ID unique. Endpoint public (pas d'authentification requise).
        
        Args:
            race_id (int): L'identifiant unique de la race à récupérer
            
        Code Erreur:
            404: Si aucune race ne correspond à l'ID fourni
        """
        try:
            # Récupération de la race spécifique via la façade
            race = facade.get_race(race_id)

            # Conversion de l'objet histoire en dictionnaire pour la réponse JSON
            return race.to_dict(), 200

        except ValueError as error:
            return {"error": str(error)}, 404
