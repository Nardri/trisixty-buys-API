"""Module for all base schemas"""

from marshmallow import fields, Schema
from api.utilities.validations.custom_validations import ValidationError


class BaseSchema(Schema):
    """Base schema for all schemas."""

    id = fields.String(dump_only=True)
    deleted = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def load_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema"""

        data, errors = self.load(data, partial=partial)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data
