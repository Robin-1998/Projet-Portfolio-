from app.models.basemodel import BaseModel
from app import db


class PlaceMap(BaseModel):
    """ N'importe quel utilisateur pourra voir le contenu de chaque lieux
        - lieu pour les villes/forêt/village identifié via un marqueur POSTGIS
        - lieu pour les régions via un tracé polygone DE POSTGIS

        info importante
        SQLAlchemy doit connaître les valeurs possibles de l'enum dans le code Python, pour pouvoir :
        valider les entrées avant insertion (type safety),
        sérialiser/désérialiser correctement les données,
        générer le mapping entre Postgres et Python,
        éviter les erreurs ORM à l'exécution.
    """
    __tablename__ = "places"

    title = db.Column(db.String(200), nullable=False)
    type_place = db.Column(
        db.Enum(
            'Région', 'Ville', 'Village', 'Forteresse', 'Mer', 'Lac/Marais', 'Rivière',
            name="place_enum",
            native_enum=False,
            create_type=False
        ),
        nullable=False
    )
    description = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))

    map_regions = db.relationship('MapRegion', back_populates='place', cascade='all, delete-orphan')
    map_markers = db.relationship('MapMarker', back_populates='place', cascade='all, delete-orphan')

    def __init__(self, title, type_place, description, parent_id):
        super().__init__()
        self.title = title
        self.type_place = type_place
        self.description = description
        self.parent_id = parent_id

    def to_dict(self, include_geometry=False):
        data = {
            "id": self.id,
            "title": self.title,
            "type_place": self.type_place,
            "description": self.description,
            "parent_id": self.parent_id
        }

        if include_geometry:
            data["markers"] = [marker.to_dict() for marker in self.map_markers]
            data["regions"] = [region.to_dict() for region in self.map_regions]

        return data

PlaceMap.parent = db.relationship('PlaceMap', remote_side=[PlaceMap.id], backref='children')
