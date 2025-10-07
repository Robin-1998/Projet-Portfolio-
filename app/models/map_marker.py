from app.models.basemodel import BaseModel
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from app import db

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
