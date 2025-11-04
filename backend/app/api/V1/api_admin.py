"""
Module des routes d'administration
Ce module contient des endpoints REST (POST / PUT / DELETE)
permettant aux admin seulement de gérer les utilisateurs de l'appli
(supprimer un user / mettre à jour le profil d'un utilisateur 
/ créer un nouvel utilisateur admin)

Note du 29/10/2025 : le côté Admin n'a pas encore été implémenté sur le front,
il sera fait pour le RNCP
"""
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from backend.app.services import facade

api = Namespace('admin', description='Admin operations')

# ---------- ROUTE POST /admin/users ---------- Création d'un utilisateur admin
@api.route('/users/')
class AdminUserCreate(Resource):
    """Ressource pour la création d'utilisateurs par les administrateurs."""
    @jwt_required()
    def post(self):
        """
        Créer un nouvel utilisateur (via un admin)

        Cette fonction vérifie d'abord si l'utilisateur admin est connecté
        depuis son token. Des condition permmette de vérifier
        s'il à bien les privilèges admin, valide que les données soit correct,
        puis créé un user à l'aide de la fonction create_user stocké en facade

        Code Erreur:
            403: Si l'utilisateur n'a pas les privilèges administrateur
            400: Si les données sont manquantes ou invalides
            500: En cas d'erreur serveur inattendue
        """
        # On récupère l'identité de l'utilisateur connecté depuis son token
        current_user = get_jwt_identity()

        # Si l'utilisateur n'est pas un administrateur, on retourne une erreur
        if not current_user.get('is_admin'):
            return {"error": "Privilèges d'administrateur requis"}, 403

        # stockage de request.json dans data car permet d'échanger les données
        # entre un client et un serveur (converti)
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
    """Ressource pour la modification et suppression d'utilisateurs par les administrateurs."""
    @jwt_required()
    def put(self, user_id):
        """
        Mettre à jour un utilisateur existant (avia un admin).

        Permet à un administrateur de modifier les informations d'un utilisateur.

        Args:
            user_id (str): Identifiant de l'utilisateur à modifier

        Code Erreur:
            403: Si l'utilisateur n'a pas les privilèges ou tente une action interdite
            400: Si les données sont invalides ou introuvables
            500: En cas d'erreur serveur inattendue
        """
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

        # Retour des informations de l'utilisateur mis à jour
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }, 200

    @jwt_required()
    def delete(self, user_id):
        """
        Supprimer un utilisateur existant (via un admin).

        Permet à un administrateur de supprimer définitivement un compte utilisateur.
        la fonction delete_user est appelé depuis la facade pour la mise à jour
        Cette action est irréversible.

        Args:
            user_id (str): Identifiant de l'utilisateur à supprimer

        Code Erreur:
            403: Si l'utilisateur n'a pas les privilèges administrateur
            404: Si l'utilisateur à supprimer n'existe pas
            500: En cas d'erreur serveur inattendue
        """
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
