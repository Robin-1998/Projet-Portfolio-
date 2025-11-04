from backend.app.models.race import Race
from backend.app.models.character import Character
from backend.app.models.history import History
from backend.app.models.image_post import ImagePost
from backend.app.models.place_map import PlaceMap
from backend.app.models.map_region import MapRegion
from backend.app.models.map_marker import MapMarker
from sqlalchemy.orm import joinedload
from geoalchemy2.shape import to_shape
from backend.app.models.relation_type import RelationType
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


# ------------------------- SEARCH ------------------------------------------

    def search_all(self, query):
        """
        Effectue une recherche globale sur plusieurs entités : personnages, races,
        histoires et posts d'images.

        Code Erreur:
            ValueError: Si le terme de recherche est vide
        """
        if not query or query.strip() == '':
            raise ValueError("Aucun terme de recherche fourni")

        # Recherche insensible à la casse dans chaque table
        characters = Character.query.filter(Character.name.ilike(f"%{query}%")).all()
        races = Race.query.filter(Race.name.ilike(f"%{query}%")).all()
        history = History.query.filter(History.name.ilike(f"%{query}%")).all()
        image_post = ImagePost.query.filter(ImagePost.title.ilike(f"%{query}%")).all()

        # Retour sous forme structurée (dict)
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
        Récupère toutes les régions (places de type 'Région') sans parent
        et construit leur hiérarchie complète d'enfants.
        """
        # Récupérer toutes les régions qui n'ont pas de parents (racines)
        regions = db.session.query(PlaceMap).join(
            MapRegion, PlaceMap.id == MapRegion.place_id
        ).filter(PlaceMap.parent_id.is_(None)).all()

        # Construire récursivement la hiérarchie pour chaque région
        return [PortfolioFacade._build_place_hierarchy(region) for region in regions]

# -- Get 1 region by ID avec enfant
    @staticmethod
    def get_region_by_id_with_hierarchy(region_id):
        """
        Récupère UNE région spécifique (map_region) avec sa hiérarchie complète

        Returns:
            Dict avec structure identique à get_all_regions_with_hierarchy
        """
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
        Récupère un lieu spécifique (ville, village, etc.) avec son marqueur
        et construit la hiérarchie si des enfants existent.

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
        Construit récursivement le dictionnaire d'un lieu avec ses enfants,
        sa forme géométrique si région, et son marqueur si présent.

        Returns:
            Dict avec toute la hiérarchie
        """
        # Forme géométrique du polygone si la place est une région
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

        # Construction récursive pour tous les enfants
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
        Fournit une version "légère" des données pour initialiser la carte:
        - Tous les markers avec leur lieu
        - Toutes les régions avec leur lieu
        """
        from sqlalchemy.orm import joinedload
        from geoalchemy2.shape import to_shape

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
