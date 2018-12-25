"""Module for user schema"""

# third party imports
from marshmallow import fields

# base schema
from .base_schema import BaseSchema

# utilities
from api.utilities.validations.string_validations import validate_string
from api.utilities.validations.validations import (email_validation,
                                                   password_validation)


class UserSchema(BaseSchema):
    """User schema"""

    verified = fields.Boolean(dump_only=True)
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

    token = fields.String()

    email = fields.String(required=True, validate=email_validation)
    password = fields.String(required=True, validate=password_validation)
    password_reset = fields.String(required=True, validate=validate_string)
