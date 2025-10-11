from app.models.basemodel import BaseModel
from app import db
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import validates
from geoalchemy2.elements import WKTElement


class MapRegion(BaseModel):
    """ Modèle pour les régions sur la carte (polygones via POSTGIS)"""
    __tablename__ = "map_region"

    name = db.Column(db.String(100), nullable=False)
    shape_data = db.Column(Geometry('POLYGON', srid=0), nullable=False)
    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))

    place = db.relationship('PlaceMap', back_populates='map_regions')

    def __init__(self, name, shape_data, place_id):
        super().__init__()
        self.name = name
        self.shape_data = shape_data
        self.place_id = place_id

    @validates("name")
    def validate_name(self, key, value):
        """Vérifier que le nom n'est pas vide."""
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
