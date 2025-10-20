from backend.app.models.race import Race
from backend.app.models.character import Character
from backend.app.models.history import History
from backend.app.models.image_post import ImagePost
from backend.app.models.place_map import PlaceMap
from backend.app.models.map_region import MapRegion
from backend.app.models.map_marker import MapMarker
from sqlalchemy.orm import joinedload
from geoalchemy2.shape import to_shape

from backend.app import db

class PortfolioFacade:
# -------------------------RACES-----------------------------------------------

    def get_all_races(self):
        return Race.query.all()

    def get_race(self, race_id):
        race = db.session.get(Race, race_id)
        if not race:
            raise ValueError(f"Race avec id {race_id} introuvable.")
        return race
    """
    def get_characters_by_race(self, race_id=None):
        query = Character.query

        if race_id is not None:
            query = query.filter(Character.race_id == race_id)

        return query.all()
    """
# -------------------------CHARACTERS------------------------------------------

    def get_all_characters(self):
        return Character.query.all()

    def get_character(self, character_id):
        character = db.session.get(Character, character_id)
        if not character:
            raise ValueError(f"Character avec id {character_id} introuvable.")
        return character

# ------------------------- HISTORY ------------------------------------------

    def get_all_histories(self):
        return History.query.all()

    def get_history(self, history_id):
        history = db.session.get(History, history_id)
        if not history:
            raise ValueError(f"History avec id {history_id} introuvable.")
        return history


# ------------------------- SEARCH ------------------------------------------

    def search_all(self, query):
        if not query or query.strip() == '':
            raise ValueError("Aucun terme de recherche fourni")

        characters = Character.query.filter(Character.name.ilike(f"%{query}%")).all()
        races = Race.query.filter(Race.name.ilike(f"%{query}%")).all()
        history = History.query.filter(History.name.ilike(f"%{query}%")).all()
        image_post = ImagePost.query.filter(ImagePost.title.ilike(f"%{query}%")).all()

        return {
            "query": query,
            "results": {
                "characters": [c.to_dict() for c in characters],
                "races": [r.to_dict() for r in races],
                "history": [h.to_dict() for h in history],
                "image_post": [i.to_dict() for i in image_post]
            }
        }

#-------------------------- PLACE -----------------------------------------
# -- Get all régions avec enfants
    @staticmethod
    def get_all_regions_with_hierarchy():
        """
        Récupère toutes les régions (places de type 'Région' qui ont un MapRegion)
        avec leur hiérarchie complète d'enfants

        Returns:
            Liste de dict avec structure :
            {
                "id": 1,
                "title": "Gondor",
                "type_place": "Région",
                "description": "...",
                "children": [...],  # récursif
                "region_shape": {...},  # coordonnées du polygone
                "marker_location": null
            }
        """
        # Récupérer toutes les régions (places qui ont un MapRegion et parent_id = None)
        regions = db.session.query(PlaceMap).join(
            MapRegion, PlaceMap.id == MapRegion.place_id
        ).filter(PlaceMap.parent_id.is_(None)).all()

        return [PortfolioFacade._build_place_hierarchy(region) for region in regions]

# -- Get 1 region by ID avec enfant
    @staticmethod
    def get_region_by_id_with_hierarchy(region_id):
        """
        Récupère UNE région spécifique avec sa hiérarchie complète

        Args:
            region_id: ID du MapRegion (pas du Place!)

        Returns:
            Dict avec structure identique à get_all_regions_with_hierarchy
        """
        # Récupérer le MapRegion et son Place associé
        map_region = db.session.query(MapRegion).options(
            joinedload(MapRegion.place)
        ).filter_by(id=region_id).first()

        if not map_region or not map_region.place:
            return None

        return PortfolioFacade._build_place_hierarchy(map_region.place)

# -- Get 1 Place by ID
    @staticmethod
    def get_place_by_id(place_id):
        """
        Récupère UN lieu spécifique (ville, village, etc. avec marqueur)

        Args:
            place_id: ID du Place

        Returns:
            Dict avec structure :
            {
                "id": 3,
                "title": "Minas Tirith",
                "type_place": "Ville",
                "description": "...",
                "children": [],
                "region_shape": null,
                "marker_location": {...}  # coordonnées du point
            }
        """
        place = db.session.query(PlaceMap).filter_by(id=place_id).first()

        if not place:
            return None

        return PortfolioFacade._build_place_hierarchy(place)

#-- Construit dictionnaire Région place
    @staticmethod
    def _build_place_hierarchy(place):
        """
        Construit récursivement la hiérarchie d'un lieu avec ses enfants

        Args:
            place: Instance de PlaceMap

        Returns:
            Dict avec toute la hiérarchie
        """
        # Récupérer les coordonnées du polygone (si région)
        region_shape = None
        if place.map_regions:
            region = place.map_regions[0]  # Un place n'a qu'une seule région
            geom = to_shape(region.shape_data)
            region_shape = {
                "type": "Polygon",
                "coordinates": list(geom.exterior.coords)
            }

        # Récupérer les coordonnées du marqueur (si lieu avec marqueur)
        marker_location = None
        if place.map_markers:
            marker = place.map_markers[0]  # Un place n'a qu'un seul marqueur
            geom = to_shape(marker.location)
            marker_location = {
                "type": "Point",
                "coordinates": [geom.x, geom.y]
            }

        # Construire la structure de base
        place_dict = {
            "id": place.id,
            "title": place.title,
            "type_place": place.type_place,
            "description": place.description,
            "children": [],
            "region_shape": region_shape,
            "marker_location": marker_location
        }

        # Récupérer et construire récursivement les enfants
        if place.children:
            place_dict["children"] = [
                PortfolioFacade._build_place_hierarchy(child)
                for child in place.children
            ]

        return place_dict


# -- Get marker des Place ou région
    @staticmethod
    def get_map_data():
        """
        Version légère pour l'initialisation de la carte
        Retourne juste les markers et regions sans détails
        """
        markers = db.session.query(MapMarker).all()
        regions = db.session.query(MapRegion).all()

        return {
            "markers": [marker.to_dict() for marker in markers],
            "regions": [region.to_dict() for region in regions]
        }
