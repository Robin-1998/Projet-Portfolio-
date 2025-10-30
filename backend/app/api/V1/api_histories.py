"""
Module de gestion des histoires

Ce module contient les endpoints REST permettant de consulter les informations
sur les histoires. Il s'agit d'endpoints en lecture seule (GET uniquement).
"""

from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

# Appel de PortfolioFacade qui est divisié en deux fichier
facade = PortfolioFacade()

api = Namespace('histories', description='Opérations de lecture sur les races')

@api.route("/")
class historyList(Resource):
    """Ressource pour accéder à la liste complète des histoires."""
    def get(self):
        """
        Récupère la liste de toute les histoires.
        Cette méthode retourne l'ensemble des histoires stocker en db.
        Endpoint public (pas d'authentification requise).
        """
        # Récupération de toutes les histoires via la façade
        histories = facade.get_all_histories()

        # Conversion de chaque objet histoires en dictionnaire
        # La méthode to_dict() transforme l'objet en format JSON-serializable
        return [history.to_dict() for history in histories], 200

@api.route("/<int:history_id>")
class HistoryDetail(Resource):
    """ Ressource pour accéder aux détails d'une histoire spécifique. """
    def get(self, history_id):
        """
        Récupère les détails d'une histoire par son ID.

        Cette méthode retourne les informations complètes d'un personnage identifié
        par son ID unique. Endpoint public (pas d'authentification requise).
        
        Args:
            history_id (int): L'identifiant unique de l'histoire à récupérer
            
        Code Erreur:
            404: Si aucune histoire ne correspond à l'ID fourni
        """
        try:
            # Récupération de l'histoire spécifique via la façade
            history = facade.get_history(history_id)

            # Conversion de l'objet histoire en dictionnaire pour la réponse JSON
            return history.to_dict(), 200
        except ValueError as error:
            return {"error": str(error)}, 404
