from flask import request
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models import user
from flask_restx import Namespace, Resource

api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    def post(self):
        """ Envoie d'un nouveau commentaire"""
        review_data = request.json
        if not review_data:
            return {"error": "Données manquantes"}, 400

        user_identity = get_jwt_identity()
        user_id = user_identity.get("id")
        image_post_id = review_data.get('image_post_id')

        # présence de l'id de l'image et de l'utilisateur obligatoire
        if not user_id or not image_post_id:
            return {'erreur': 'user_id or image_post_id manquant'}, 400

        # On vérifie que l'utilisateur existe sinon on retourne une erreur
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'erreur': 'Utilisateur non trouvé'}, 400

        # On vérifie que l'image existe sinon on retourne une erreur
        image = facade.get_post_image(image_post_id)
        if not image:
            return {'erreur': 'Image non trouvé'}, 400

        # Récupère toutes les reviews existantes pour une image
        existing_reviews = facade.get_reviews_by_image(image_post_id) or []

        # Vérifie si l'utilisateur a déjà posté une review pour cette image
        for rev in existing_reviews:
            if rev.user and str(rev.user.id) == str(user_id):
                return {'error': 'Vous avez déjà laissé un commentaire'}, 400

        # Injecte l'user_id dans les données de review avant de créer
        review_data['user_id'] = user_id # Injection du user_id côté serveur

        try:
            new_review = facade.create_review(review_data)
        except ValueError as error:
            return {"error": str(error)}, 400
        return {
            'id': new_review.id,
            'comment': new_review.text,
            'user_id': new_review.user.id,
            'post_image_id': new_review.post_image_id.id
        }, 201

    def get(self):
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<reviews_id>')
class ReviewResource(Resource):
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

        # 1. Vérifier si la review existe
        review = facade.get_review(review_id)

        user_id = get_jwt_identity()["id"]
        if not review.user or str(review.user.id) != str(user_id):
            return {"erreur": "Action non autorisé"}, 403

        # 2. Valider les données fournies
        if 'text' in review_data:
            text = review_data['text'].strip()
            if not text:
                return {'erreur': 'Le texte ne peut pas être vide'}, 400

        # 3. Mettre à jour la review via la façade
        try:
            updated_review = facade.update_review(review_id, review_data)
        except Exception as e:
            # Capture toute erreur inattendue (ex: validation côté modèle)
            return {'erreur': str(e)}, 400

        # 4. Retourner la review mise à jour
        return {
            'review': {
                'id': updated_review.id,
                'comment': updated_review.text,
                'user': updated_review.user.id if updated_review.user else None,
                'image_post': updated_review.image_post.id if updated_review.image_post else None
            },
            'message': 'Commentaire correctement mis à jour'
        }, 200
    
    @jwt_required()
    def delete(self, review_id):
        """ supprimer un commentaire (avec l'ID) """
        review_delete = facade.get_review(review_id)

        # Étape 2 : Vérifier que l'utilisateur connecté est bien le propriétaire
        user_id = get_jwt_identity()["id"]
        if not review_delete.user or str(review_delete.user.id) != str(user_id):
            return {"erreur": " Action non autorisé"}, 403

        # Étape 3 : delete the review
        facade.delete_review(review_id)
        return {'message': 'Commentaire supprimé'}, 200
