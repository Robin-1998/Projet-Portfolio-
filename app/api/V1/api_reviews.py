from flask import request
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models import user
from flask_restx import Namespace, Resource

api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    def post(self):
        """Envoie d'un nouveau commentaire"""
        review_data = request.json
        if not review_data:
            return {"error": "Données manquantes"}, 400

        # Récupération de l'utilisateur connecté
        user_identity = get_jwt_identity()
        user_id = user_identity.get("id")
        
        # Récupération de l'ID de l'image depuis les données envoyées
        image_post_id = review_data.get('image_post_id')

        # Présence de l'id de l'image obligatoire
        if not image_post_id:
            return {'error': 'image_post_id manquant'}, 400

        try:
            # Vérifie que l'utilisateur existe
            user = facade.get_user_by_id(user_id)
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404

            # Vérifie que l'image existe
            image = facade.get_post_image(image_post_id)
            if not image:
                return {'error': 'Image non trouvée'}, 404

            # Récupère toutes les reviews existantes pour cette image
            existing_reviews = facade.get_reviews_by_image(image_post_id) or []

            # Vérifie si l'utilisateur a déjà posté une review pour cette image
            for rev in existing_reviews:
                if rev.user and str(rev.user_id) == str(user_id):
                    return {'error': 'Vous avez déjà laissé un commentaire sur cette image'}, 400

            # Prépare les données avec le bon nom de champ
            # IMPORTANT: Votre facade attend 'post_image_id', pas 'image_post_id'
            review_create_data = {
                'user_id': user_id,
                'post_image_id': image_post_id,  # Nom attendu par la facade
                'comment': review_data.get('comment')
            }

            # Crée la review
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
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<int:review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id):
        review = facade.get_review(review_id)
        
        if review.user is not None:
            user_data = review.user.to_dict()
        else:
            user_data = None

        if review.image_post is not None: 
            image_post_data = review.image_post.to_dict()
        else:
            image_post_data = None

        return {
        'id': review.id,
        'comment': review.text,
        'user': user_data,
        'image_post': image_post_data
    }, 200

    def put (self, review_id):
        review_data = request.json
        if not review_data:
            return {'erreur': 'Commentaire non trouvé'}, 404

        try:
            # Vérifie si la review existe
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Commentaire non trouvé'}, 404

            # Vérifie que l'utilisateur connecté est le propriétaire
            user_id = get_jwt_identity()["id"]
            if not review.user_id or str(review.user_id) != str(user_id):
                return {"error": "Action non autorisée"}, 403

            # Valide les données fournies
            if 'comment' in review_data:
                comment = review_data['comment'].strip()
                if not comment:
                    return {'error': 'Le commentaire ne peut pas être vide'}, 400

            # Met à jour la review via la façade
            updated_review = facade.update_review(review_id, review_data)

            # Retourne la review mise à jour
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
        """ supprimer un commentaire (avec l'ID) """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Commentaire non trouvé'}, 404

        # Étape 2 : Vérifier que l'utilisateur connecté est bien le propriétaire
        user_id = get_jwt_identity()["id"]
        if not review.user or str(review.user.id) != str(user_id):
            return {"erreur": " Action non autorisé"}, 403

        # Étape 3 : delete the review
        facade.delete_review(review_id)
        return {'message': 'Commentaire supprimé'}, 200
