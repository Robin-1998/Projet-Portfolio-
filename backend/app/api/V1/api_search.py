from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from backend.app.services.facade2 import PortfolioFacade
from flask import request

facade = PortfolioFacade()

# Namespace character
api = Namespace('search', description='Recherche dans la base de données')

@api.route('')
class SearchRessource(Resource):
    def get(self):
        """Recherche globale dans tous les contenus"""
        query = request.args.get('q', '').strip()

        try:
            results = facade.search_all(query)
            return results, 200
        except ValueError as e:
            return {"error": str(e)}, 400
