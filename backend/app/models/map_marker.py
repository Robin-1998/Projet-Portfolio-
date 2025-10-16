from backend.app.models.basemodel import BaseModel
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from backend.app import db
from sqlalchemy.orm import validates
from geoalchemy2.elements import WKTElement


class MapMarker(BaseModel):
    """
    Modèle pour les marqueurs sur la carte (via POSTGIS)
    """

    __tablename__ = "map_marker"

    name = db.Column(db.String(100), nullable=False)
    location = db.Column(Geometry('POINT', srid=0), nullable=False)
    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))

    place = db.relationship('PlaceMap', back_populates='map_markers')

    def __init__(self, name, location, place_id):
        super().__init__()
        self.name = name
        self.location = location
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
            "geometry": {
                "type": "Point",
                "coordinates": [geom.x, geom.y]
            }
        }
