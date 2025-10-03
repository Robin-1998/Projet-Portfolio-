from app.models.user import User
from app.models.review import Review
from app.models.image_post import ImagePost
from app import db
from app.persistence.user_repository import UserRepository
from app.persistence.repository import Repository

# from app.persistence.repository import SQLAlchemyRepository

class PortfolioFacade:
    def __init__(self):
        self.user_repo = UserRepository()

# -------------------- Authentification de l'utilisateur --------------------

    def create_user(self, user_data):
        """ Création du compte utilisateur """
        try:
        # Vérifie si l'email existe déjà
            existing_user = self.user_repo.get_user_by_email(user_data.get('email'))
            if existing_user:
                raise ValueError(f"Un utilisateur avec l'email {user_data['email']} existe déjà.")
        # Si l'email n'existe pas, on créé un utilisateur
            if 'password' not in user_data or not user_data['password']:
                raise ValueError("Le mot de passe est requis pour la création de l'utilisateur.")
        # Si l'email n'existe pas, on créé un utilisateur
            user = User(**user_data)
            # user.hash_password(user_data['password']) DOUBLON ????
            self.user_repo.add(user)
            return user

        except ValueError:
            # Erreurs de validation ou logique métier
            db.session.rollback()
            raise

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    def login_user(self, email, password):
        try:
            # Validation des paramètres
            if not email or not password:
                raise ValueError("Email et mot de passe sont requis.")
            # Recherche l'utilisateur
            user = self.user_repo.get_user_by_email(email)
            if not user:
                raise ValueError("Email ou mot de passe incorrect.")
            # Vérifie le mot de passe
            if not user.verify_password(password):
                raise ValueError("Email ou mot de passe incorrect.")
            return user

        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f"Erreur lors de la connexion : {str(e)}")


    def get_users(self, user_id):
        """ On retourne un utilisateur par son ID """
        try:
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}.")
            return user

        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")

    def get_all_user(self):
        """ Liste tout les utilisateurs dans un format type dictionnaire """
        try:
            users = self.user_repo.get_all()
            return [user.to_dict() for user in users]

        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des utilisateurs : {str(e)}")

    def get_user_by_email(self, email):
        """ Cherche utilsateur à partir de son email """
        try:
            if not email:
                raise ValueError("L'email ne peut pas être vide.")
            user = self.user_repo.get_user_by_email(email)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'email {email}.")
            return user
        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche par email : {str(e)}")
    
    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son identifiant unique"""
        try:
            if not user_id:
                raise ValueError("L'identifiant utilisateur est requis.")
            user = self.user_repo.get_by_attribute('id', user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'id {user_id}.")
            return user
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche par ID : {str(e)}")

    def update_user(self, user_id, current_user_id, data):
        """
        Met à jour les données d'un utilisateur.

        IMPORTANT : Ne pas inclure 'password' dans data.
        Utilisez update_user_password() pour changer le mot de passe.

        Args:
            user_id: ID de l'utilisateur
            data (dict): Dictionnaire contenant les champs à mettre à jour

        Returns:
            User: L'objet utilisateur mis à jour

        Raises:
            ValueError: Si tentative de modification du mot de passe ou données invalides
        """
        try:
            # Sécurité : empêche la modification directe du mot de passe
            if 'password' in data:
                raise ValueError(
                    "Impossible de modifier le mot de passe via cette méthode. "
                    "Utilisez update_user_password() à la place."
                )

            # Sécurité : empêche la modification de l'ID
            if 'id' in data:
                del data['id']

            # Vérifie que l'utilisateur existe
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}.")

            current_user = self.user_repo.get(current_user_id)
            if not current_user:
                raise PermissionError("Utilisateur connecté invalide.")

            if user_id != current_user_id and not current_user.is_admin:
                raise PermissionError(
                    "Vous ne pouvez modifier que votre propre profil."
                )

            # Met à jour (le repository fait le commit)
            self.user_repo.update(user_id, data)

            # Récupère l'utilisateur mis à jour
            updated_user = self.user_repo.get(user_id)

            return updated_user

        except ValueError:
            db.session.rollback()
            raise

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la mise à jour : {str(e)}")

    def update_user_password(self, user_id, old_password, new_password):
        """
        Met à jour le mot de passe d'un utilisateur de manière sécurisée.

        Args:
            user_id: ID de l'utilisateur
            old_password (str): Ancien mot de passe pour vérification
            new_password (str): Nouveau mot de passe

        Returns:
            User: L'objet utilisateur mis à jour

        Raises:
            ValueError: Si l'ancien mot de passe est incorrect
        """
        try:
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}.")

            # Vérifie l'ancien mot de passe
            if not user.verify_password(old_password):
                raise ValueError("L'ancien mot de passe est incorrect.")

            # Met à jour avec le nouveau mot de passe (sera haché)
            user.update_password(new_password)
            db.session.commit()

            return user

        except ValueError:
            db.session.rollback()
            raise

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors du changement de mot de passe : {str(e)}")

    def delete_user(self, user_id):
        """
        Supprime un utilisateur (opération admin).

        Args:
            user_id: ID de l'utilisateur à supprimer

        Returns:
            bool: True si la suppression a réussi

        Raises:
            ValueError: Si l'utilisateur n'existe pas
        """
        try:
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}.")

            # Supprime l'utilisateur (le repository fait le commit)
            self.user_repo.delete(user_id)

            return True

        except ValueError:
            db.session.rollback()
            raise

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la suppression : {str(e)}")

# -------------------- Review --------------------

    def create_review(self, review_data):
        """ création d'un nouveau commentaire basé sur image + user """
        #récupération des IDS
        user_id = review_data.get('user_id')
        image_post_id = review_data.get('post_image_id')

        if not user_id:
            raise ValueError("user_id est requis")
        if not image_post_id:
            raise ValueError("post_image_id est requis")
        
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}")
        post_image = self.get_post_image(image_post_id)
        if not post_image:
            raise ValueError(f"Aucune image trouvé avec l'ID {image_post_id}")
        
        comment = review_data.get('comment')

        review = Review(
            comment=comment,
            user_id=user.id,
            image_post_id=post_image.id
        )

        self.review_repo.add(review)
        db.session.commit()
        return review
    
    def get_review(self, review_id):
        """ Liste un commentaire spécifique """
        try:
            review = self.review_repo.get(review_id)
            if not review:
                raise ValueError(f"Aucun commentaire trouvé avec l'ID {review_id}.")
            return review
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")

    def get_all_reviews(self):
        """ Liste tout les commentaires """
        try:
            reviews = self.review_repo.get_all()
            return [review.to_dict() for review in reviews]
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des commentaires : {str(e)}")

    def get_reviews_by_image(self, image_post_id):
        """ Retourne tous les commentaires liés à une image spécifique """
        return self.review_repo.get_by_post_image_id(image_post_id)
    
    def update_review(self, review_id, review_data):
        """ mettre à jour un commentaire """
        self.review_repo.update(review_id, review_data)
        review = self.review_repo.get(review_id)
        db.session.commit()
        return review
    
    def delete_review(self, review_id):
        """ supprime un commentaire """
        review = self.review_repo.get(review_id)
        if not review:
            return False  # Ne rien supprimer si l'ID est inconnu
        # Supprime la review
        self.review_repo.delete(review_id)
        db.session.commit()
        # Confirme qu'elle n'existe plus
        return True

# -------------------- Post_image  --------------------

    def get_post_image(self, image_post_id):
        """ retourne une image spécifique """
        try:
            image = self.image_post_repo.get(image_post_id)
            if not image:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {image_post_id}.")
            return image
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération de l'image : {str(e)}")

    """
    def delete_image_post(self, image_id, user_id):
        Supprime une image ET son fichier physique
        image = self.image_repo.get(image_id)

        # Vérification des permissions
        if image.user_id != user_id and not is_admin(user_id):
            raise PermissionError("Vous ne pouvez pas supprimer cette image")

        # Supprime le fichier physique
        os.remove(image.file_path)

        # Supprime de la base de données
        self.image_repo.delete(image_id)

    def update_review(self, review_id, data, user_id):
        Met à jour une review avec validation
        review = self.review_repo.get(review_id)

        # Vérification : seul l'auteur peut modifier
        if review.user_id != user_id:
            raise PermissionError("Vous ne pouvez modifier que vos propres reviews")

        # Validation du rating
        if 'rating' in data and not (1 <= data['rating'] <= 5):
            raise ValueError("Le rating doit être entre 1 et 5")

        self.review_repo.update(review_id, data)

    def delete_post(self, post_id, user_id):
        Supprime un post avec toutes ses dépendances
        post = self.post_repo.get(post_id)

        # Vérification
        if post.user_id != user_id and not is_admin(user_id):
            raise PermissionError("Permission refusée")

        # Supprime les images associées (avec fichiers physiques)
        for image in post.images:
            self.delete_image_post(image.id, user_id)

        # Supprime les reviews associées
        reviews = self.review_repo.get_by_attribute('post_id', post_id)
        for review in reviews:
            self.review_repo.delete(review.id)

        # Supprime le post
        self.post_repo.delete(post_id)
    """
