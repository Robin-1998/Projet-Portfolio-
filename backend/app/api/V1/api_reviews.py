from flask import request
from backend.app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

api = Namespace('reviews', description='Review operations')

# -------------------- Liste et création des reviews --------------------
@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    def post(self):
        """Envoie d'un nouveau commentaire"""
        review_data = request.json
        if not review_data:
            return {"error": "Données manquantes"}, 400

        user_identity = get_jwt_identity()
        user_id = user_identity.get("id")
        image_post_id = review_data.get('image_post_id')

        if not image_post_id:
            return {'error': 'image_post_id manquant'}, 400

        try:
            user = facade.get_user_by_id(user_id)
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404

            image = facade.get_post_image(image_post_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404

            existing_reviews = facade.get_reviews_by_image(image_post_id) or []
            for rev in existing_reviews:
                if rev.user and str(rev.user_id) == str(user_id):
                    return {'error': 'Vous avez déjà laissé un commentaire sur cette image'}, 400

            review_create_data = {
                'user_id': user_id,
                'image_post_id': image_post_id,
                'comment': review_data.get('comment')
            }

            new_review = facade.create_review(review_create_data)

            return {
                'id': new_review.id,
                'comment': new_review.comment,
                'user_id': new_review.user_id,
                'image_post_id': new_review.image_post_id
            }, 201

        except ValueError as error:
            return {"error": str(error)}, 400
        except Exception as e:
            return {"error": f"Erreur serveur: {str(e)}"}, 500

    def get(self):
        """Liste toutes les reviews"""
        try:
            reviews = facade.get_all_reviews()
            return reviews, 200
        except Exception as e:
            return {"error": f"Erreur serveur: {str(e)}"}, 500


# -------------------- Opérations sur une review spécifique --------------------
@api.route('/<int:review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id):
        """Récupère une review spécifique"""
        try:
            review = facade.get_review(review_id)
            return {
                'id': review.id,
                'comment': review.comment,
                'user_id': review.user_id,
                'image_post_id': review.image_post_id
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500

    @jwt_required()
    def put(self, review_id):
        """Met à jour une review"""
        review_data = request.json
        if not review_data:
            return {'error': 'Données manquantes'}, 400

        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Commentaire non trouvé'}, 404

            user_id = get_jwt_identity()["id"]
            if not review.user_id or str(review.user_id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

            if 'comment' in review_data and not review_data['comment'].strip():
                return {'error': 'Le commentaire ne peut pas être vide'}, 400

            updated_review = facade.update_review(review_id, review_data)

            return {
                'review': {
                    'id': updated_review.id,
                    'comment': updated_review.comment,
                    'user_id': updated_review.user_id,
                    'image_post_id': updated_review.image_post_id
                },
                'message': 'Commentaire correctement mis à jour'
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500

    @jwt_required()
    def delete(self, review_id):
        """Supprime un commentaire"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Commentaire non trouvé'}, 404

            user_id = get_jwt_identity()["id"]
            if not review.user or str(review.user.id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

            facade.delete_review(review_id)
            return {'message': 'Commentaire supprimé'}, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': f"Erreur serveur: {str(e)}"}, 500


# -------------------- Reviews par utilisateur --------------------
@api.route('/user/<int:user_id>')
class UserReviews(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            reviews = facade.get_reviews_by_user(user_id)
            if not reviews:
                return {'message': 'Aucune review trouvée pour cet utilisateur'}, 404
            return reviews, 200
        except Exception as e:
            return {'error': str(e)}, 500


# -------------------- Reviews par image_post --------------------
@api.route('/image/<int:image_id>')
class ReviewByImage(Resource):
    @jwt_required()
    def get(self, image_id):
        """Récupère tous les commentaires d'une image"""
        try:
            reviews = facade.get_reviews_by_image(image_id)
            if not reviews:
                return {"message": "Aucune review trouvée pour cette image"}, 404

            # Convertit les reviews en dictionnaire
            reviews_list = [
                {
                    "id": r.id,
                    "comment": r.comment,
                    "user_id": r.user_id,
                    "image_post_id": r.image_post_id,
                } for r in reviews
            ]
            return {"reviews": reviews_list}, 200

        except Exception as e:
            return {"error": str(e)}, 500
