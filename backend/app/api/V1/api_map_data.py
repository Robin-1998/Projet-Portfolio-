"""
Module pour la récupération des différents types de lieu

Ce module définit l'ensemble des routes de l'API Flask-RESTX liées à la carte interactive.
Il permet de récupérer les régions (polygones), les lieux (marqueurs), et leurs hiérarchies.
Il s'agit d'endpoints en lecture seule (GET uniquement).

Structure hiérarchique :
- Régions : Zones géographiques définies par des polygones (ex: Mordor, Rohan)
- Lieux : Points d'intérêt avec marqueurs (ex: villes, forteresses, ports)
- Chaque entité peut avoir des enfants (sous-régions ou sous-lieux)
"""

from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

api = Namespace('map', description='API Carte interactive')

#---------------- CARTE COMPLÈTE - pour initialisation -----------------------

@api.route('/data')
class MapData(Resource):
    """Gestion des données complètes pour l'initialisation de la carte."""
    def get(self):
        """
        Récupère toutes les données nécessaires pour initialiser la carte interactive.

        Cette méthode retourne un ensemble complet mais léger de données
        permettant d'afficher la carte initiale sans surcharger le client.
        Version optimisée pour le premier chargement.

        Note:
            Cette route est typiquement appelée une seule fois au chargement
            de la page pour initialiser la carte complète. Les détails
            supplémentaires sont ensuite chargés à la demande.
        """
        map_data = facade.get_map_data()
        return {
            "success": True,
            "data": map_data
        }, 200

#--------------------- PLACES - Détails enrichis ------------------------

@api.route('/places/<int:place_id>/details')
class PlaceDetailedInfo(Resource):
    """
    Gestion des informations détaillées d'un lieu
    """
    def get(self, place_id):
        """
        Récupère les informations complètes et détaillées d'un lieu.

        Cette méthode retourne un ensemble enrichi de données sur un lieu,
        incluant ses descriptions organisées par sections, ses métadonnées
        (ex: titre + texte descriptif), son image principale,
        et potentiellement sa hiérarchie d'enfants.
        """
        detailed_data = facade.get_place_detailed_info(place_id)

        if not detailed_data:
            return {
                "success": False,
                "error": "Lieu non trouvé ou aucune information détaillée disponible"
            }, 404

        return {
            "success": True,
            "data": detailed_data
        }, 200
