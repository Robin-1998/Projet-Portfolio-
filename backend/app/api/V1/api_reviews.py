"""
Module de gestion des commentaires sur les posts d'images.

Ce module contient les endpoints REST permettant de créer, consulter, modifier
et supprimer des commentaires sur les images postées par les utilisateurs.
Les utilisateurs peuvent laisser un seul commentaire par image.

Note du 29/10/2025: Ils a été  implémenter le post/get de commentaires. Le
put / delete n'ont pas été ajouté.
"""

from flask import request
from backend.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

api = Namespace('reviews', description='Review operations')

# -------------------- Liste et création des reviews --------------------
@api.route('/')
class ReviewList(Resource):
    """Gestion de la liste des commentaires (création et consultation globale)."""
    @jwt_required()
    def post(self):
        """
        Crée un nouveau commentaire sur une image.

        Cette méthode permet à un utilisateur authentifié de laisser un commentaire
        sur un post d'image. Un utilisateur ne peut laisser qu'un seul commentaire
        par image.

        Authentication:
            Requiert un token JWT valide.

        Note:
            Un utilisateur ne peut laisser qu'un seul commentaire par image.
            Toute tentative de créer un second commentaire retournera une erreur 400.
        """
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
        """
        Liste tous les commentaires de la plateforme.

        Cette méthode retourne l'ensemble de tous les commentaires présents
        dans la base de données, toutes images confondues.

        Note:
            Cette route est publique et ne nécessite pas d'authentification.
        """
        try:
            reviews = facade.get_all_reviews()
            return reviews, 200
        except Exception as e:
            return {"error": f"Erreur serveur: {str(e)}"}, 500


# -------------------- Opérations sur une review spécifique --------------------
@api.route('/image/<int:image_id>')
class ReviewByImage(Resource):
    def get(self, image_id):
        """
        Récupère tous les commentaires d'une image spécifique.

        Cette méthode retourne la liste de tous les commentaires laissés
        sur un post d'image donné, avec les informations de l'auteur.

        Args:
            image_id (int): Identifiant unique du post d'image

        Note:
            Cette route est publique et ne nécessite pas d'authentification.
            Le nom de l'auteur affiché suit cette priorité :
            1. first_name si disponible
            2. email si first_name non disponible
            3. "Utilisateur" par défaut        """
        try:
            reviews = facade.get_reviews_by_image(image_id)
            if not reviews:
                return {"message": "Aucune review trouvée pour cette image"}, 404

            # Récupérer les infos utilisateur pour chaque review
            reviews_list = []
            for r in reviews:
                # Récupérer le nom de l'utilisateur
                author_name = 'Utilisateur'
                if hasattr(r, 'user') and r.user:
                    author_name = r.user.first_name or r.user.email or 'Utilisateur'

                reviews_list.append({
                    "id": r.id,
                    "comment": r.comment,
                    "user_id": r.user_id,
                    "author": author_name,
                    "image_post_id": r.image_post_id,
                    "created_at": r.created_at.isoformat() if hasattr(r, 'created_at') else None
                })

            return {"reviews": reviews_list}, 200

        except Exception as e:
            return {"error": str(e)}, 500

# -------------------- Opération sur un commentaire spécifique --------------------
@api.route('/<int:review_id>')
class ReviewResource(Resource):
    """Gestion d'un commentaire spécifique (modification et suppression)."""
    @jwt_required()
    def put(self, review_id):
        """
        Met à jour un commentaire existant
        
        Cette méthode permet à l'utilisateur auteur de modifier le contenu
        de son commentaire.

        Authentication:
            Requiert un token JWT valide. Seul l'auteur peut modifier son commentaire.

        Args:
            review_id (int): Identifiant unique du commentaire à modifier

        Note:
            Le commentaire ne peut pas être vide (validation avec .strip()).
            Seul l'auteur du commentaire peut le modifier.
        """
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
        """
        Supprime un commentaire
        
        Cette méthode permet à l'utilisateur auteur de supprimer définitivement
        son commentaire.

        Authentication:
            Requiert un token JWT valide. Seul l'auteur peut supprimer son commentaire.

        Args:
            review_id (int): Identifiant unique du commentaire à supprimer

        Warning:
            Cette action est irréversible. Le commentaire sera définitivement supprimé.

        Note:
            Seul l'auteur du commentaire peut le supprimer.
        """
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
    """Gestion des commentaires d'un utilisateur spécifique."""
    @jwt_required()
    def get(self, user_id):
        """
        Récupère tous les commentaires d'un utilisateur spécifique.

        Cette méthode retourne la liste de tous les commentaires laissés
        par un utilisateur donné.

        Authentication:
            Requiert un token JWT valide.

        Args:
            user_id (int): Identifiant unique de l'utilisateur

        Note:
            Cette route permet à un utilisateur de voir l'historique
            de tous ses commentaires.
        """
        try:
            reviews = facade.get_reviews_by_user(user_id)
            if not reviews:
                return {'message': 'Aucune review trouvée pour cet utilisateur'}, 404
            return reviews, 200
        except Exception as e:
            return {'error': str(e)}, 500
