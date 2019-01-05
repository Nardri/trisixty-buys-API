"""String validations"""

# third part imports
from marshmallow import ValidationError
from api.utilities.constants import MESSAGES


def validate_string(data):
    """Validates the string"""

    if data and len(data) > 3:
        return data
    else:
        raise ValidationError(MESSAGES['REQUIRED_FIELDS'])
