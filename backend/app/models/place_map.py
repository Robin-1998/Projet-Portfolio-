"""
Module contenant le modèle de chaque lieu
Chaque lieu (ville, forêt, région, etc.) peut être visualisé sur une carte via des marqueurs ou des polygones PostGIS.

Ce modèle hérite de `BaseModel`, qui fournit les attributs communs (id, timestamps, etc.).
"""
from backend.app.models.basemodel import BaseModel
from backend.app import db
from sqlalchemy.orm import validates


class PlaceMap(BaseModel):
    """
    Modèle représentant un lieu géographique affichable sur une carte.

    Un lieu peut être :
    - ponctuel (ville, forêt, ruine...) via un marqueur PostGIS,
    - ou étendu (région, montagne...) via un polygone PostGIS.

        info importante
        SQLAlchemy doit connaître les valeurs possibles de l'enum dans le code Python, pour pouvoir :
        valider les entrées avant insertion (type safety),
        sérialiser/désérialiser correctement les données,
        générer le mapping entre Postgres et Python,
        éviter les erreurs ORM à l'exécution.

    Notes importantes :
        - SQLAlchemy doit connaître toutes les valeurs possibles de l'enum `type_place`
          pour effectuer correctement les vérifications et le mapping ORM.
        - Les validations assurent que les champs critiques ne sont pas vides
          et que le type du lieu est cohérent.
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

    # ---------------------
    # Relations ORM
    # ---------------------

    map_regions = db.relationship('MapRegion', back_populates='place', cascade='all, delete-orphan', lazy='select')
    map_markers = db.relationship('MapMarker', back_populates='place', cascade='all, delete-orphan', lazy='select')

    def __init__(self, title, type_place, description, parent_id, image_url):
        super().__init__()
        self.title = title
        self.type_place = type_place
        self.description = description
        self.parent_id = parent_id
        self.image_url = image_url

    # ---------------------
    # Validations des champs
    # ---------------------

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
        """
        Sérialise l'objet PlaceMap en dictionnaire JSON-compatible.

        Args:
            include_geometry (bool): Si True, inclut les marqueurs et régions liés.
        """
        data = {
            "id": self.id,
            "title": self.title,
            "type_place": self.type_place,
            "description": self.description,
            "image_url": self.image_url,
            "parent_id": self.parent_id
        }

        # Inclure la géométrie uniquement si demandé
        # Le paramètre include_geometry est un booléen optionnel (par défaut False) 
        # qui permet de choisir si tu veux inclure ces données dans le dictionnaire.

        if include_geometry:
            data["markers"] = [marker.to_dict() for marker in self.map_markers]
            data["regions"] = [region.to_dict() for region in self.map_regions]

        return data
# ---------------------
# Relation auto-référencée : un lieu peut avoir un parent et des enfants
# ---------------------

PlaceMap.parent = db.relationship('PlaceMap', remote_side=[PlaceMap.id], backref='children')
