"""
Module de gestion des utilisateurs

Ce module contient les endpoints REST permettant de créer, consulter et modifier
des comptes utilisateurs. Il gère l'inscription, la consultation des profils,
et la mise à jour des informations personnelles.
"""

from flask import request
from backend.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource

api = Namespace('users', description='Users operations')

# ---------- ROUTE POST /users ---------- Lister tous les utilisateurs
@api.route("/")
class UserList(Resource):
    """Gestion de la liste des utilisateurs (création et consultation)."""
    def post(self):
        """
        Crée un nouveau compte utilisateur (inscription).

        Cette méthode permet de créer un nouveau compte utilisateur
        avec les informations de base (nom, prénom, email, mot de passe).

        Note:
            - Le mot de passe est automatiquement hashé avant stockage
            - L'email doit être unique dans le système
            - Le mot de passe n'est jamais retourné dans la réponse
        """
        data = request.json
        if not data:
            return {"error": "Données manquantes"}, 400

        try:
            # Création de l'utilisateur via la facade
            new_user = facade.create_user(data)

            # Retour des informations (sans le mot de passe)
            return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "is_admin": new_user.is_admin
            }, 201

        except ValueError as error:
            return ({"error": str(error)}), 400

# ---------- ROUTE GET /users ---------- Récupérer tous les utilisateurs
    def get(self):
        """
        Récupère la liste de tous les utilisateurs.

        Cette méthode retourne la liste complète de tous les utilisateurs
        enregistrés dans le système.

        Note:
            Cette route est publique et ne nécessite pas d'authentification.
            Les mots de passe ne sont jamais inclus dans la réponse.
        """
        users = facade.get_all_user()
        if not users:
            return {"error": "No users found"}, 404

        return users, 200


# ---------- ROUTE GET /users ---------- Récupérer un utilisateur par ID
@api.route('/<int:user_id>')
class UserResource(Resource):
    """Gestion d'un utilisateur spécifique (consultation et modification)."""
    def get(self, user_id):
        """
        Récupère les informations d'un utilisateur spécifique.

        Cette méthode retourne les détails d'un utilisateur identifié par son ID.

        Args:
            user_id (int): Identifiant unique de l'utilisateur

        Note:
            Cette route est publique et ne nécessite pas d'authentification.
            Utile pour afficher les profils publics des utilisateurs.
        """
        # Récupération de l'utilisateur par ID
        user = facade.get_users(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }, 200

# ---------- ROUTE PUT /users/<id> ---------- Mettre à jour un utilisateur (seul l’utilisateur peut mettre à jour ses données)
    @jwt_required()
    def put(self, user_id):
        """
        Met à jour les informations d'un utilisateur.

        Cette méthode permet à un utilisateur authentifié de modifier
        ses propres informations personnelles. Un utilisateur ne peut
        modifier que son propre compte.

        Authentication:
            Requiert un token JWT valide. L'utilisateur ne peut modifier
            que son propre profil (sauf administrateurs).

        Args:
            user_id (int): Identifiant unique de l'utilisateur à modifier

        Code Erreur :
            PermissionError: Si l'utilisateur tente de modifier un compte qui n'est pas le sien
            ValueError: Si les données fournies sont invalides (email déjà utilisé, etc.)

        Note:
            - Un utilisateur ne peut modifier que son propre profil
            - Le nouveau mot de passe est automatiquement hashé
            - Si l'email est modifié, il doit rester unique dans le système
        """
        data = request.json
        if not data:
            return {"error": "Missing data"}, 400

        # Récupération de l'identité de l'utilisateur connecté
        current_user = get_jwt_identity()
        try:
            # Tentative de mise à jour
            # La facade vérifie que current_user["id"] == user_id
            user = facade.update_user(user_id, current_user["id"], data)
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }, 200
