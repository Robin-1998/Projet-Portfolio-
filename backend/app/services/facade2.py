from backend.app.models.race import Race
from backend.app.models.character import Character
from backend.app.models.history import History
from backend.app.models.image_post import ImagePost
from backend.app.models.place_map import PlaceMap
from backend.app.models.map_region import MapRegion
from backend.app.models.map_marker import MapMarker
from sqlalchemy.orm import joinedload
from geoalchemy2.shape import to_shape
from backend.app.models.entity_description import EntityDescription
from backend.app.models.relation_type import RelationType

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
        Retourne markers et regions avec leurs descriptions depuis PlaceMap
        """
        from sqlalchemy.orm import joinedload
        from geoalchemy2.shape import to_shape

        # Récupérer les markers avec eager loading de la relation place
        markers = db.session.query(MapMarker).options(
            joinedload(MapMarker.place)
        ).all()

        # Récupérer les regions avec eager loading de la relation place
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
        Récupère les informations détaillées d'un lieu incluant :
        - Les infos de base depuis PlaceMap
        - Les sections détaillées depuis EntityDescription

        Args:
            place_id: ID du Place

        Returns:
            Dict avec structure :
            {
                "id": 42,
                "title": "Forteresse de Kar-Dun",
                "type_place": "forteresse",
                "description": "...",
                "image_url": "/images/...",
                "details": {
                    "population": 2000,
                    "climate": "Montagnard",
                    ...
                },
                "detailed_sections": [
                    {
                        "id": 1,
                        "title": "Architecture",
                        "content": "...",
                        "image_url": "/images/...",
                        "order_index": 1,
                        "relation_type": "Construit par"
                    },
                    ...
                ]
            }
        """
        # On récupère le lieu de base
        place = db.session.query(PlaceMap).filter_by(id=place_id).first()

        if not place:
            return None

        # On récupère les descriptions détaillées lié à ce lieu
        descriptions = db.session.query(EntityDescription).outerjoin(
            RelationType, EntityDescription.relation_type_id == RelationType.id
        ).filter(
            EntityDescription.entity_type == 'place',
            EntityDescription.entity_id == place_id
        ).order_by(EntityDescription.order_index).all()

        # On formate les sections détaillées
        detailed_sections = []
        for desc in descriptions:
            detailed_sections.append({
                'id': desc.id,
                'title': desc.title,
                'content': desc.content,
                'image_url': desc.image_url if hasattr(desc, 'image_url') else None,
                'order_index': desc.order_index,
                'relation_type': desc.relation_type.name if desc.relation_type else None
            })

        # on renvoi l'objet
        return {
            'id': place.id,
            'title': place.title,
            'type_place': place.type_place,
            'description': place.description,
            'image_url': getattr(place, 'image_url', None),
            'details': {
                'population': getattr(place, 'population', None),
                'climate': getattr(place, 'climate', None),
                'founded_year': getattr(place, 'founded_year', None),
                'notable_features': getattr(place, 'notable_features', None)
            },
            'detailed_sections': detailed_sections
        }
