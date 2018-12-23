"""Email field validation"""

# system imports
import re

# third party imports
from marshmallow import ValidationError

# email regex
EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')


def email_validation(data):
    """Validates the email"""

    if not EMAIL_REGEX.match(data):
        raise ValidationError('Please provide a valid email.')




