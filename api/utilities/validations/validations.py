"""Email field validation"""

# system imports
import re

# third party imports
from marshmallow import ValidationError

from api.utilities.constants import MESSAGES

# email regex
EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

# password regex
PASSWORD_REGEX = re.compile(
    r'(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$)'
)


def email_validation(data):
    """Validates the email"""

    if not EMAIL_REGEX.match(data):
        raise ValidationError(MESSAGES['EMAIL_FORMAT'])


def password_validation(data):
    """Validates the password"""

    if not PASSWORD_REGEX.match(data):
        raise ValidationError(MESSAGES['INVALID_PASSWORD'])
