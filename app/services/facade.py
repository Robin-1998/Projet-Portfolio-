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
    user = User(**user_data)
    user.hash_password(user_data['password'])
    self.user_repo.add(user)
    db.session.commit()
    return user

  def login_user(self, email, password):
      user = self.get_user_by_email(email)
      if user and user.verify_password(password):
          return user
      return None
  
  def get_users(self, user_id):
    """ On retourne un utilisateur par son ID """
    return self.user_repo.get(user_id)

  def get_all_user(self):
    """ Liste tout les utilisateurs dans un format type dictionnaire """
    users = self.user_repo.get_all()
    return [user.to_dict() for user in users]

  def get_user_by_email(self, email):
    """ Cherche utilsateur à partir de son mail """
    return self.user_repo.get_by_attribute('email', email)

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

