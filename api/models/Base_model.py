"""Base class model"""

# system imports
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4

# local imports
from . import db
from .model_operation import ModelOperation


class BaseModel(db.Model, ModelOperation):
    """Base model"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid4())
    deleted = db.Column(db.Boolean, nullable=True, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
