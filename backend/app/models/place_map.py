from backend.app.models.basemodel import BaseModel
from backend.app import db
from sqlalchemy.orm import validates


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
            'region',
            'foret',
            'montagne',
            'forteresse',
            'ville',
            'capitale',
            'eau',
            'ruine',
            'dark',
            'mine',
            'port',
            'pont',
            'plaine',
            'chemin',
            'monument',
            'special',
            'default',
            name="place_enum",
            native_enum=False,
            create_type=False
        ),
        nullable=False
    )
    description = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))
    image_url = db.Column(db.String(500), nullable=True)

    map_regions = db.relationship('MapRegion', back_populates='place', cascade='all, delete-orphan', lazy='select')
    map_markers = db.relationship('MapMarker', back_populates='place', cascade='all, delete-orphan', lazy='select')

    def __init__(self, title, type_place, description, parent_id):
        super().__init__()
        self.title = title
        self.type_place = type_place
        self.description = description
        self.parent_id = parent_id
        self.image_url = image_url

    @validates("title", "description")
    def validate_non_empty(self, key, value):
        """Empêcher les champs vides ou None."""
        if not value or not str(value).strip():
            raise ValueError(f"Le champ '{key}' ne peut pas être vide.")
        return value

    @validates("type_place")
    def validate_type_place(self, key, value):
        """Vérifier que le type_place est valide."""
        valid_types = {"Région", "Ville", "Village", "Forteresse", "Mer", "Lac/Marais", "Rivière"}
        if value not in valid_types:
            raise ValueError(f"Type de lieu invalide : '{value}'.")
        return value

    def to_dict(self, include_geometry=False):
        data = {
            "id": self.id,
            "title": self.title,
            "type_place": self.type_place,
            "description": self.description,
            "image_url": self.image_url,
            "parent_id": self.parent_id
        }

        if include_geometry:
            data["markers"] = [marker.to_dict() for marker in self.map_markers]
            data["regions"] = [region.to_dict() for region in self.map_regions]

        return data

PlaceMap.parent = db.relationship('PlaceMap', remote_side=[PlaceMap.id], backref='children')
