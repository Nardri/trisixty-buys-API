"""Base class model"""

# system imports
from datetime import datetime

# local imports
from ..db_config import db
from ..model_operation import ModelOperation

# utilities
from api.utilities.helpers.date_time import date_time


class BaseModel(db.Model, ModelOperation):
    """Base model"""

    __abstract__ = True

    id = db.Column(db.String(36), unique=True, primary_key=True)

    created_at = db.Column(db.DateTime, default=date_time.time())
    updated_at = db.Column(db.DateTime, onupdate=date_time.time())
    deleted = db.Column(db.Boolean, default=False)
