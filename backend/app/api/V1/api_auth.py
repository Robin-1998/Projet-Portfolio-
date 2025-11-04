"""
Module d'authentification

Ce module gère l'authentification des utilisateurs via JWT (JSON Web Tokens).
Il contient les endpoints pour la connexion et un exemple de route protégée.
"""

from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.app.services import facade

# Namespace pour l'authentification
api = Namespace('auth', description='Authentication operations')

@api.route('/login')
class Login(Resource):
    """Ressource pour l'authentification des utilisateurs."""
    def post(self):
        """
        Authentifier l'utilisateur et renvoie d'un jeton JWT
        
        Cette méthode vérifie d'abord les identifiants de l'utilisateurs
        (email et mdp) et génère par la suite un token JWT en cas de succès.
        Ce token devra être utilisé pour accéder aux routes protégés de l'API -> @jwt_required()

        Body (JSON):
            email (str): Adresse email de l'utilisateur
            password (str): Mot de passe en clair

        Codes Erreur:
            400: Si l'email ou le mot de passe sont manquants
            401: Si le mot de passe est incorrect
            404: Si l'email n'existe pas dans la base de données
            500: En cas d'erreur serveur inattendue
        """
        credentials = request.get_json()

        # Vérification que l'email et le mot de passe sont bien présents
        if not credentials or 'email' not in credentials or 'password' not in credentials:
            return {'error': 'Email et password obligatoire'}, 400

        try:
            # Récupération de l'utilisateur depuis la base de données via son email
            user = facade.get_user_by_email(credentials['email'])

            # Vérifie le mot de passe
            if not user.verify_password(credentials['password']):
                return {'error': 'Mot de passe incorrect'}, 401

        except ValueError as error:
            # Email inconnu → on renvoie un message clair
            return {'error': str(error)}, 404
        except Exception as error:
            # Erreur inattendue
            return {'error': f'Erreur interne : {str(error)}'}, 500

        # Création du token JWT contenant l'ID et le statut admin de l'utilisateur
        # Ce token sera utilisé pour authentifier les futures requêtes
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        return {'access_token': access_token}, 200

@api.route('/protected')
class Protected(Resource):
    """Ressource d'exemple d'un endpoint protégé nécessitant une authentification."""
    @jwt_required()
    def get(self):
        """
        Endpoint protégé nécessitant un jeton JWT valide.
        
        Cette route sert d'exemple pour démontrer comment protéger un endpoint.
        Seuls les utilisateurs authentifiés possédant un token JWT valide peuvent
        y accéder. Le décorateur @jwt_required() vérifie automatiquement la validité
        du token.
        
        Headers:
            Authorization (str): Bearer <access_token>
                Example:
                 # Requête
                 GET /auth/protected
                 Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

                 # Réponse
                 {
                     "message": "Bonjour, user abc123"
                 }
        """
        # Récupération des informations de l'utilisateur depuis le token JWT
        current_user = get_jwt_identity()
        return {'message': f'Bonjour, user {current_user["id"]}'}, 200
