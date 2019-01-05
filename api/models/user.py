"""User model"""

# local import
from .db_config import db
from api.models.Base.Base_model import BaseModel


class User(BaseModel):
    """User model"""

    # table name
    __tablename__ = 'users'

    verified = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=True)
    password_reset = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.email)
