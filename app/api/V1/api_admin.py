from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

# ---------- ROUTE POST /admin/users ---------- Création d'un utilisateur admin
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {"error": "Privilèges d'administrateur requis"}, 403

        data = request.json
        if not data:
            return {"error": "Données manquantes"}, 400

        # Vérification du mot de passe
        password = data.get('password', '').strip()
        if not password:
            return {"error": "Le mot de passe ne peut pas être vide"}, 400

        try:
            new_user = facade.create_user(data)
        except ValueError as error:
            return {"error": str(error)}, 400
        except Exception as error:
            return {"error": f"Erreur interne : {str(error)}"}, 500

        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }, 201


# ---------- ROUTE PUT / DELETE /admin/users/<user_id> ----------
@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Mettre à jour un utilisateur existant (admin uniquement)."""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {"error": "Privilèges d'administrateur requis"}, 403

        data = request.json
        if not data:
            return {"error": "Données introuvables"}, 400

        try:
            # La façade gère toutes les validations (email unique, user existant, etc.)
            user = facade.update_user(user_id, current_user["id"], data)
        except PermissionError as error:
            return {"error": str(error)}, 403
        except ValueError as error:
            return {"error": str(error)}, 400
        except Exception as error:
            return {"error": f"Erreur interne : {str(error)}"}, 500

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }, 200

    @jwt_required()
    def delete(self, user_id):
        """Supprimer un utilisateur existant (admin uniquement)."""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {"error": "Privilèges d'administrateur requis"}, 403

        try:
            facade.delete_user(user_id)
        except ValueError as error:
            return {"error": str(error)}, 404
        except Exception as error:
            return {"error": f"Erreur interne : {str(error)}"}, 500

        return {"message": f"Utilisateur {user_id} supprimé avec succès"}, 200
