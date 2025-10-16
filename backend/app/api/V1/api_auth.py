from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.app.services import facade

# Namespace pour l'authentification
api = Namespace('auth', description='Authentication operations')

@api.route('/login')
class Login(Resource):
    def post(self):
        """Authentifier l'utilisateur et renvoyer un jeton JWT"""
        credentials = request.get_json()

        if not credentials or 'email' not in credentials or 'password' not in credentials:
            return {'error': 'Email et password obligatoire'}, 400

        try:
            # Récupère l'utilisateur via la façade
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

        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        return {'access_token': access_token}, 200

@api.route('/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        """Un point de terminaison protégé qui nécessite un jeton JWT valide"""
        current_user = get_jwt_identity()
        return {'message': f'Bonjour, user {current_user["id"]}'}, 200
