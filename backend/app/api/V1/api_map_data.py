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


#-------------------- REGIONS - Routes principales -------------------------

@api.route('/regions')
class RegionsList(Resource):
    """Gestion de la liste complète des régions avec leur hiérarchie."""
    def get(self):
        """
        Récupère TOUTES les régions avec leur hiérarchie complète d'enfants

        Cette méthode retourne la liste de toutes les régions géographiques
        de la carte, incluant leurs sous-régions et lieux enfants de manière récursive.

        Note:
            La hiérarchie est récursive : chaque enfant peut lui-même avoir des enfants.
            Les régions ont un polygon (region_shape), les lieux ont un point (marker_location).
        """
        regions_data = facade.get_all_regions_with_hierarchy()

        return {
            "success": True,
            "data": regions_data
        }, 200

#-------------------- REGIONS - par ID -------------------------

@api.route('/regions/<int:region_id>')
class RegionDetail(Resource):
    """Gestion d'une région spécifique avec sa hiérarchie."""
    def get(self, region_id):
        """
        Récupère UNE région spécifique avec sa hiérarchie complète

        Cette méthode retourne les détails d'une région particulière,
        incluant tous ses enfants et descendants de manière récursive.

        Args:
            region_id (int): Identifiant unique de la région

        Note:
            Cette route est utile pour charger dynamiquement les détails
            d'une région au clic sur la carte.
        """
        region_data = facade.get_region_by_id_with_hierarchy(region_id)

        if not region_data:
            return {
                "success": False,
                "error": "Région non trouvée"
            }, 404

        return {
            "success": True,
            "data": region_data
        }, 200


#--------------------- PLACES - Route marker par ID ------------------------

@api.route('/places/<int:place_id>')
class PlaceDetail(Resource):
    """Gestion d'un lieu spécifique (marqueur sur la carte)."""
    def get(self, place_id):
        """
        Récupère un lieu spécifique avec ses informations de base.

        Cette méthode retourne les détails d'un lieu particulier
        (ville, village, forteresse, port, etc.) avec sa position sur la carte.

        Args:
            place_id (int): Identifiant unique du lieu

        Note:
            Pour obtenir les descriptions détaillées d'un lieu, utilisez plutôt
            l'endpoint /api/descriptions/<entity_type>/<entity_id>.
        """
        place_data = facade.get_place_by_id(place_id)

        if not place_data:
            return {
                "success": False,
                "error": "Lieu non trouvé"
            }, 404

        return {
            "success": True,
            "data": place_data
        }, 200


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
