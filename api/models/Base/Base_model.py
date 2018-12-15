"""Base class model"""

# system imports
from datetime import datetime


# local imports
from ..db_config import db
from ..model_operation import ModelOperation


class BaseModel(db.Model, ModelOperation):
    """Base model"""

    __abstract__ = True

    id = db.Column(db.String(36), unique=True, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

