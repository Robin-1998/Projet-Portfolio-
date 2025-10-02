from flask import request, jsonify
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models import user
from flask_restx import Namespace, Resource

api = Namespace('users', description='Users operations')

# ---------- ROUTE POST /users ---------- Lister tous les utilisateurs
@api.route("/")
class UserList(Resource):
    def post(self):
        data = request.json
        if not data:
            return ({"error": "Données manquantes"}), 400

        try:
            new_user = facade.create_user(data)
            return ({
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "is_admin": new_user.is_admin
            }), 201

        except ValueError as error:
            return ({"error": str(error)}), 400

# ---------- ROUTE GET /users ---------- Récupérer tous les utilisateurs
    def get(self):
        users = facade.get_all_users()
        if not users:
            return ({"error": "No users found"}), 404

        users_list = [{
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        } for user in users]

        return (users_list), 200


# ---------- ROUTE GET /users ---------- Récupérer un utilisateur par ID
@api.route('/<int:user_id>')
class UserResource(Resource):
    def get_user(self, user_id):
        user = facade.get_users(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }), 200

# ---------- ROUTE PUT /users/<id> ---------- Mettre à jour un utilisateur (seul l’utilisateur peut mettre à jour ses données)
    @jwt_required()
    def put(self, user_id):
        data = request.json
        if not data:
            return jsonify({"error": "Missing data"}), 400

        current_user = get_jwt_identity()
        try:
            user = facade.update_user(user_id, current_user["id"], data)
        except PermissionError as e:
            return jsonify({"error": str(e)}), 403
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        return jsonify({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }), 200
