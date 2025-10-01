from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import SQLAlchemyRepository

class PortfolioFacade:

  def __init__(self):
    self.user_repo = SQLAlchemyRepository(User)

----------------------------- Authentification --------------------------------------
----------------------------- de l'utilisateur --------------------------------------

  def create_user(self, user_data):
    """ Création du compte utilisateur """
    try:
      # Vérifie si l'email existe déjà
      existing_user = self.user_repo.get_user_by_email(user_data['email'])
      if existing_user:
        raise ValueError(f"Un utilisateur avec l'email {user_data['email']} existe déjà.")
      # Si l'email n'existe pas, on créé un utilisateur
      if 'password' not in user_data:
        raise ValueError("Le mot de passe est requis pour la création de l'utilisateur.")
      # Si l'email n'existe pas, on créé un utilisateur
      user = User(**user_data)
      user.hash_password(user_data['password'])
      self.user_repo.add(user)
      db.session.commit()
      return user
    except Exception as e:
      db.session.rollback()
        logging.error(f"Erreur lors de la création de l'utilisateur: {str(e)}")
        raise ValueError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

  def login_user(self, email, password):
    try:
      user = self.get_user_by_email(email)
      if not user:
        raise ValueError("Aucun utilisateur trouvé avec cet email.")
      if not user.verify_password(password):
        raise ValueError("Mot de passe incorrect.")
      return user

  except Exception as e:
    logging.error(f"Erreur lors de la connexion: {str(e)}")
    raise ValueError(f"Erreur lors de la connexion: {str(e)}")


  def get_users(self, user_id):
    """ On retourne un utilisateur par son ID """
    try:
      return self.user_repo.get(user_id)
    except Exception as e:
      logging.error(f"Erreur lors de la récupération de l'utilisateur par ID: {str(e)}")
      raise ValueError(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")

  def get_all_user(self):
    """ Liste tout les utilisateurs dans un format type dictionnaire """
    try:
      users = self.user_repo.get_all()
      return [user.to_dict() for user in users]
    except Exception as e:
      logging.error(f"Erreur lors de la récupération de tous les utilisateurs: {str(e)}")
      raise ValueError(f"Erreur lors de la récupération des utilisateurs: {str(e)}")

  def get_user_by_email(self, email):
    """ Cherche utilsateur à partir de son email """
    try:
      user = self.user_repo.get_by_attribute('email', email)
      if not user:
        raise ValueError(f"Aucun utilisateur trouvé avec l'email {email}.")
      return user
    except Exception as e:
      logging.error(f"Erreur lors de la récupération de l'utilisateur par email: {str(e)}")
      raise ValueError(f"Erreur lors de la récupération de l'utilisateur par email: {str(e)}")

  def update_user(self, user_id, data):
    """ On met à jour la donnée d'un utilisateur """
    user = self.user_repo.update(user_id, data)
    db.session.commit()
    return user

  def delete_user(self, user_id):
    """ Suprimez un utilisateur (admin) """
    self.user_repo.delete(user_id)
    db.session.commit()
    return True    


