"""
Module de gestion des posts d'images

Ce module contient les endpoints REST permettant de créer, consulter, modifier
et supprimer des posts d'images. Les images sont stockées en base64 dans la base
de données avec leur type MIME. Certaines opérations nécessitent une authentification JWT.
Ce module con
"""
from flask import request
from backend.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource
import base64

api = Namespace('images', description='Image post operations')


@api.route('/')
class ImagePostList(Resource):
    """Gestion de la liste des posts d'images (création et consultation)."""
    @jwt_required()
    def post(self):
        """
        Crée un nouveau post image
        
        Cette méthode permet à un utilisateur authentiifé de créer un nouveau 
        post contenant une image encodée en base64.

        Authentication:
            Requiert un token JWT valide.

        Note:
            L'image doit être encodée en base64 avant l'envoi.
            Le user_id est automatiquement récupéré depuis le token JWT.
        """
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
        """
        Liste tous les posts d'images
        
        Cette méthode retourne la liste complète de tous les posts d'images
        présents dans la base de données, avec les informations de l'utilisateur créateur.

        Note:
            Les images sont converties en Data URI pour permettre un affichage direct
            dans les balises HTML <img>.
        """
        try:
            images = facade.get_all_post_images()
            result = []

            for image in images:
                # Convertir le BYTEA en Base64 pour JSON
                b64 = base64.b64encode(image.image_data).decode('utf-8') if image.image_data else None
                image_data_uri = f"data:{image.image_mime_type};base64,{b64}" if b64 else None

                user_data = None
                if hasattr(image, 'user') and image.user:
                    user_data = {
                        'id': image.user.id,
                        'first_name': getattr(image.user, 'first_name', None),
                        'email': getattr(image.user, 'email', None)
                    }

                result.append({
                    'id': image.id,
                    'title': image.title,
                    'description': image.description,
                    'image_mime_type': image.image_mime_type,
                    'image_data': image_data_uri,
                    'user': user_data,
                    'created_at': image.created_at.isoformat() if hasattr(image, 'created_at') else None
                })

            return result, 200

        except Exception as e:
            return {"error": f"Erreur lors de la récupération: {str(e)}"}, 500


@api.route('/<int:image_id>')
class ImagePostResource(Resource):
    """Gestion d'un post d'image spécifique (consultation, modification, suppression)."""
    def get(self, image_id):
        """
        Récupère un post image spécifique.

        Cette méthode retourne les détails complets d'un post d'image,
        incluant l'image encodée et les informations de l'utilisateur créateur.

        Args:
            image_id (int): Identifiant unique du post image
        """
        try:
            image = facade.get_post_image(image_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404

            # Convertir le BYTEA en Base64
            b64 = base64.b64encode(image.image_data).decode('utf-8') if image.image_data else None
            image_data_uri = f"data:{image.image_mime_type};base64,{b64}" if b64 else None

            # Prépare les données utilisateur
            user_data = None
            if hasattr(image, 'user') and image.user:
                user_data = {
                    'id': image.user.id,
                    'first_name': getattr(image.user, 'first_name', None),
                    'email': getattr(image.user, 'email', None)
                }

            return {
                'id': image.id,
                'title': image.title,
                'description': image.description,
                'image_mime_type': image.image_mime_type,
                'image_data': image_data_uri,
                'user': user_data,
                'created_at': image.created_at.isoformat() if hasattr(image, 'created_at') else None
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500

# Note -> Hasattr : véirife si un objet possède un attribut donné
#      -> Getattr : récupère l'attribut ou retourne une valeur par défaut

    @jwt_required()
    def put(self, image_id):
        """
        Met à jour un post image
        
        Cette méthode permet à l'utilisateur créateur de modifier le titre,
        la description ou l'image d'un post existant.

        Authentication:
            Requiert un token JWT valide. Seul le créateur du post peut le modifier.

        Args:
            image_id (int): Identifiant unique du post image à modifier

        Request Body (JSON):
            {
                "title": str (optionnel) - Nouveau titre,
                "description": str (optionnel) - Nouvelle description,
                "image_data": str (optionnel) - Nouvelle image encodée en base64,
                "image_mime_type": str (optionnel) - Nouveau type MIME
            }

        Note:
            Seul l'utilisateur ayant créé le post peut le modifier.
        """
        update_data = request.json
        if not update_data:
            return {'error': 'Données manquantes'}, 400

        try:
            user_id = get_jwt_identity()["id"]
            image = facade.get_post_image(image_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404
            if str(image.user_id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

            updated_image = facade.update_image_post(image_id, user_id, update_data)

            # Convertir le BYTEA en Base64
            b64 = base64.b64encode(updated_image.image_data).decode('utf-8') if updated_image.image_data else None
            image_data_uri = f"data:{updated_image.image_mime_type};base64,{b64}" if b64 else None

            return {
                'image': {
                    'id': updated_image.id,
                    'title': updated_image.title,
                    'description': updated_image.description,
                    'image_mime_type': updated_image.image_mime_type,
                    'image_data': image_data_uri
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
        """
        Supprime un post image
        
        Cette méthode permet à l'utilisateur créateur de supprimer définitivement
        un post d'image.

        Authentication:
            Requiert un token JWT valide. Seul le créateur du post peut le supprimer.

        Args:
            image_id (int): Identifiant unique du post image à supprimer

        Warning:
            Cette action est irréversible. Le post et l'image seront définitivement supprimés.

        Note:
            Seul l'utilisateur ayant créé le post peut le supprimer.
        """
        try:
            user_id = get_jwt_identity()["id"]
            image = facade.get_post_image(image_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404
            if str(image.user_id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

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
        """
        Récupère tous les posts d'un utilisateur

        Cette méthode retourne la liste complète de tous les posts d'images
        créés par un utilisateur donné.

        Args:
            user_id (int): Identifiant unique de l'utilisateur
        
        Note:
            Cette route est publique et ne nécessite pas d'authentification.
            Les posts sont triés par date de création (du plus récent au plus ancien).
        """
        try:
            images = facade.get_post_images_by_user(user_id)
            result = []

            for image in images:
                # Convertir le BYTEA en Base64
                b64 = base64.b64encode(image.image_data).decode('utf-8') if image.image_data else None
                image_data_uri = f"data:{image.image_mime_type};base64,{b64}" if b64 else None

                result.append({
                    'id': image.id,
                    'title': image.title,
                    'description': image.description,
                    'image_mime_type': image.image_mime_type,
                    'image_data': image_data_uri,
                    'created_at': image.created_at.isoformat() if hasattr(image, 'created_at') else None
                })

            return result, 200

        except Exception as e:
            return {"error": f"Erreur lors de la récupération: {str(e)}"}, 500
