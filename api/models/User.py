"""User model"""

# local import
from main import db
from .Base_model import BaseModel


class UserModel(BaseModel):
    """User model"""

    # table name
    __tablename__ = 'users'

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)



