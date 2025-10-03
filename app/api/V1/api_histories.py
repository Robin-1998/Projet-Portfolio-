from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

# Namespace histories
api = Namespace('histories', description='Opérations de lecture sur les races')

@api.route("/")
class historyList(Resource):
    def get(self):
        histories = facade.get_all_histories()
        return [history.to_dict() for history in histories], 200

@api.route("/<int:history_id>")
class HistoryDetail(Resource):
    def get(self, history_id):
        try:
            histories = facade.get_histories(history_id)
            return history.to_dict(), 200
        except ValueError as error:
            return {"error": str(error)}, 404
