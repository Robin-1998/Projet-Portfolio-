"""
Module contenant le modèle des marqueurs de carte

Ce module définit la classe MapMarker, qui représente les points géographiques affichés sur la carte
(gestion via PostGIS et GeoAlchemy2). Chaque marqueur correspond à un lieu précis, associé à un type
(par exemple : forêt, montagne, forteresse, ville, ruine, etc.).

Les coordonnées sont stockées sous forme géographique (type POINT) dans la base de données,
ce qui permet des traitements géospatiaux (requêtes spatiales, affichage sur une carte, etc.).
"""
from backend.app.models.basemodel import BaseModel
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from backend.app import db
from sqlalchemy.orm import validates
from geoalchemy2.elements import WKTElement
from sqlalchemy import Enum
import enum

# Définir l'ENUM Python pour correspondre à votre ENUM PostgreSQL
class MarkerTypeEnum(enum.Enum):
    """Énumération des types de marqueurs disponibles sur la carte.

    Cette énumération doit correspondre à la définition ENUM utilisée dans PostgreSQL,
    afin d’assurer la cohérence entre la base et le modèle ORM.
    !! Si pas de cohérence dans les texte il n'y aura pas de contenu
    """
    foret = 'foret'
    montagne = 'montagne'
    forteresse = 'forteresse'
    ville = 'ville'
    capitale = 'capitale'
    eau = 'eau'
    ruine = 'ruine'
    dark = 'dark'
    mine = 'mine'
    port = 'port'
    pont = 'pont'
    plaine = 'plaine'
    chemin = 'chemin'
    monument = 'monument'
    special = 'special'
    default = 'default'

class MapMarker(BaseModel):
    """
    Modèle représentant un marqueur géographique sur la carte.

    Chaque instance correspond à un point géographique précis (coordonnées X/Y),
    défini via un objet `WKTElement` compatible avec PostGIS.  
    Le marqueur est associé à un lieu (`place`) et à un type (`type`) défini
    par l’énumération MarkerTypeEnum.
    """

    __tablename__ = "map_marker"

    name = db.Column(db.String(100), nullable=False)

    # Coordonnées géographiques (PostGIS POINT)
    # SRID 0 utilisé ici pour un système de coordonnées arbitraire (peut être modifié)
    location = db.Column(Geometry('POINT', srid=0), nullable=False)

    # Type du marqueur, basé sur l’ENUM MarkerTypeEnum
    type = db.Column(
        Enum(MarkerTypeEnum, name='marker_type', native_enum=True),
        nullable=False,
        default=MarkerTypeEnum.default
    )

    # Lien  vers un lieu existant (PlaceMap)
    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))
    place = db.relationship('PlaceMap', back_populates='map_markers')

    def __init__(self, name, location, type, place_id):
        """Initialise un marqueur géographique avec ses attributs principaux."""
        super().__init__()
        self.name = name
        self.location = location
        self.type = type
        self.place_id = place_id

    @validates("name")
    def validate_name(self, key, value):
        """Vérifier que le nom n'est pas vide."""
        if not value or not str(value).strip():
            raise ValueError("Le nom du marqueur ne peut pas être vide.")
        return value

    @validates("location")
    def validate_location(self, key, value):
        """Vérifier que la localisation est un WKTElement valide."""
        if not isinstance(value, WKTElement):
            raise ValueError("La location doit être un WKTElement valide.")
        return value

    def to_dict(self):
        """
        Conversion en dictionnaire avec coordonnées
        Le frontend utilisera ces données pour afficher le marqueur
        """
        geom = to_shape(self.location)

        return {
            "id": self.id,
            "name": self.name,
            "place_id": self.place_id,
            "type": self.type.value if self.type else 'default',
            "geometry": {
                "type": "Point",
                "coordinates": [geom.x, geom.y]
            }
        }
