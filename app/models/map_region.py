from app.models.basemodel import BaseModel
from app import db
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

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
