"""Errors"""

# utilities
from api.utilities.validations.custom_validations_error import ValidationError


def raises(message, status_code):
    """A helper method for raising exceptions.

    Args:
        message (str): Message
        status_code (int): Status code

    Raises:
        ValidationError

    """
    raise ValidationError(dict(message=message), status_code)
