from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

# Namespace character
api = Namespace('characters', description='Opérations de lecture sur les races')

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
