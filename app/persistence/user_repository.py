from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        """ Initializes the UserRepository with the User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """ Retrieve a user instance by their email address."""
        return self.model.query.filter_by(email=email).first()
