from backend.app.models.race import Race
from backend.app.models.character import Character
from backend.app.models.history import History
from backend.app.models.place_map import PlaceMap
from backend.app.models.map_region import MapRegion
from backend.app.models.map_marker import MapMarker
from sqlalchemy.orm import joinedload
from geoalchemy2.shape import to_shape
from backend.app.models.description import Description
from sqlalchemy import func

from backend.app import db

class PortfolioFacade:
    """
    Facade pour gérer les entités du portfolio : races, personnages, histoires, lieux, descriptions,
    images et recherche globale.
    Fournit des méthodes de lecture (get) et de recherche qui ne sont pas liés à l'utilisateur
    """

    # Note du 30/10/2025 -> fonctionalité SEARCH non implémenté

# -------------------------DESCRIPTION----------------------------------------

    def get_descriptions(self, entity_type, entity_id):
        """
        Récupère toutes les descriptions pour une entité donnée.

        Code Erreur :
            Aucun raise explicite ici, retourne simplement une liste vide si aucune description.
        """
        return (
            Description.query
            .filter(
                func.lower(Description.entity_type) == entity_type.lower(),
                Description.entity_id == entity_id
            )
            .order_by(Description.order_index)
            .all()
        )

# -------------------------RACES-----------------------------------------------

    def get_all_races(self):
        """ récupère toutes les races """
        return Race.query.all()

    def get_race(self, race_id):
        """ Récupère une race spécifique par son identifiant. """
        race = db.session.get(Race, race_id)
        if not race:
            raise ValueError(f"Race avec id {race_id} introuvable.")
        return race
# -------------------------CHARACTERS------------------------------------------

    def get_all_characters(self):
        """ Récupère tous les personnages. """
        return Character.query.all()

    def get_character(self, character_id):
        """ Récupère un personnage spécifique par son identifiant. """
        character = db.session.get(Character, character_id)
        if not character:
            raise ValueError(f"Character avec id {character_id} introuvable.")
        return character

# ------------------------- HISTORY ------------------------------------------

    def get_all_histories(self):
        """ Récupère toutes les histoires. """
        return History.query.all()

    def get_history(self, history_id):
        """ Récupère une histoire spécifique par son identifiant. """
        history = db.session.get(History, history_id)
        if not history:
            raise ValueError(f"History avec id {history_id} introuvable.")
        return history

#-------------------------- PLACE -----------------------------------------
    # -- Get marker des Place ou région
    @staticmethod
    def get_map_data():
        """
        Fournit une version "légère" des données pour initialiser la carte:
        - Tous les markers avec leur lieu
        - Toutes les régions avec leur lieu
        """
        # Récupérer tous les markers et leur Place associé (eager loading)
        markers = db.session.query(MapMarker).options(
            joinedload(MapMarker.place)
        ).all()

        # Récupérer toutes les régions et leur Place associé
        regions = db.session.query(MapRegion).options(
            joinedload(MapRegion.place)
        ).all()

        markers_data = []
        for marker in markers:
            geom = to_shape(marker.location)

            # Gérer le cas où place peut être None
            place = marker.place if marker.place else None

            markers_data.append({
                "id": marker.id,
                "name": place.title if place else f"Marker {marker.id}",
                "description": place.description if place else "Aucune description disponible",
                "type": marker.type.value if marker.type else "default",
                "place_id": marker.place_id,
                "geometry": {
                    "coordinates": [geom.x, geom.y]
                },
                "details": {}
            })

        regions_data = []
        for region in regions:
            geom = to_shape(region.shape_data)

            # Gérer le cas où place peut être None
            place = region.place if region.place else None

            regions_data.append({
                "id": region.id,
                "name": place.title if place else f"Region {region.id}",
                "description": place.description if place else "Aucune description disponible",
                "place_id": region.place_id,
                "geometry": {
                    "coordinates": list(geom.exterior.coords)
                },
                "details": {}
            })

        return {
            "markers": markers_data,
            "regions": regions_data
        }

# ------------------------- PLACE DETAILED INFO ------------------------------------------
    @staticmethod
    def get_place_detailed_info(place_id):
        """
        Récupère un lieu avec ses descriptions détaillées, triées par ordre.
        """
        place = db.session.query(PlaceMap).filter_by(id=place_id).first()
        if not place:
            return None

        # Récupérer les descriptions associées au lieu
        descriptions = (
            db.session.query(Description)
            .filter_by(entity_type='place', entity_id=place_id)
            .order_by(Description.order_index)
            .all()
        )

        return {
            **place.to_dict(),
            'detailed_sections': [desc.to_dict() for desc in descriptions]
        }
