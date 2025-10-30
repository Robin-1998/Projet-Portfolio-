"""
Module de recherche globale via la db

Ce module contient l'endpoint REST permettant d'effectuer des recherches
dans l'ensemble des contenus de la base de données (personnages, lieux, races, etc.).
Il s'agit d'un endpoint en lecture seule (GET uniquement).

Note du 29/10/2025: Cette fonctionalité n'a pas été intégré sur le front
"""
from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade
from flask import request

facade = PortfolioFacade()

api = Namespace('search', description='Recherche dans la base de données')

@api.route('')
class SearchRessource(Resource):
    """Gestion de la recherche globale dans tous les contenus."""
    def get(self):
        """
        Effectue une recherche globale dans tous les contenus de la base de données.

        Cette méthode permet de rechercher dans l'ensemble des entités
        (personnages, lieux, races, histoires, régions, etc.) en utilisant
        un terme de recherche fourni via le paramètre de requête 'q'.

        Query Parameters:
            q (str): Terme de recherche. Si vide ou absent, retourne une erreur.

        Code Erreur:
            ValueError: Si le terme de recherche est invalide ou vide

        Note:
            Le terme de recherche est automatiquement nettoyé avec .strip()
            pour éviter les espaces superflus.
        """
        query = request.args.get('q', '').strip()

        try:
            results = facade.search_all(query)
            return results, 200
        except ValueError as e:
            return {"error": str(e)}, 400
