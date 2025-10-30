from backend.app.models.user import User
from backend.app.models.review import Review
from backend.app.models.image_post import ImagePost
from backend.app import db
from backend.app.persistence.user_repository import UserRepository
from backend.app.persistence.review_repository import ReviewRepository
from backend.app.persistence.image_post_repository import ImagePostRepository
import base64

class PortfolioFacade:
    """
    Façade principale de l'application 

    Cette classe centralise l'accès aux repositories spécifiques
    et fournit des méthodes de service pour la logique métier
    (création, mise à jour, suppression, authentification, etc.).
    
    Chaque méthode applique les règles de validation et gère
    les transactions avec rollback en cas d'erreur.
    """
    def __init__(self):
        self.user_repo = UserRepository()
        self.review_repo = ReviewRepository()
        self.image_post_repo = ImagePostRepository()

# -------------------- Authentification de l'utilisateur --------------------

    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur et le sauvegarde dans la base de données.
        Code Erreur:
            ValueError: Si l'email existe déjà, si le mot de passe est manquant
                        ou si une erreur survient lors de la création.
        """
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
        """
        Authentifie un utilisateur avec son email et mot de passe.

        Code Erreur:
            ValueError: Si l'email ou le mot de passe est incorrect ou manquant.
        """
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
        """
        On retourne un utilisateur par son ID
        Code Erreur:
            ValueError: Si aucun utilisateur n'est trouvé avec l'ID fourni.
        """
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
        """
        Liste tout les utilisateurs dans un format type dictionnaire
        Code Erreur:
            ValueError: Si une erreur survient lors de la récupération.
        """
        try:
            users = self.user_repo.get_all()
            return [user.to_dict() for user in users]

        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des utilisateurs : {str(e)}")

    def get_user_by_email(self, email):
        """ 
        Récupère un utilisateur à partir de son email.
        Code Erreur:
            ValueError: Si l'email est vide ou aucun utilisateur n'est trouvé.
        """
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


        Code Erreur:
            ValueError: Si tentative de modifier le mot de passe ou si l'utilisateur n'existe pas.
            PermissionError: Si l'utilisateur n'a pas le droit de modifier ce profil.
        """
        # ⚠️ Remarque : le mot de passe doit toujours être mis à jour via `update_user_password`.
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

        except PermissionError:
            db.session.rollback()
            raise  # ne pas transformer en ValueError

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la mise à jour : {str(e)}")

    def update_user_password(self, user_id, old_password, new_password):
        """
        Met à jour le mot de passe d'un utilisateur de manière sécurisée.

        Returns:
            User: L'objet utilisateur mis à jour

        Code Erreur:
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

        Code Erreur:
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
        try:
            user_id = review_data.get('user_id')
            image_post_id = review_data.get('image_post_id')

            if not user_id:
                raise ValueError("user_id est requis")
            if not image_post_id:
                raise ValueError("image_post_id est requis")

            user = self.get_user_by_id(user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}")
            image_post = self.get_post_image(image_post_id)
            if not image_post:
                raise ValueError(f"Aucune image trouvé avec l'ID {image_post_id}")

            comment = review_data.get('comment')

            review = Review(
                comment=comment,
                user_id=user.id,
                image_post_id=image_post.id
            )

            self.review_repo.add(review)
            return review

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la création du commentaire : {str(e)}")

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
        """Retourne tous les commentaires liés à une image spécifique"""
        try:
            reviews = self.review_repo.get_by_image_post_id(image_post_id)
            return reviews
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des commentaires : {str(e)}")

    def get_reviews_by_user(self, user_id):
        """Retourne tous les commentaires d'un utilisateur sous forme de dictionnaires"""
        try:
            reviews = self.review_repo.get_by_user_id(user_id)
            if not reviews:
                return []
            return [review.to_dict() for review in reviews]
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des commentaires : {str(e)}")

    def update_review(self, review_id, review_data):
        """Met à jour un commentaire"""
        try:
            review = self.review_repo.get(review_id)
            if not review:
                raise ValueError(f"Aucun commentaire trouvé avec l'ID {review_id}.")

            # Mise à jour via le repository (qui fait le commit)
            self.review_repo.update(review_id, review_data)
            updated_review = self.review_repo.get(review_id)
            return updated_review

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la mise à jour : {str(e)}")

    def delete_review(self, review_id):
        """Supprime un commentaire"""
        try:
            review = self.review_repo.get(review_id)
            if not review:
                raise ValueError(f"Aucun commentaire trouvé avec l'ID {review_id}.")

            # Suppression via le repository (qui fait le commit)
            self.review_repo.delete(review_id)
            return True

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la suppression : {str(e)}")

# -------------------- Post_image  --------------------
    def create_image_post(self, image_post_data):
        """
            Crée un nouveau post image pour un utilisateur.
            Code Erreur:
                ValueError: si des données sont manquantes ou invalides
        """
        try:
            # Vérification de la présence de user_id
            user_id = image_post_data.get("user_id")
            if not user_id:
                raise ValueError("user_id est requis")

            # Conversion de user_id en int si nécessaire
            # Permet d'empêcher que n'importe qu'elle valeur non valide se retrouve
            # dans l'user_id (utile pour les INSERT dans la db)
            if not isinstance(user_id, int):
                try:
                    user_id = int(user_id)
                except (ValueError, TypeError):
                    raise ValueError("user_id doit être un entier valide")

            # Vérification que l'utilisateur existe
            user = self.get_user_by_id(user_id)
            if not user:
                raise ValueError("Aucun utilisateur trouvé avec cet ID")

            title = image_post_data.get("title")

             # Vérifie l'unicité du titre pour cet utilisateur pour éviter qu'un
             # utilisateur créé plusieurs posts avec le même titre
            existing_post = self.image_post_repo.get_by_title_and_user(title, user_id)
            # cherche dans la base si un post existe déjà pour l'user id avec le titre
            if existing_post:
                raise ValueError("Cette image existe déjà pour cet utilisateur")

            # Décodage de l'image base64 en bytes
            image_data_b64 = image_post_data.get("image_data")
            try:
                image_data_bytes = base64.b64decode(image_data_b64)
            except Exception:
                raise ValueError("L'image n'est pas un base64 valide")

             # Vérification que le décodage a bien produit des bytes
            if not isinstance(image_data_bytes, bytes):
                raise ValueError("L'image doit être de type binaire (bytes)")
            
            # Création de l'objet ImagePost
            new_post = ImagePost(
                title=image_post_data.get("title"),
                description=image_post_data.get("description"),
                image_data=image_data_bytes,
                image_mime_type=image_post_data.get("image_mime_type"),
                user_id=user_id
            )

            # Ajout via le repository (qui fait le commit)
            self.image_post_repo.add(new_post)
            return new_post

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la création du post : {str(e)}")

    def get_post_image(self, image_post_id):
        """ Récupère un post image spécifique par son ID. """
        try:
            image = self.image_post_repo.get(image_post_id)
            if not image:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {image_post_id}.")
            return image
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération de l'image : {str(e)}")

    def get_all_post_images(self):
        """ Récupère tous les posts images. """
        try:
            return self.image_post_repo.get_all()  # retourne des objets ImagePost, pas des dicts
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des images : {str(e)}")


    def get_post_images_by_user(self, user_id):
        """ Récupère tous les posts images d'un utilisateur. """
        try:
            images = self.image_post_repo.get_by_user_id(user_id)
            return images
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des images : {str(e)}")

    def update_image_post(self, post_id, user_id, update_data):
        """
        Met à jour un post image
        
        Code Erreur:
            ValueError: si le post n'existe pas ou données invalides
            PermissionError: si l'utilisateur n'est pas le propriétaire du post
        """
        try:
            image_post = self.image_post_repo.get(post_id)
            if not image_post:
                raise ValueError("Image non trouvée")

            # Conversion user_id en int si nécessaire
            if not isinstance(user_id, int):
                try:
                    user_id = int(user_id)
                except (ValueError, TypeError):
                    raise ValueError("user_id doit être un entier valide")

            # Vérification que l'utilisateur est bien le propriétaire
            if image_post.user_id != user_id:
                raise PermissionError("Vous n'êtes pas autorisé à modifier cette image")

            # Décodage base64 si l'image est mise à jour
            if "image_data" in update_data:
                try:
                    update_data["image_data"] = base64.b64decode(update_data["image_data"])
                except Exception:
                    raise ValueError("L'image n'est pas un base64 valide")

                if not isinstance(update_data["image_data"], bytes):
                    raise ValueError("L'image doit être de type binaire (bytes).")

            # Mise à jour via le repository
            self.image_post_repo.update(post_id, update_data)
            updated_post = self.image_post_repo.get(post_id)

            return updated_post

        except (ValueError, PermissionError):
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la mise à jour : {str(e)}")

    def delete_image_post(self, post_id, user_id):
        """
        Supprime un post image
        
        Code Erreur:
            ValueError: si le post n'existe pas
            PermissionError: si l'utilisateur n'est pas le propriétaire
        """
        try:
            image_post = self.image_post_repo.get(post_id)
            if not image_post:
                raise ValueError("Image non trouvée")

            # Conversion user_id en int si nécessaire
            if not isinstance(user_id, int):
                try:
                    user_id = int(user_id)
                except (ValueError, TypeError):
                    raise ValueError("user_id doit être un entier valide")

            # Vérification que l'utilisateur est bien le propriétaire
            if image_post.user_id != user_id:
                raise PermissionError("Vous n'êtes pas autorisé à supprimer cette image")

            # Suppression via le repository
            self.image_post_repo.delete(post_id)
            return True

        except (ValueError, PermissionError):
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de la suppression : {str(e)}")

