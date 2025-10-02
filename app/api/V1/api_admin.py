from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """Créez un nouvel utilisateur avec des privilèges d'administrateur."""
        current_user = get_jwt_identity()
        # Vérification des droits d'administration
        if not current_user.get('is_admin'):
            return {"error": "Privilèges d'administrateur requis"}, 403

        # Récupération et traitement des données entrantes
        user_data = request.json
        email = user_data.get('email')

        # Vérification unicité de l'email
        if facade.get_user_by_email(email):
            return {'error': 'Email déjà enregistré'}, 400
        #---------------------------------------------------------------------
        """Enregistrez un nouvel utilisateur"""

        # Vérification manuelle du mot de passe (vide)
        password = user_data.get('password', '').strip()
        if not password:
            return {'error': 'Le mot de passe ne peut pas être vide'}, 400

        try:
            new_user_admin = facade.create_user(user_data)
        except ValueError as error :
            return {'error': str(error)}, 400
        # Retourne les info du nouvel utilisateur avec un code 201 ("created")
        return {
            'id': new_user_admin.id,
            'first_name': new_user_admin.first_name,
            'last_name': new_user_admin.last_name,
            'email': new_user_admin.email,
            'is_admin': new_user_admin.is_admin,
            }, 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Mettre à jour les détails d'un utilisateur existant."""
#--------------------------Code donnée de user--------------------------------#

        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {"error": "Privilèges d'administrateur requis"}, 403

        data = request.json
        email = data.get('email')

        # Garantir l’unicité des e-mails
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'E-mail déjà utilisé'}, 400

#-------------------------Notre code de user----------------------------------#

        # Logique pour mettre à jour les détails de l'utilisateur
        if not data:
            return {"error": "Données introuvables"}, 400

        #if str(current_user["id"]) != str(user_id):
            #return {'error': "Unauthorized action"}, 403

        user = facade.get_user(user_id)
        if not user:
            return {"error": "Utilisateur introuvable"}, 404

        try:
            user = facade.update_user(user_id, data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

# ajouter delete
