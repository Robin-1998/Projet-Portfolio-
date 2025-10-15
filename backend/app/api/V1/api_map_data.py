from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

api = Namespace('map', description='API Carte interactive')


#-------------------- REGIONS - Routes principales -------------------------

@api.route('/regions')
class RegionsList(Resource):
    def get(self):
        """
        GET /api/map/regions
        Récupère TOUTES les régions avec leur hiérarchie complète d'enfants

        Retourne une liste de régions, chacune avec :
        - id, title, type_place, description
        - children[] : liste récursive de tous les enfants/petits-enfants
        - region_shape : coordonnées du polygone (si c'est une région)
        - marker_location : coordonnées du point (si c'est un lieu avec marqueur)
        """
        regions_data = facade.get_all_regions_with_hierarchy()

        return {
            "success": True,
            "data": regions_data
        }, 200

#-------------------- REGIONS - par ID -------------------------

@api.route('/regions/<int:region_id>')
class RegionDetail(Resource):
    def get(self, region_id):
        """
        GET /api/map/regions/<region_id>
        Récupère UNE région spécifique avec sa hiérarchie complète

        Retourne :
        - Les infos de la région (id, title, type_place, description)
        - children[] : tous les enfants/petits-enfants récursivement
        - region_shape : coordonnées du polygone
        - marker_location : null (car c'est une région)
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
    def get(self, place_id):
        """
        GET /api/map/places/<place_id>
        Récupère UN lieu spécifique (ville, village, etc.)

        Retourne :
        - Les infos du lieu (id, title, type_place, description)
        - marker_location : coordonnées du point
        - region_shape : null (car c'est un marqueur, pas une région)
        - children[] : liste vide ou enfants si applicable
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
    def get(self):
        """
        GET /api/map/data
        Récupère TOUTES les données pour initialiser la carte
        (Version légère sans détails, juste pour affichage initial)
        """
        map_data = facade.get_map_data()
        return {
            "success": True,
            "data": map_data
        }, 200
