"""Module for user schema"""

# third party imports
from marshmallow import fields

# base schema
from .base_schema import BaseSchema

# utilities
from api.utilities.validations.string_validations import validate_string
from api.utilities.validations.email_validation import email_validation


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
    email = fields.String(
            required=True,
            validate=(validate_string, email_validation))
    password = fields.String(required=True, validate=validate_string)
