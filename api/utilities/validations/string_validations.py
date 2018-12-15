"""String validations"""


from marshmallow import ValidationError


def validate_string(data):
    """Validates the string"""

    if data and len(data) > 3:
        return data
    else:
        raise ValidationError('Field required and cannot be less '
                              'than three character')


