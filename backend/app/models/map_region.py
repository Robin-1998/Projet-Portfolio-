"""
Module contenant le modèle des régions géographiques

Ce module définit la classe MapRegion, qui représente les régions sur la carte.
Chaque région est stockée sous forme géométrique (type POLYGON) dans la base de données
grâce à l’intégration de PostGIS et GeoAlchemy2.

Les régions permettent de définir des zones plus larges que les marqueurs individuels
(par exemple : un royaume, une forêt, une chaîne de montagnes, etc.), et peuvent être
associées à des lieux via la relation `place`.
Car une région est le parent de plusieurs villes ou autre entité
Ex: Gondor contient : Minas Tirith, champs de Pelenor, Osgiliath etc...
"""
from backend.app.models.basemodel import BaseModel
from backend.app import db
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import validates
from geoalchemy2.elements import WKTElement


class MapRegion(BaseModel):
    """
    Modèle représentant une région géographique sur la carte.

    Cette classe stocke et gère des formes polygonales (zones) définies
    via PostGIS pour permettre un affichage ou des calculs géospatiaux.
    Chaque région peut être associée à un lieu spécifique via `place_id`.
    """
    __tablename__ = "map_region"

    name = db.Column(db.String(100), nullable=False)

    # Forme géographique de la région (polygone PostGIS)
    shape_data = db.Column(Geometry('POLYGON', srid=0), nullable=False)

    # Lien vers un lieu associé
    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))
    place = db.relationship('PlaceMap', back_populates='map_regions')

    def __init__(self, name, shape_data, place_id):
        """Initialise une région avec son nom, sa forme géométrique et son lieu associé."""
        super().__init__()
        self.name = name
        self.shape_data = shape_data
        self.place_id = place_id

    @validates("name")
    def validate_name(self, key, value):
        """Vérifie que le nom de la région n'est pas vide."""
        if not value or not str(value).strip():
            raise ValueError("Le nom de la région ne peut pas être vide.")
        return value

    @validates("shape_data")
    def validate_shape_data(self, key, value):
        """Vérifier que la forme est un WKTElement valide."""
        if not isinstance(value, WKTElement):
            raise ValueError("La forme (shape_data) doit être un WKTElement valide.")
        return value

    def to_dict(self):
        """
        Convertit la région en dictionnaire JSON-sérialisable.

        Cette méthode extrait les coordonnées du polygone (via Shapely)
        pour fournir une structure compatible avec le format GeoJSON,
        utilisable directement par le frontend (ex: Leaflet, Mapbox).
        """
        geom = to_shape(self.shape_data)
        return {
            "id": self.id,
            "name": self.name,
            "place_id": self.place_id,
            "geometry": {
                "type": "Polygon",
                "coordinates": list(geom.exterior.coords)
            }
        }
