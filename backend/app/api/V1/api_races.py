from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

# Namespace races
api = Namespace('races', description='Opérations de lecture sur les races')

@api.route("/")
class RaceList(Resource):
    def get(self):
        races = facade.get_all_races()
        return [race.to_dict() for race in races], 200

@api.route("/<int:race_id>")
class RaceDetail(Resource):
    def get(self, race_id):
        try:
            race = facade.get_race(race_id)
            return race.to_dict(), 200
        except ValueError as error:
            return {"error": str(error)}, 404
