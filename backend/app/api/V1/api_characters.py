from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

api = Namespace('characters', description='Opérations de lecture sur les personnages')

@api.route("/")
class CharacterList(Resource):
    def get(self):
        characters = facade.get_all_characters()
        return [character.to_dict() for character in characters], 200

@api.route("/<int:character_id>")
class CharacterDetail(Resource):
    def get(self, character_id):
        try:
            character = facade.get_character(character_id)
            return character.to_dict(), 200
        except ValueError as error:
            return {"error": str(error)}, 404

"""
from flask_restx import Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

# Namespace characters
api = Namespace('characters', description='Opérations de lecture sur les personnages')

# Création d'un parseur d'arguments pour récupérer race_id dans la requête GET
parser = reqparse.RequestParser()
# Le parser sert à extraire et valider facilement les paramètres envoyés dans la requête HTTP,
# ici il récupère le paramètre optionnel 'race_id' en s'assurant que c'est un entier.
parser.add_argument('race_id', type=int, required=False, help='ID de la race')

@api.route("/")
class CharacterList(Resource):
    def get(self):
        args = parser.parse_args()
        race_id = args.get("race_id")

        if race_id:
            characters = facade.get_characters_by_race(race_id)
        else:
            characters = facade.get_all_characters()

        return [character.to_dict() for character in characters], 200
"""
