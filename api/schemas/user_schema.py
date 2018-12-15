"""Module for user schema"""

from .base_schema import BaseSchema
from marshmallow import fields

from api.utilities.validations.string_validations import validate_string


class UserSchema(BaseSchema):
    """User schema"""

    first_name = fields.String(
        required=True,
        dump_to='firstName',
        load_from='firstname',
        validate=validate_string)
    last_name = fields.String(
        required=True,
        dump_to='lastName',
        load_from='lastname',
        validate=validate_string)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
