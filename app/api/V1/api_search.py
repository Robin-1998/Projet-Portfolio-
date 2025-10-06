from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services.facade2 import PortfolioFacade
from flask import request

facade = PortfolioFacade()

# Namespace character
api = Namespace('search', description='Recherche dans la base de données')

@api.route("/")
class SearchRessource(Resource):
    def get(self):
        query = request.args.get("q", "").strip()
        results = facade.search_all(query)
        return results, 200
