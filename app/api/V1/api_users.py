from flask import request, jsonify
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

# ---------- ROUTE POST /users ---------- Lister tous les utilisateurs
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    try:
        new_user = facade.create_user(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin
    }), 201


# ---------- ROUTE GET /users ---------- Récupérer tous les utilisateurs
@app.route("/users", methods=["GET"])
def get_all_users():
    users = facade.get_all()
    if not users:
        return jsonify({"error": "No users found"}), 404

    users_list = [{
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin
    } for user in users]

    return jsonify(users_list), 200


# ---------- ROUTE GET /users ---------- Récupérer un utilisateur par ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = facade.get_user(user_id)
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
@app.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
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
