from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

api = Namespace('images', description='Image post operations')

@api.route('/')
class ImagePostList(Resource):
    @jwt_required()
    def post(self):
        """Crée un nouveau post image"""
        image_data = request.json
        if not image_data:
            return {"error": "Données manquantes"}, 400

        # Récupération de l'utilisateur connecté
        user_identity = get_jwt_identity()
        user_id = user_identity.get("id")

        # Validation des champs requis
        required_fields = ['title', 'image_data', 'image_mime_type']
        for field in required_fields:
            if field not in image_data:
                return {'error': f'Le champ {field} est requis'}, 400

        try:
            # Prépare les données pour la création
            image_post_data = {
                'user_id': user_id,
                'title': image_data.get('title'),
                'description': image_data.get('description', ''),
                'image_data': image_data.get('image_data'),
                'image_mime_type': image_data.get('image_mime_type')
            }

            # Crée le post via la facade
            new_post = facade.create_image_post(image_post_data)

            return {
                'id': new_post.id,
                'title': new_post.title,
                'description': new_post.description,
                'user_id': new_post.user_id,
                'created_at': new_post.created_at.isoformat() if hasattr(new_post, 'created_at') else None,
                'message': 'Image postée avec succès'
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Erreur serveur: {str(e)}"}, 500

    def get(self):
        """Liste tous les posts d'images"""
        try:
            images = facade.get_all_post_images()
            return images, 200
        except Exception as e:
            return {"error": f"Erreur lors de la récupération: {str(e)}"}, 500


@api.route('/<int:image_id>')
class ImagePostResource(Resource):
    def get(self, image_id):
        """Récupère un post image spécifique"""
        try:
            image = facade.get_post_image(image_id)
            
            if not image:
                return {'error': 'Image non trouvée'}, 404

            # Prépare les données utilisateur
            user_data = None
            if image.user:
                user_data = {
                    'id': image.user.id,
                    'first_name': image.user.first_name if hasattr(image.user, 'first_name') else None,
                    'email': image.user.email if hasattr(image.user, 'email') else None
                }

            return {
                'id': image.id,
                'title': image.title,
                'description': image.description,
                'image_mime_type': image.image_mime_type,
                'user': user_data,
                'created_at': image.created_at.isoformat() if hasattr(image, 'created_at') else None
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500

    @jwt_required()
    def put(self, image_id):
        """Met à jour un post image"""
        update_data = request.json
        if not update_data:
            return {'error': 'Données manquantes'}, 400

        try:
            # Récupère l'utilisateur connecté
            user_id = get_jwt_identity()["id"]

            # Vérifie que l'image existe et appartient à l'utilisateur
            image = facade.get_post_image(image_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404

            if str(image.user_id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

            # Valide les données
            if 'title' in update_data and not update_data['title'].strip():
                return {'error': 'Le titre ne peut pas être vide'}, 400

            # Met à jour via la facade
            updated_image = facade.update_image_post(image_id, user_id, update_data)

            return {
                'image': {
                    'id': updated_image.id,
                    'title': updated_image.title,
                    'description': updated_image.description,
                    'image_mime_type': updated_image.image_mime_type
                },
                'message': 'Image mise à jour avec succès'
            }, 200

        except PermissionError as e:
            return {'error': str(e)}, 403
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500
    
    @jwt_required()
    def delete(self, image_id):
        """Supprime un post image"""
        try:
            # Récupère l'utilisateur connecté
            user_id = get_jwt_identity()["id"]

            # Vérifie que l'image existe
            image = facade.get_post_image(image_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404

            # Vérifie les permissions
            if str(image.user_id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

            # Supprime via la facade
            facade.delete_image_post(image_id, user_id)
            
            return {'message': 'Image supprimée avec succès'}, 200

        except PermissionError as e:
            return {'error': str(e)}, 403
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500


@api.route('/users/<int:user_id>')
class UserImagePosts(Resource):
    def get(self, user_id):
        """Récupère tous les posts d'un utilisateur"""
        try:
            images = facade.get_post_images_by_user(user_id)
            
            if not images:
                return [], 200

            # Formatte la réponse
            result = []
            for image in images:
                result.append({
                    'id': image.id,
                    'title': image.title,
                    'description': image.description,
                    'image_mime_type': image.image_mime_type,
                    'created_at': image.created_at.isoformat() if hasattr(image, 'created_at') else None
                })

            return result, 200

        except Exception as e:
            return {"error": f"Erreur lors de la récupération: {str(e)}"}, 500
